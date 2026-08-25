"""中間表現から KDP 入稿用の .docx を生成する。

python-docx などに依存せず、OOXML(WordprocessingML)を直接組み立てて
zip に固める。KDPの要件に合わせて次を作り込んでいる。

* 見出しを Word 組み込みの Heading 1〜3 スタイル + ``outlineLvl`` で出力する
  (KDPの自動変換とKindleの目次ジャンプはこれを見ている)
* 章見出しにブックマークを打ち、リンク付き目次(``toc.style: link``)と
  Wordの目次フィールド(``toc.style: field``、ページ番号入り)の両方を出せる
* ペーパーバック向けに判型・見開き余白(mirrorMargins)・ノド・柱番号を設定する
* ルビ(``w:ruby``)、画像(``w:drawing``)、箇条書き(``numbering.xml``)に対応
"""

from __future__ import annotations

import datetime as _dt
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from xml.sax.saxutils import escape, quoteattr

from .config import BookConfig, LayoutConfig, mm_to_twips
from .images import ImageError, ImageInfo, probe
from .mdparse import (
    Block,
    Chapter,
    CodeBlock,
    CodeSpan,
    Document,
    Emph,
    Heading,
    ImageBlock,
    Inline,
    Link,
    ListBlock,
    PageBreak,
    Paragraph,
    Quote,
    Ruby,
    SceneBreak,
    Strong,
    Text,
)

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
CT_NS = "http://schemas.openxmlformats.org/package/2006/content-types"
PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
REL_BASE = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
CORE_PROPS_REL = (
    "http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties"
)

DOC_NS_DECL = (
    f'xmlns:w="{W_NS}" '
    f'xmlns:r="{R_NS}" '
    'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
    'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
    'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"'
)

XML_DECL = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'

BULLET_NUM_ID = 1
ORDERED_NUM_ID = 2


@dataclass
class DocxResult:
    path: Path
    warnings: list[str] = field(default_factory=list)


def build_docx(
    book: BookConfig,
    document: Document,
    profile: str,
    out_path: str | Path,
) -> DocxResult:
    """``profile`` (``ebook`` / ``print``)の .docx を ``out_path`` に書き出す。"""
    writer = _DocxWriter(book, document, book.layout(profile))
    return writer.write(Path(out_path))


class _DocxWriter:
    def __init__(self, book: BookConfig, document: Document, layout: LayoutConfig) -> None:
        self.book = book
        self.doc = document
        self.layout = layout
        self.warnings: list[str] = []
        self._rels: list[tuple[str, str, str, bool]] = []
        self._rel_seq = 10
        self._media: dict[str, tuple[str, str]] = {}  # 実パス -> (zip内名, rId)
        self._image_files: list[tuple[str, Path]] = []
        self._bookmark_id = 100
        self._drawing_id = 1000
        self._extensions: set[str] = set()

    # ------------------------------------------------------------------ 出力本体
    def write(self, out_path: Path) -> DocxResult:
        out_path.parent.mkdir(parents=True, exist_ok=True)

        # 先に本文を組み立てる(この過程で画像・リンクの関係IDが確定する)
        body = self._body_xml()
        document_xml = f"{XML_DECL}<w:document {DOC_NS_DECL}><w:body>{body}</w:body></w:document>"

        parts: dict[str, bytes] = {
            "[Content_Types].xml": self._content_types().encode("utf-8"),
            "_rels/.rels": self._package_rels().encode("utf-8"),
            "docProps/core.xml": self._core_props().encode("utf-8"),
            "docProps/app.xml": self._app_props().encode("utf-8"),
            "word/document.xml": document_xml.encode("utf-8"),
            "word/_rels/document.xml.rels": self._document_rels().encode("utf-8"),
            "word/styles.xml": self._styles().encode("utf-8"),
            "word/settings.xml": self._settings().encode("utf-8"),
            "word/numbering.xml": self._numbering().encode("utf-8"),
        }
        if self.layout.page_numbers:
            parts["word/footer1.xml"] = self._footer().encode("utf-8")

        with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for name, data in parts.items():
                zf.writestr(name, data)
            for zip_name, src in self._image_files:
                zf.write(src, zip_name)
        return DocxResult(out_path, self.warnings)

    # ----------------------------------------------------------------- 関係(rels)
    def _add_rel(self, rel_type: str, target: str, *, external: bool = False) -> str:
        rid = f"rId{self._rel_seq}"
        self._rel_seq += 1
        self._rels.append((rid, rel_type, target, external))
        return rid

    def _image_rel(self, path: Path) -> tuple[str, ImageInfo] | None:
        try:
            info = probe(path)
        except (OSError, ImageError) as exc:
            self.warnings.append(f"画像を埋め込めませんでした: {exc}")
            return None
        key = str(path.resolve())
        if key not in self._media:
            ext = path.suffix.lower().lstrip(".") or "png"
            self._extensions.add(ext)
            zip_name = f"word/media/image{len(self._media) + 1}.{ext}"
            rid = self._add_rel(f"{REL_BASE}/image", zip_name[len("word/") :])
            self._media[key] = (zip_name, rid)
            self._image_files.append((zip_name, path))
        return self._media[key][1], info

    def _document_rels(self) -> str:
        rels = [
            ("rId1", f"{REL_BASE}/styles", "styles.xml", False),
            ("rId2", f"{REL_BASE}/settings", "settings.xml", False),
            ("rId3", f"{REL_BASE}/numbering", "numbering.xml", False),
        ]
        if self.layout.page_numbers:
            rels.append(("rId4", f"{REL_BASE}/footer", "footer1.xml", False))
        rels.extend(self._rels)
        items = "".join(
            f'<Relationship Id="{rid}" Type="{rtype}" Target={quoteattr(target)}'
            + (' TargetMode="External"/>' if external else "/>")
            for rid, rtype, target, external in rels
        )
        return f'{XML_DECL}<Relationships xmlns="{PKG_REL_NS}">{items}</Relationships>'

    def _package_rels(self) -> str:
        return (
            f'{XML_DECL}<Relationships xmlns="{PKG_REL_NS}">'
            f'<Relationship Id="rId1" Type="{REL_BASE}/officeDocument" Target="word/document.xml"/>'
            f'<Relationship Id="rId2" Type="{CORE_PROPS_REL}" Target="docProps/core.xml"/>'
            f'<Relationship Id="rId3" Type="{REL_BASE}/extended-properties" Target="docProps/app.xml"/>'
            "</Relationships>"
        )

    def _content_types(self) -> str:
        defaults = [
            ('rels', 'application/vnd.openxmlformats-package.relationships+xml'),
            ('xml', 'application/xml'),
        ]
        image_types = {
            "png": "image/png",
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "gif": "image/gif",
            "bmp": "image/bmp",
            "tif": "image/tiff",
            "tiff": "image/tiff",
        }
        for ext in sorted(self._extensions):
            defaults.append((ext, image_types.get(ext, "application/octet-stream")))
        wml = "application/vnd.openxmlformats-officedocument.wordprocessingml"
        overrides = [
            ("/word/document.xml", f"{wml}.document.main+xml"),
            ("/word/styles.xml", f"{wml}.styles+xml"),
            ("/word/settings.xml", f"{wml}.settings+xml"),
            ("/word/numbering.xml", f"{wml}.numbering+xml"),
            (
                "/docProps/core.xml",
                "application/vnd.openxmlformats-package.core-properties+xml",
            ),
            (
                "/docProps/app.xml",
                "application/vnd.openxmlformats-officedocument.extended-properties+xml",
            ),
        ]
        if self.layout.page_numbers:
            overrides.insert(4, ("/word/footer1.xml", f"{wml}.footer+xml"))
        body = "".join(f'<Default Extension="{e}" ContentType="{c}"/>' for e, c in defaults)
        body += "".join(f'<Override PartName="{p}" ContentType="{c}"/>' for p, c in overrides)
        return f'{XML_DECL}<Types xmlns="{CT_NS}">{body}</Types>'

    def _core_props(self) -> str:
        now = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        b = self.book
        keywords = ", ".join(b.keywords)
        return (
            f"{XML_DECL}<cp:coreProperties "
            'xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" '
            'xmlns:dcterms="http://purl.org/dc/terms/" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            f"<dc:title>{escape(b.full_title)}</dc:title>"
            f"<dc:creator>{escape(b.author)}</dc:creator>"
            f"<dc:description>{escape(b.description[:1000])}</dc:description>"
            f"<cp:keywords>{escape(keywords)}</cp:keywords>"
            f"<cp:lastModifiedBy>{escape(b.author)}</cp:lastModifiedBy>"
            f'<dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>'
            f'<dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>'
            "</cp:coreProperties>"
        )

    def _app_props(self) -> str:
        return (
            f"{XML_DECL}<Properties "
            'xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
            'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
            "<Application>kdp-pipeline</Application>"
            f"<Company>{escape(self.book.publisher)}</Company>"
            f"<Characters>{self.doc.char_count()}</Characters>"
            "</Properties>"
        )

    # -------------------------------------------------------------------- 設定など
    def _settings(self) -> str:
        parts = ['<w:zoom w:percent="100"/>']
        if self.layout.mirror_margins:
            parts.append("<w:mirrorMargins/>")
        parts.append('<w:defaultTabStop w:val="840"/>')
        if self.layout.toc.style in ("field", "both"):
            parts.append('<w:updateFields w:val="true"/>')
        parts.append(
            "<w:compat><w:compatSetting w:name=\"compatibilityMode\" "
            'w:uri="http://schemas.microsoft.com/office/word" w:val="15"/></w:compat>'
        )
        parts.append(f'<w:themeFontLang w:val="en-US" w:eastAsia="{self.book.language}-JP"/>'
                     if self.book.language == "ja"
                     else '<w:themeFontLang w:val="en-US"/>')
        return f'{XML_DECL}<w:settings xmlns:w="{W_NS}">{"".join(parts)}</w:settings>'

    def _footer(self) -> str:
        return (
            f'{XML_DECL}<w:ftr {DOC_NS_DECL}>'
            '<w:p><w:pPr><w:pStyle w:val="Footer"/><w:jc w:val="center"/></w:pPr>'
            '<w:fldSimple w:instr=" PAGE   \\* MERGEFORMAT ">'
            "<w:r><w:t>1</w:t></w:r></w:fldSimple></w:p></w:ftr>"
        )

    def _numbering(self) -> str:
        def lvl(i: int, ordered: bool) -> str:
            indent = 425 * (i + 1)
            if ordered:
                fmt, text = "decimal", f"%{i + 1}."
            else:
                fmt, text = "bullet", ("・", "－", "＊")[i]
            return (
                f'<w:lvl w:ilvl="{i}"><w:start w:val="1"/>'
                f'<w:numFmt w:val="{fmt}"/>'
                f'<w:lvlText w:val="{escape(text)}"/>'
                '<w:lvlJc w:val="left"/>'
                f'<w:pPr><w:ind w:left="{indent}" w:hanging="425"/></w:pPr>'
                '<w:rPr><w:rFonts w:hint="eastAsia"/></w:rPr>'
                "</w:lvl>"
            )

        bullet = "".join(lvl(i, False) for i in range(3))
        ordered = "".join(lvl(i, True) for i in range(3))
        return (
            f'{XML_DECL}<w:numbering xmlns:w="{W_NS}">'
            f'<w:abstractNum w:abstractNumId="0"><w:multiLevelType w:val="hybridMultilevel"/>{bullet}</w:abstractNum>'
            f'<w:abstractNum w:abstractNumId="1"><w:multiLevelType w:val="hybridMultilevel"/>{ordered}</w:abstractNum>'
            f'<w:num w:numId="{BULLET_NUM_ID}"><w:abstractNumId w:val="0"/></w:num>'
            f'<w:num w:numId="{ORDERED_NUM_ID}"><w:abstractNumId w:val="1"/></w:num>'
            "</w:numbering>"
        )

    # ------------------------------------------------------------------ スタイル
    def _styles(self) -> str:
        lay = self.layout
        sz = _half_points(lay.base_font_pt)
        line = int(round(240 * lay.line_spacing))
        body_fonts = _fonts(lay.body_font)
        head_fonts = _fonts(lay.heading_font)

        def style(
            sid: str,
            name: str,
            *,
            stype: str = "paragraph",
            based_on: str | None = "Normal",
            next_style: str | None = None,
            ppr: str = "",
            rpr: str = "",
            quick: bool = True,
            default: bool = False,
        ) -> str:
            head = (
                f'<w:style w:type="{stype}"'
                + (' w:default="1"' if default else "")
                + f' w:styleId="{sid}">'
            )
            head += f"<w:name w:val={quoteattr(name)}/>"
            if based_on:
                head += f'<w:basedOn w:val="{based_on}"/>'
            if next_style:
                head += f'<w:next w:val="{next_style}"/>'
            if quick:
                head += "<w:qFormat/>"
            if ppr:
                head += f"<w:pPr>{ppr}</w:pPr>"
            if rpr:
                head += f"<w:rPr>{rpr}</w:rPr>"
            return head + "</w:style>"

        heading_common = "<w:keepNext/><w:keepLines/>"

        styles = [
            style(
                "Normal",
                "Normal",
                based_on=None,
                default=True,
                ppr=(
                    f'<w:spacing w:before="0" w:after="0" w:line="{line}" w:lineRule="auto"/>'
                    + _first_line_indent(lay, sz)
                    + '<w:jc w:val="both"/>'
                ),
                rpr=f'{body_fonts}<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/>',
            ),
            style(
                "Heading1",
                "heading 1",
                next_style="Normal",
                ppr=(
                    f"{heading_common}<w:pageBreakBefore/>"
                    f'<w:spacing w:before="0" w:after="{int(sz * 14)}" w:line="240" w:lineRule="auto"/>'
                    '<w:ind w:firstLine="0" w:firstLineChars="0"/>'
                    '<w:jc w:val="left"/><w:outlineLvl w:val="0"/>'
                ),
                rpr=f'{head_fonts}<w:b/><w:sz w:val="{_scale(sz, 1.8)}"/><w:szCs w:val="{_scale(sz, 1.8)}"/>',
            ),
            style(
                "Heading2",
                "heading 2",
                next_style="Normal",
                ppr=(
                    f"{heading_common}"
                    f'<w:spacing w:before="{int(sz * 10)}" w:after="{int(sz * 5)}" w:line="240" w:lineRule="auto"/>'
                    '<w:ind w:firstLine="0" w:firstLineChars="0"/>'
                    '<w:jc w:val="left"/><w:outlineLvl w:val="1"/>'
                ),
                rpr=f'{head_fonts}<w:b/><w:sz w:val="{_scale(sz, 1.35)}"/><w:szCs w:val="{_scale(sz, 1.35)}"/>',
            ),
            style(
                "Heading3",
                "heading 3",
                next_style="Normal",
                ppr=(
                    f"{heading_common}"
                    f'<w:spacing w:before="{int(sz * 8)}" w:after="{int(sz * 4)}" w:line="240" w:lineRule="auto"/>'
                    '<w:ind w:firstLine="0" w:firstLineChars="0"/>'
                    '<w:jc w:val="left"/><w:outlineLvl w:val="2"/>'
                ),
                rpr=f'{head_fonts}<w:b/><w:sz w:val="{_scale(sz, 1.15)}"/><w:szCs w:val="{_scale(sz, 1.15)}"/>',
            ),
            style(
                "Title",
                "Title",
                next_style="Normal",
                ppr=(
                    '<w:spacing w:before="2400" w:after="240" w:line="240" w:lineRule="auto"/>'
                    '<w:ind w:firstLine="0" w:firstLineChars="0"/><w:jc w:val="center"/>'
                ),
                rpr=f'{head_fonts}<w:b/><w:sz w:val="{_scale(sz, 2.4)}"/><w:szCs w:val="{_scale(sz, 2.4)}"/>',
            ),
            style(
                "Subtitle",
                "Subtitle",
                next_style="Normal",
                ppr=(
                    '<w:spacing w:before="0" w:after="960" w:line="240" w:lineRule="auto"/>'
                    '<w:ind w:firstLine="0" w:firstLineChars="0"/><w:jc w:val="center"/>'
                ),
                rpr=f'{head_fonts}<w:sz w:val="{_scale(sz, 1.3)}"/><w:szCs w:val="{_scale(sz, 1.3)}"/>',
            ),
            style(
                "TOCHeading",
                "TOC Heading",
                based_on="Heading1",
                next_style="Normal",
                ppr='<w:pageBreakBefore/><w:outlineLvl w:val="9"/>',
            ),
            style(
                "Quote",
                "Quote",
                next_style="Normal",
                ppr=(
                    f'<w:spacing w:before="{int(sz * 5)}" w:after="{int(sz * 5)}" w:line="{line}" w:lineRule="auto"/>'
                    '<w:ind w:left="480" w:right="240" w:firstLine="0" w:firstLineChars="0"/>'
                ),
                rpr="<w:i/>",
            ),
            style(
                "Code",
                "HTML Preformatted",
                next_style="Normal",
                ppr=(
                    '<w:shd w:val="clear" w:color="auto" w:fill="F4F4F4"/>'
                    '<w:kinsoku w:val="0"/><w:wordWrap w:val="0"/>'
                    '<w:spacing w:before="120" w:after="120" w:line="240" w:lineRule="auto"/>'
                    '<w:ind w:left="240" w:firstLine="0" w:firstLineChars="0"/>'
                    '<w:jc w:val="left"/>'
                ),
                rpr=(
                    '<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas" w:eastAsia="ＭＳ ゴシック"/>'
                    f'<w:sz w:val="{_scale(sz, 0.85)}"/><w:szCs w:val="{_scale(sz, 0.85)}"/>'
                ),
            ),
            style(
                "Caption",
                "caption",
                next_style="Normal",
                ppr=(
                    '<w:spacing w:before="60" w:after="240" w:line="240" w:lineRule="auto"/>'
                    '<w:ind w:firstLine="0" w:firstLineChars="0"/><w:jc w:val="center"/>'
                ),
                rpr=f'<w:sz w:val="{_scale(sz, 0.85)}"/><w:szCs w:val="{_scale(sz, 0.85)}"/>',
            ),
            style(
                "ListParagraph",
                "List Paragraph",
                next_style="Normal",
                ppr=(
                    '<w:ind w:firstLine="0" w:firstLineChars="0"/>'
                    '<w:contextualSpacing/><w:jc w:val="left"/>'
                ),
            ),
            style(
                "Figure",
                "Figure",
                next_style="Normal",
                ppr=(
                    '<w:spacing w:before="240" w:after="60" w:line="240" w:lineRule="auto"/>'
                    '<w:ind w:firstLine="0" w:firstLineChars="0"/><w:jc w:val="center"/>'
                ),
            ),
            style(
                "SceneBreak",
                "Scene Break",
                next_style="Normal",
                ppr=(
                    '<w:spacing w:before="240" w:after="240" w:line="240" w:lineRule="auto"/>'
                    '<w:ind w:firstLine="0" w:firstLineChars="0"/><w:jc w:val="center"/>'
                ),
            ),
            style(
                "Footer",
                "footer",
                ppr=(
                    '<w:tabs><w:tab w:val="center" w:pos="4252"/><w:tab w:val="right" w:pos="8504"/></w:tabs>'
                    '<w:spacing w:line="240" w:lineRule="auto"/>'
                    '<w:ind w:firstLine="0" w:firstLineChars="0"/>'
                ),
                rpr=f'<w:sz w:val="{_scale(sz, 0.85)}"/>',
                quick=False,
            ),
            style(
                "Colophon",
                "Colophon",
                ppr=(
                    f'<w:spacing w:before="0" w:after="0" w:line="{line}" w:lineRule="auto"/>'
                    '<w:ind w:firstLine="0" w:firstLineChars="0"/><w:jc w:val="left"/>'
                ),
                rpr=f'<w:sz w:val="{_scale(sz, 0.9)}"/>',
                quick=False,
            ),
            style(
                "DefaultParagraphFont",
                "Default Paragraph Font",
                stype="character",
                based_on=None,
                quick=False,
                default=True,
            ),
            style(
                "Hyperlink",
                "Hyperlink",
                stype="character",
                based_on=None,
                rpr='<w:color w:val="0563C1"/><w:u w:val="single"/>',
                quick=False,
            ),
        ]
        for i in range(1, 4):
            styles.append(
                style(
                    f"TOC{i}",
                    f"toc {i}",
                    next_style="Normal",
                    ppr=(
                        '<w:tabs><w:tab w:val="right" w:leader="dot" w:pos="8504"/></w:tabs>'
                        f'<w:spacing w:before="{0 if i > 1 else 120}" w:after="60" w:line="240" w:lineRule="auto"/>'
                        f'<w:ind w:left="{(i - 1) * 320}" w:right="480" w:hanging="0" '
                        'w:firstLine="0" w:firstLineChars="0"/>'
                        '<w:jc w:val="left"/>'
                    ),
                    quick=False,
                )
            )

        doc_defaults = (
            "<w:docDefaults>"
            f'<w:rPrDefault><w:rPr>{body_fonts}<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/>'
            f'<w:lang w:val="en-US" w:eastAsia="{"ja-JP" if self.book.language == "ja" else "en-US"}"/>'
            "</w:rPr></w:rPrDefault>"
            "<w:pPrDefault><w:pPr>"
            f'<w:spacing w:line="{line}" w:lineRule="auto"/>'
            "</w:pPr></w:pPrDefault>"
            "</w:docDefaults>"
        )
        return f'{XML_DECL}<w:styles xmlns:w="{W_NS}">{doc_defaults}{"".join(styles)}</w:styles>'

    # ---------------------------------------------------------------------- 本文
    def _body_xml(self) -> str:
        out: list[str] = []
        first_page_used = False

        if self.book.frontmatter.title_page:
            out.append(self._title_page())
            first_page_used = True

        if self.book.frontmatter.copyright_page:
            out.append(self._copyright_page(page_break=first_page_used))
            first_page_used = True

        toc_xml = self._toc()
        if toc_xml:
            out.append(toc_xml)
            first_page_used = True

        for chapter in self.doc.chapters:
            out.append(self._chapter(chapter, force_break=first_page_used))
            first_page_used = True

        if self.book.frontmatter.colophon:
            out.append(self._colophon())

        out.append(self._sect_pr())
        return "".join(out)

    def _title_page(self) -> str:
        b = self.book
        parts = [_para(_runs_text(b.title), style="Title")]
        if b.subtitle:
            parts.append(_para(_runs_text(b.subtitle), style="Subtitle"))
        parts.append(_para(_runs_text(b.author), style="Subtitle"))
        if b.publisher:
            parts.append(_para(_runs_text(b.publisher), style="Caption"))
        return "".join(parts)

    def _copyright_page(self, *, page_break: bool) -> str:
        b = self.book
        lines = [b.full_title, b.copyright_line]
        if b.publisher:
            lines.append(f"発行: {b.publisher}")
        if b.isbn:
            lines.append(f"ISBN: {b.isbn}")
        lines.append("本書の内容の一部または全部を、著作権者の許可なく複製・転載することを禁じます。")
        out = []
        for i, line in enumerate(lines):
            out.append(
                _para(
                    _runs_text(line),
                    style="Colophon",
                    page_break_before=(page_break and i == 0),
                )
            )
        return "".join(out)

    def _toc(self) -> str:
        toc = self.layout.toc
        if toc.style == "none":
            return ""
        entries = self.doc.headings(max_level=toc.depth)
        if not entries:
            return ""

        parts = [_para(_runs_text(toc.title), style="TOCHeading")]

        if toc.style in ("field", "both"):
            instr = f' TOC \\o "1-{toc.depth}" \\h \\z \\u '
            placeholder = (
                "Wordで目次を右クリックし「フィールド更新」を実行すると、"
                "ページ番号付きの目次に置き換わります。"
            )
            parts.append(
                "<w:p>"
                f"<w:fldSimple w:instr={quoteattr(instr)}>"
                f'<w:r><w:rPr><w:webHidden/></w:rPr><w:t xml:space="preserve">{escape(placeholder)}</w:t></w:r>'
                "</w:fldSimple></w:p>"
            )

        if toc.style in ("link", "both"):
            for _chapter, heading in entries:
                anchor = _bookmark_name(heading.index)
                runs = _runs_text(heading.text)
                parts.append(
                    f"<w:p><w:pPr><w:pStyle w:val=\"TOC{min(3, heading.level)}\"/></w:pPr>"
                    f'<w:hyperlink w:anchor="{anchor}">{runs}</w:hyperlink></w:p>'
                )
        return "".join(parts)

    def _chapter(self, chapter: Chapter, *, force_break: bool) -> str:
        parts: list[str] = []
        first = True
        for block in chapter.blocks:
            override_break: bool | None = None
            if first and isinstance(block, Heading) and block.level == 1:
                if not chapter.page_break or not force_break:
                    override_break = False
            parts.append(self._block(block, page_break_before=override_break))
            first = False
        return "".join(parts)

    def _colophon(self) -> str:
        b = self.book
        lines = [b.full_title]
        if b.published:
            lines.append(f"{b.published}　発行")
        lines.append(f"著者　{b.author}")
        if b.publisher:
            lines.append(f"発行　{b.publisher}")
        if b.isbn:
            lines.append(f"ISBN　{b.isbn}")
        if b.frontmatter.colophon_note:
            lines.append(b.frontmatter.colophon_note)
        lines.append(b.copyright_line)

        out = [_para(_runs_text("奥付"), style="Heading1", page_break_before=True)]
        out.extend(_para(_runs_text(line), style="Colophon") for line in lines)
        return "".join(out)

    def _sect_pr(self) -> str:
        lay = self.layout
        m = lay.margins
        footer_ref = '<w:footerReference w:type="default" r:id="rId4"/>' if lay.page_numbers else ""
        return (
            "<w:sectPr>"
            f"{footer_ref}"
            f'<w:pgSz w:w="{mm_to_twips(lay.width_mm)}" w:h="{mm_to_twips(lay.height_mm)}"/>'
            f'<w:pgMar w:top="{mm_to_twips(m.top_mm)}" w:right="{mm_to_twips(m.outside_mm)}" '
            f'w:bottom="{mm_to_twips(m.bottom_mm)}" w:left="{mm_to_twips(m.inside_mm)}" '
            f'w:header="{mm_to_twips(max(8.0, m.top_mm / 2))}" '
            f'w:footer="{mm_to_twips(max(8.0, m.bottom_mm / 2))}" '
            f'w:gutter="{mm_to_twips(m.gutter_mm)}"/>'
            '<w:docGrid w:linePitch="360"/>'
            "</w:sectPr>"
        )

    # ------------------------------------------------------------------ ブロック
    def _block(self, block: Block, *, page_break_before: bool | None = None) -> str:
        if isinstance(block, Heading):
            return self._heading(block, page_break_before=page_break_before)
        if isinstance(block, Paragraph):
            return _para(self._runs(block.inlines), page_break_before=page_break_before)
        if isinstance(block, ListBlock):
            return self._list(block)
        if isinstance(block, Quote):
            return "".join(_para(self._runs(p), style="Quote") for p in block.paragraphs)
        if isinstance(block, CodeBlock):
            return self._code(block)
        if isinstance(block, ImageBlock):
            return self._image(block)
        if isinstance(block, SceneBreak):
            return _para(_runs_text("＊　＊　＊"), style="SceneBreak")
        if isinstance(block, PageBreak):
            return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'
        return ""

    def _heading(self, heading: Heading, *, page_break_before: bool | None = None) -> str:
        self._bookmark_id += 1
        anchor = _bookmark_name(heading.index)
        inner = (
            f'<w:bookmarkStart w:id="{self._bookmark_id}" w:name="{anchor}"/>'
            f"{self._runs(heading.inlines)}"
            f'<w:bookmarkEnd w:id="{self._bookmark_id}"/>'
        )
        return _para(
            inner,
            style=f"Heading{min(3, heading.level)}",
            page_break_before=page_break_before,
        )

    def _list(self, block: ListBlock) -> str:
        num_id = ORDERED_NUM_ID if block.ordered else BULLET_NUM_ID
        out = []
        for item in block.items:
            ppr = (
                '<w:pStyle w:val="ListParagraph"/>'
                f'<w:numPr><w:ilvl w:val="{item.level}"/><w:numId w:val="{num_id}"/></w:numPr>'
                '<w:ind w:firstLine="0" w:firstLineChars="0"/>'
            )
            out.append(f"<w:p><w:pPr>{ppr}</w:pPr>{self._runs(item.inlines)}</w:p>")
        return "".join(out)

    def _code(self, block: CodeBlock) -> str:
        out = []
        for line in block.text.split("\n"):
            run = (
                f'<w:r><w:t xml:space="preserve">{escape(line)}</w:t></w:r>' if line else "<w:r/>"
            )
            out.append(f'<w:p><w:pPr><w:pStyle w:val="Code"/></w:pPr>{run}</w:p>')
        return "".join(out)

    def _image(self, block: ImageBlock) -> str:
        path = block.resolve(self.book.root)
        if path is None:
            self.warnings.append(f"画像が見つかりません: {block.src}")
            return _para(_runs_text(f"[画像が見つかりません: {block.src}]"), style="Caption")
        rel = self._image_rel(path)
        if rel is None:
            return _para(_runs_text(f"[画像を埋め込めません: {block.src}]"), style="Caption")
        rid, info = rel

        m = self.layout.margins
        content_mm = self.layout.width_mm - m.inside_mm - m.outside_mm - m.gutter_mm
        cx, cy = info.emu_for_width_mm(max(20.0, content_mm))
        self._drawing_id += 1
        name = escape(path.name)
        drawing = (
            "<w:r><w:drawing>"
            f'<wp:inline distT="0" distB="0" distL="0" distR="0">'
            f'<wp:extent cx="{cx}" cy="{cy}"/>'
            f'<wp:docPr id="{self._drawing_id}" name={quoteattr(path.stem)} '
            f'descr={quoteattr(block.caption)}/>'
            "<a:graphic><a:graphicData "
            'uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            "<pic:pic>"
            f'<pic:nvPicPr><pic:cNvPr id="{self._drawing_id}" name="{name}"/>'
            "<pic:cNvPicPr/></pic:nvPicPr>"
            f'<pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
            "<pic:spPr><a:xfrm><a:off x=\"0\" y=\"0\"/>"
            f'<a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
            '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
            "</pic:pic></a:graphicData></a:graphic>"
            "</wp:inline></w:drawing></w:r>"
        )
        out = [_para(drawing, style="Figure")]
        if block.caption:
            out.append(_para(_runs_text(block.caption), style="Caption"))
        return "".join(out)

    # -------------------------------------------------------------------- ラン
    def _runs(self, inlines: list[Inline], *, rpr: str = "") -> str:
        out: list[str] = []
        for node in inlines:
            if isinstance(node, Text):
                out.append(_run(node.value, rpr))
            elif isinstance(node, Strong):
                out.append(self._runs(node.children, rpr=rpr + "<w:b/>"))
            elif isinstance(node, Emph):
                out.append(self._runs(node.children, rpr=rpr + "<w:i/>"))
            elif isinstance(node, CodeSpan):
                code_rpr = (
                    '<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas" w:eastAsia="ＭＳ ゴシック"/>'
                )
                out.append(_run(node.value, rpr + code_rpr))
            elif isinstance(node, Link):
                out.append(self._link(node, rpr))
            elif isinstance(node, Ruby):
                out.append(self._ruby(node, rpr))
        return "".join(out)

    def _link(self, node: Link, rpr: str) -> str:
        inner = self._runs(node.children, rpr=rpr + '<w:rStyle w:val="Hyperlink"/>')
        if node.href.startswith("#"):
            return f'<w:hyperlink w:anchor={quoteattr(node.href[1:])}>{inner}</w:hyperlink>'
        rid = self._add_rel(f"{REL_BASE}/hyperlink", node.href, external=True)
        return f'<w:hyperlink r:id="{rid}">{inner}</w:hyperlink>'

    def _ruby(self, node: Ruby, rpr: str) -> str:
        sz = _half_points(self.layout.base_font_pt)
        hps = max(6, int(round(sz * 0.5)))
        raise_ = max(hps, int(round(sz * 0.95)))
        rt_rpr = f'{rpr}<w:sz w:val="{hps}"/><w:szCs w:val="{hps}"/>'
        return (
            "<w:r><w:ruby>"
            "<w:rubyPr>"
            '<w:rubyAlign w:val="distributeSpace"/>'
            f'<w:hps w:val="{hps}"/><w:hpsRaise w:val="{raise_}"/><w:hpsBaseText w:val="{sz}"/>'
            f'<w:lid w:val="{"ja-JP" if self.book.language == "ja" else "en-US"}"/>'
            "</w:rubyPr>"
            f"<w:rt>{_run(node.ruby, rt_rpr)}</w:rt>"
            f"<w:rubyBase>{_run(node.base, rpr)}</w:rubyBase>"
            "</w:ruby></w:r>"
        )


# ------------------------------------------------------------------------ 補助関数


def _bookmark_name(index: int) -> str:
    return f"_Toc{index:05d}"


def _half_points(pt: float) -> int:
    return max(2, int(round(pt * 2)))


def _scale(sz: int, factor: float) -> int:
    return max(2, int(round(sz * factor)))


def _fonts(name: str) -> str:
    n = quoteattr(name)
    return f"<w:rFonts w:ascii={n} w:hAnsi={n} w:eastAsia={n} w:cs={n} w:hint=\"eastAsia\"/>"


def _first_line_indent(layout: LayoutConfig, sz: int) -> str:
    chars = layout.first_line_indent_chars
    if chars <= 0:
        return ""
    twips = int(round(chars * sz / 2 * 20))
    return f'<w:ind w:firstLineChars="{int(round(chars * 100))}" w:firstLine="{twips}"/>'


def _run(text: str, rpr: str = "") -> str:
    if not text:
        return ""
    rpr_xml = f"<w:rPr>{rpr}</w:rPr>" if rpr else ""
    return f'<w:r>{rpr_xml}<w:t xml:space="preserve">{escape(text)}</w:t></w:r>'


def _runs_text(text: str, rpr: str = "") -> str:
    return _run(text, rpr)


def _para(
    inner: str,
    *,
    style: str | None = None,
    page_break_before: bool | None = None,
    jc: str | None = None,
) -> str:
    ppr_parts: list[str] = []
    if style:
        ppr_parts.append(f'<w:pStyle w:val="{style}"/>')
    if page_break_before is True:
        ppr_parts.append("<w:pageBreakBefore/>")
    elif page_break_before is False:
        ppr_parts.append('<w:pageBreakBefore w:val="0"/>')
    if jc:
        ppr_parts.append(f'<w:jc w:val="{jc}"/>')
    ppr = f"<w:pPr>{''.join(ppr_parts)}</w:pPr>" if ppr_parts else ""
    return f"<w:p>{ppr}{inner}</w:p>"
