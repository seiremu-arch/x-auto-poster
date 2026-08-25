"""中間表現から KDP 入稿用の EPUB3 を生成する。

KDPはEPUBを推奨形式にしているため、docxと同じ原稿から同じ目次構造の
EPUBを出せるようにしてある。生成物の構成は次のとおり。

* ``mimetype`` (無圧縮・先頭エントリ) / ``META-INF/container.xml``
* ``OEBPS/package.opf`` (メタデータ・マニフェスト・spine)
* ``OEBPS/nav.xhtml`` (EPUB3のナビゲーション目次) と ``OEBPS/toc.ncx`` (EPUB2互換)
* 章ごとの ``OEBPS/text/chNNN.xhtml``
"""

from __future__ import annotations

import datetime as _dt
import uuid
import zipfile
from dataclasses import dataclass, field
from html import escape as _html_escape
from pathlib import Path

from .config import BookConfig
from .images import ImageError, mime_for, probe
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

XML_DECL = '<?xml version="1.0" encoding="UTF-8"?>\n'
#: 同じ本を作り直しても identifier が変わらないように固定の名前空間を使う
UUID_NAMESPACE = uuid.UUID("6f9d3a2e-0f2a-5a7f-9c62-0f7a9a1d4b11")

DEFAULT_CSS = """@charset "utf-8";

html { -epub-hyphens: auto; }

body {
  margin: 0 5%;
  line-height: 1.8;
  text-align: justify;
  font-family: serif;
}

h1, h2, h3 {
  font-family: sans-serif;
  line-height: 1.4;
  text-align: left;
  page-break-after: avoid;
  -webkit-column-break-after: avoid;
}

h1 {
  font-size: 1.6em;
  margin: 2em 0 1.4em;
  page-break-before: always;
}

h2 { font-size: 1.25em; margin: 2em 0 0.8em; }
h3 { font-size: 1.1em; margin: 1.6em 0 0.6em; }

p {
  margin: 0;
  text-indent: 1em;
}

p.noindent, .titlepage p, .colophon p, figcaption, .scene-break {
  text-indent: 0;
}

.titlepage { text-align: center; margin-top: 25%; }
.titlepage .title { font-size: 1.8em; font-weight: bold; margin-bottom: 0.6em; }
.titlepage .subtitle { font-size: 1.1em; margin-bottom: 2.4em; }
.titlepage .author { font-size: 1.1em; }

.scene-break { text-align: center; margin: 1.6em 0; }

blockquote {
  margin: 1.2em 1.5em;
  padding-left: 0.6em;
  border-left: 3px solid #ccc;
  font-style: italic;
}

pre {
  font-family: monospace;
  font-size: 0.85em;
  line-height: 1.5;
  background: #f4f4f4;
  padding: 0.6em;
  white-space: pre-wrap;
  word-wrap: break-word;
  text-indent: 0;
}

code { font-family: monospace; font-size: 0.9em; }

figure { margin: 1.6em 0; text-align: center; page-break-inside: avoid; }
figure img { max-width: 100%; height: auto; }
figcaption { font-size: 0.85em; color: #444; margin-top: 0.4em; }

ul, ol { margin: 0.8em 0 0.8em 1.4em; padding: 0; }
li { margin-bottom: 0.3em; text-indent: 0; }

nav#toc ol { list-style: none; margin-left: 0; padding-left: 0; }
nav#toc ol ol { margin-left: 1.2em; }
nav#toc li { margin-bottom: 0.5em; }

.colophon { margin-top: 3em; font-size: 0.9em; line-height: 1.9; }

rt { font-size: 0.5em; }
"""


@dataclass
class EpubResult:
    path: Path
    warnings: list[str] = field(default_factory=list)


def build_epub(book: BookConfig, document: Document, out_path: str | Path) -> EpubResult:
    return _EpubWriter(book, document).write(Path(out_path))


class _EpubWriter:
    def __init__(self, book: BookConfig, document: Document) -> None:
        self.book = book
        self.doc = document
        self.warnings: list[str] = []
        self._images: dict[str, str] = {}  # 実パス -> OEBPS内の相対パス
        self._image_files: list[tuple[str, Path]] = []
        self._chapter_files: list[tuple[Chapter, str]] = []

    # ------------------------------------------------------------------ 出力本体
    def write(self, out_path: Path) -> EpubResult:
        out_path.parent.mkdir(parents=True, exist_ok=True)

        for i, chapter in enumerate(self.doc.chapters, start=1):
            self._chapter_files.append((chapter, f"text/ch{i:03d}.xhtml"))

        cover_href = self._register_cover()
        chapter_docs = [
            (href, self._chapter_xhtml(chapter)) for chapter, href in self._chapter_files
        ]
        extra_docs: list[tuple[str, str]] = []
        if cover_href:
            extra_docs.append(("text/cover.xhtml", self._cover_xhtml(cover_href)))
        if self.book.frontmatter.title_page:
            extra_docs.append(("text/titlepage.xhtml", self._title_page_xhtml()))
        if self.book.frontmatter.colophon:
            extra_docs.append(("text/colophon.xhtml", self._colophon_xhtml()))

        spine = [href for href, _ in extra_docs if href != "text/colophon.xhtml"]
        spine += ["nav.xhtml"]
        spine += [href for _, href in self._chapter_files]
        if self.book.frontmatter.colophon:
            spine.append("text/colophon.xhtml")

        opf = self._package_opf(spine, cover_href, [h for h, _ in extra_docs])

        with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zf:
            # mimetype は無圧縮で最初に入れる(EPUB仕様)
            zf.writestr(
                zipfile.ZipInfo("mimetype"), "application/epub+zip", zipfile.ZIP_STORED
            )
            zf.writestr("META-INF/container.xml", _CONTAINER_XML)
            zf.writestr("OEBPS/package.opf", opf)
            zf.writestr("OEBPS/nav.xhtml", self._nav_xhtml())
            zf.writestr("OEBPS/toc.ncx", self._ncx())
            zf.writestr("OEBPS/css/book.css", DEFAULT_CSS)
            for href, content in extra_docs + chapter_docs:
                zf.writestr(f"OEBPS/{href}", content)
            for href, src in self._image_files:
                zf.write(src, f"OEBPS/{href}")
        return EpubResult(out_path, self.warnings)

    # ------------------------------------------------------------------ メタデータ
    @property
    def identifier(self) -> str:
        if self.book.isbn:
            return f"urn:isbn:{self.book.isbn.replace('-', '')}"
        return f"urn:uuid:{uuid.uuid5(UUID_NAMESPACE, self.book.slug)}"

    def _package_opf(self, spine: list[str], cover_href: str | None, extra: list[str]) -> str:
        b = self.book
        modified = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        meta = [
            f'<dc:identifier id="bookid">{_e(self.identifier)}</dc:identifier>',
            f'<dc:title id="title">{_e(b.title)}</dc:title>',
            f"<dc:language>{_e(b.language)}</dc:language>",
            f'<dc:creator id="creator">{_e(b.author)}</dc:creator>',
            '<meta refines="#creator" property="role" scheme="marc:relators">aut</meta>',
            f'<meta property="dcterms:modified">{modified}</meta>',
        ]
        if b.subtitle:
            meta.append('<meta refines="#title" property="title-type">main</meta>')
            meta.append(f'<dc:title id="subtitle">{_e(b.subtitle)}</dc:title>')
            meta.append('<meta refines="#subtitle" property="title-type">subtitle</meta>')
        if b.publisher:
            meta.append(f"<dc:publisher>{_e(b.publisher)}</dc:publisher>")
        if b.description:
            meta.append(f"<dc:description>{_e(b.description)}</dc:description>")
        if b.published:
            meta.append(f"<dc:date>{_e(b.published)}</dc:date>")
        meta.append(f"<dc:rights>{_e(b.copyright_line)}</dc:rights>")
        for kw in b.keywords:
            meta.append(f"<dc:subject>{_e(kw)}</dc:subject>")
        if cover_href:
            meta.append('<meta name="cover" content="cover-image"/>')

        manifest = [
            '<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>',
            '<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>',
            '<item id="css" href="css/book.css" media-type="text/css"/>',
        ]
        for href in extra:
            ident = href.replace("/", "-").replace(".xhtml", "")
            manifest.append(
                f'<item id="{_e(ident)}" href="{_e(href)}" media-type="application/xhtml+xml"/>'
            )
        for i, (_chapter, href) in enumerate(self._chapter_files, start=1):
            manifest.append(
                f'<item id="ch{i:03d}" href="{_e(href)}" media-type="application/xhtml+xml"/>'
            )
        for idx, (href, src) in enumerate(self._image_files, start=1):
            props = ' properties="cover-image"' if href == cover_href else ""
            ident = "cover-image" if href == cover_href else f"img{idx:03d}"
            manifest.append(
                f'<item id="{ident}" href="{_e(href)}" media-type="{mime_for(src)}"{props}/>'
            )

        spine_items = []
        for href in spine:
            if href == "nav.xhtml":
                spine_items.append('<itemref idref="nav"/>')
            else:
                ident = next(
                    (f"ch{i:03d}" for i, (_c, h) in enumerate(self._chapter_files, 1) if h == href),
                    href.replace("/", "-").replace(".xhtml", ""),
                )
                spine_items.append(f'<itemref idref="{_e(ident)}"/>')

        return (
            f"{XML_DECL}"
            '<package xmlns="http://www.idpf.org/2007/opf" version="3.0" '
            f'unique-identifier="bookid" xml:lang="{_e(self.book.language)}">'
            '<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">'
            f'{"".join(meta)}</metadata>'
            f'<manifest>{"".join(manifest)}</manifest>'
            f'<spine toc="ncx">{"".join(spine_items)}</spine>'
            "</package>"
        )

    def _register_cover(self) -> str | None:
        path = self.book.cover_path()
        if not path:
            return None
        if not path.is_file():
            self.warnings.append(f"表紙画像が見つかりません: {self.book.cover}")
            return None
        return self._register_image(path)

    def _register_image(self, path: Path) -> str:
        key = str(path.resolve())
        if key not in self._images:
            href = f"images/{len(self._images) + 1:03d}{path.suffix.lower()}"
            self._images[key] = href
            self._image_files.append((href, path))
        return self._images[key]

    # ------------------------------------------------------------------- 目次まわり
    def _toc_entries(self) -> list[tuple[int, str, str]]:
        """(レベル, 表示テキスト, リンク先) の並びを返す。"""
        depth = max(self.book.ebook.toc.depth, 1)
        entries: list[tuple[int, str, str]] = []
        for chapter, href in self._chapter_files:
            if not chapter.in_toc:
                continue
            for heading in chapter.headings:
                if heading.level > depth or not heading.in_toc:
                    continue
                entries.append((heading.level, heading.text, f"{href}#h{heading.index}"))
        return entries

    def _nav_xhtml(self) -> str:
        tree = _nest(self._toc_entries())
        toc_body = (
            f'<nav epub:type="toc" id="toc"><h1>{_e(self.book.ebook.toc.title)}</h1>'
            f"{_render_nav(tree)}</nav>"
        )
        if self._chapter_files:
            toc_body += (
                '<nav epub:type="landmarks" hidden="hidden"><ol>'
                f'<li><a epub:type="bodymatter" href="{_e(self._chapter_files[0][1])}">本文</a></li>'
                "</ol></nav>"
            )
        return _xhtml(self.book, self.book.ebook.toc.title, toc_body, epub_ns=True, depth=0)

    def _ncx(self) -> str:
        points = []
        for i, (level, text, href) in enumerate(self._toc_entries(), start=1):
            points.append(
                f'<navPoint id="np{i}" playOrder="{i}">'
                f"<navLabel><text>{_e(text)}</text></navLabel>"
                f'<content src="{_e(href)}"/></navPoint>'
            )
        return (
            f"{XML_DECL}"
            '<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">'
            f'<head><meta name="dtb:uid" content="{_e(self.identifier)}"/>'
            '<meta name="dtb:depth" content="2"/>'
            '<meta name="dtb:totalPageCount" content="0"/>'
            '<meta name="dtb:maxPageNumber" content="0"/></head>'
            f"<docTitle><text>{_e(self.book.title)}</text></docTitle>"
            f'<navMap>{"".join(points)}</navMap></ncx>'
        )

    # -------------------------------------------------------------------- ページ
    def _cover_xhtml(self, cover_href: str) -> str:
        body = (
            '<div style="text-align:center;margin:0;padding:0">'
            f'<img src="../{_e(cover_href)}" alt="{_e(self.book.title)}" '
            'style="max-width:100%;height:auto"/></div>'
        )
        return _xhtml(self.book, self.book.title, body)

    def _title_page_xhtml(self) -> str:
        b = self.book
        parts = [f'<p class="title">{_e(b.title)}</p>']
        if b.subtitle:
            parts.append(f'<p class="subtitle">{_e(b.subtitle)}</p>')
        parts.append(f'<p class="author">{_e(b.author)}</p>')
        if b.publisher:
            parts.append(f"<p>{_e(b.publisher)}</p>")
        return _xhtml(b, b.title, f'<div class="titlepage">{"".join(parts)}</div>')

    def _colophon_xhtml(self) -> str:
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
        body = "<h1>奥付</h1>" + '<div class="colophon">' + "".join(
            f"<p>{_e(line)}</p>" for line in lines
        ) + "</div>"
        return _xhtml(b, "奥付", body)

    def _chapter_xhtml(self, chapter: Chapter) -> str:
        body = "".join(self._block(b) for b in chapter.blocks)
        return _xhtml(self.book, chapter.title, body)

    # ------------------------------------------------------------------ ブロック
    def _block(self, block: Block) -> str:
        if isinstance(block, Heading):
            tag = f"h{min(3, block.level)}"
            return f'<{tag} id="h{block.index}">{self._inline(block.inlines)}</{tag}>'
        if isinstance(block, Paragraph):
            return f"<p>{self._inline(block.inlines)}</p>"
        if isinstance(block, ListBlock):
            tag = "ol" if block.ordered else "ul"
            out = [f"<{tag}>"]
            level = 0
            for item in block.items:
                while level < item.level:
                    out.append(f"<{tag}>")
                    level += 1
                while level > item.level:
                    out.append(f"</{tag}>")
                    level -= 1
                out.append(f"<li>{self._inline(item.inlines)}</li>")
            while level > 0:
                out.append(f"</{tag}>")
                level -= 1
            out.append(f"</{tag}>")
            return "".join(out)
        if isinstance(block, Quote):
            inner = "".join(f"<p>{self._inline(p)}</p>" for p in block.paragraphs)
            return f"<blockquote>{inner}</blockquote>"
        if isinstance(block, CodeBlock):
            cls = f' class="language-{_e(block.lang)}"' if block.lang else ""
            return f"<pre><code{cls}>{_e(block.text)}</code></pre>"
        if isinstance(block, ImageBlock):
            return self._image(block)
        if isinstance(block, SceneBreak):
            return '<p class="scene-break">＊　＊　＊</p>'
        if isinstance(block, PageBreak):
            return '<div style="page-break-after:always"></div>'
        return ""

    def _image(self, block: ImageBlock) -> str:
        path = block.resolve(self.book.root)
        if path is None:
            self.warnings.append(f"画像が見つかりません: {block.src}")
            return f'<p class="noindent">[画像が見つかりません: {_e(block.src)}]</p>'
        try:
            probe(path)
        except (OSError, ImageError) as exc:
            self.warnings.append(str(exc))
        href = self._register_image(path)
        caption = f"<figcaption>{_e(block.caption)}</figcaption>" if block.caption else ""
        return (
            f'<figure><img src="../{_e(href)}" alt="{_e(block.caption)}"/>{caption}</figure>'
        )

    # -------------------------------------------------------------------- インライン
    def _inline(self, nodes: list[Inline]) -> str:
        out: list[str] = []
        for n in nodes:
            if isinstance(n, Text):
                out.append(_e(n.value))
            elif isinstance(n, Strong):
                out.append(f"<strong>{self._inline(n.children)}</strong>")
            elif isinstance(n, Emph):
                out.append(f"<em>{self._inline(n.children)}</em>")
            elif isinstance(n, CodeSpan):
                out.append(f"<code>{_e(n.value)}</code>")
            elif isinstance(n, Link):
                out.append(f'<a href="{_e(n.href)}">{self._inline(n.children)}</a>')
            elif isinstance(n, Ruby):
                out.append(
                    f"<ruby>{_e(n.base)}<rp>(</rp><rt>{_e(n.ruby)}</rt><rp>)</rp></ruby>"
                )
        return "".join(out)


# ------------------------------------------------------------------------ 補助関数

_CONTAINER_XML = (
    f"{XML_DECL}"
    '<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
    "<rootfiles>"
    '<rootfile full-path="OEBPS/package.opf" media-type="application/oebps-package+xml"/>'
    "</rootfiles></container>"
)


def _nest(entries: list[tuple[int, str, str]]) -> list[dict]:
    """(レベル, テキスト, リンク) の平坦な並びを入れ子の木にする。"""
    root: list[dict] = []
    stack: list[list[dict]] = [root]
    levels: list[int] = []
    for level, text, href in entries:
        while levels and levels[-1] >= level:
            levels.pop()
            stack.pop()
        node = {"text": text, "href": href, "children": []}
        stack[-1].append(node)
        stack.append(node["children"])
        levels.append(level)
    return root


def _render_nav(nodes: list[dict]) -> str:
    if not nodes:
        return ""
    items = []
    for n in nodes:
        child = _render_nav(n["children"])
        items.append(f'<li><a href="{_e(n["href"])}">{_e(n["text"])}</a>{child}</li>')
    return f"<ol>{''.join(items)}</ol>"


def _e(text: str) -> str:
    return _html_escape(str(text), quote=True)


def _xhtml(
    book: BookConfig,
    title: str,
    body: str,
    *,
    epub_ns: bool = False,
    depth: int = 1,
) -> str:
    ns = ' xmlns:epub="http://www.idpf.org/2007/ops"' if epub_ns else ""
    css = "../css/book.css" if depth else "css/book.css"
    return (
        f"{XML_DECL}"
        '<!DOCTYPE html>\n'
        f'<html xmlns="http://www.w3.org/1999/xhtml"{ns} xml:lang="{_e(book.language)}" '
        f'lang="{_e(book.language)}">'
        f"<head><meta charset=\"utf-8\"/><title>{_e(title)}</title>"
        f'<link rel="stylesheet" type="text/css" href="{css}"/></head>'
        f"<body>{body}</body></html>"
    )
