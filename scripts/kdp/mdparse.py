"""原稿Markdownを、docx/EPUB両方から使える中間表現に変換する。

汎用のMarkdown処理系ではなく「書籍原稿として使う範囲」に絞った実装。
サポートするのは以下。

* 見出し ``#`` ～ ``###``(``#`` が章の切れ目になる)
* 段落、箇条書き(``-`` / ``1.``、2段階までのネスト)、引用 ``>``
* コードブロック(``` フェンス)
* 画像 ``![キャプション](path)``(単独行のとき図として扱う)
* 区切り ``---``(シーン区切り)、``<!-- pagebreak -->``(強制改ページ)
* 強調 ``**太字**`` / ``*斜体*``、``` `コード` ```、``[リンク](url)``
* ルビ ``｜漢字《かんじ》``(青空文庫記法。``｜`` は省略可)

各ファイルの先頭には任意でYAMLフロントマターを置ける(``title`` / ``toc`` /
``type`` / ``page_break``)。
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Sequence

import yaml

# --------------------------------------------------------------------- インライン


@dataclass
class Text:
    value: str


@dataclass
class Strong:
    children: list["Inline"]


@dataclass
class Emph:
    children: list["Inline"]


@dataclass
class CodeSpan:
    value: str


@dataclass
class Link:
    href: str
    children: list["Inline"]


@dataclass
class Ruby:
    base: str
    ruby: str


Inline = Text | Strong | Emph | CodeSpan | Link | Ruby


# ------------------------------------------------------------------------ ブロック


@dataclass
class Heading:
    level: int
    inlines: list[Inline]
    text: str
    #: 文書全体での通し番号(目次のアンカー生成に使う)
    index: int = 0
    in_toc: bool = True


@dataclass
class Paragraph:
    inlines: list[Inline]


@dataclass
class ListItem:
    level: int
    inlines: list[Inline]


@dataclass
class ListBlock:
    ordered: bool
    items: list[ListItem]


@dataclass
class Quote:
    paragraphs: list[list[Inline]]


@dataclass
class CodeBlock:
    lang: str
    text: str


@dataclass
class ImageBlock:
    src: str
    caption: str
    #: この画像を含む原稿ファイルのあるディレクトリ(相対パスの起点)
    base_dir: Path | None = None

    def resolve(self, book_root: Path) -> Path | None:
        """原稿ファイル基準 → 本のルート基準の順に実ファイルを探す。"""
        for base in (self.base_dir, book_root):
            if base is None:
                continue
            candidate = (base / self.src).resolve()
            if candidate.is_file():
                return candidate
        return None


@dataclass
class SceneBreak:
    pass


@dataclass
class PageBreak:
    pass


Block = Heading | Paragraph | ListBlock | Quote | CodeBlock | ImageBlock | SceneBreak | PageBreak


@dataclass
class Chapter:
    """原稿ファイル1つ分。``#`` 見出しがそのまま章タイトルになる。"""

    source: Path
    title: str
    blocks: list[Block]
    meta: dict[str, Any] = field(default_factory=dict)
    #: front(前付) / body(本文) / back(後付)
    kind: str = "body"
    in_toc: bool = True
    page_break: bool = True

    @property
    def headings(self) -> list[Heading]:
        return [b for b in self.blocks if isinstance(b, Heading)]

    def word_count(self) -> int:
        return sum(_block_char_count(b) for b in self.blocks)


@dataclass
class Document:
    chapters: list[Chapter]

    def headings(self, max_level: int = 3) -> list[tuple[Chapter, Heading]]:
        out: list[tuple[Chapter, Heading]] = []
        for ch in self.chapters:
            if not ch.in_toc:
                continue
            for h in ch.headings:
                if h.level <= max_level and h.in_toc:
                    out.append((ch, h))
        return out

    def images(self) -> list[ImageBlock]:
        return [b for ch in self.chapters for b in ch.blocks if isinstance(b, ImageBlock)]

    def char_count(self) -> int:
        return sum(ch.word_count() for ch in self.chapters)


# ------------------------------------------------------------------ インラインの解析

_ESCAPE_RE = re.compile(r"\\(.)")
_KANJI = r"一-鿿々〆ヶヵ"

_INLINE_RE = re.compile(
    r"(?P<escape>\\.)"
    r"|`(?P<code>[^`]+)`"
    r"|!\[(?P<img_alt>[^\]]*)\]\((?P<img_src>[^)\s]+)\)"
    r"|\[(?P<link_text>[^\]]*)\]\((?P<link_href>[^)\s]+)\)"
    r"|\*\*(?P<strong>(?:[^*]|\*(?!\*))+)\*\*"
    r"|\*(?P<emph>[^*\s](?:[^*]*[^*\s])?)\*"
    r"|[｜|](?P<rb_base>[^《]{1,30})《(?P<rb_ruby>[^》]{1,30})》"
    r"|(?P<rb_auto_base>[" + _KANJI + r"]{1,20})《(?P<rb_auto_ruby>[^》]{1,30})》"
)


def parse_inline(text: str) -> list[Inline]:
    """1行分(改行を含まない)のインライン記法を解析する。"""
    nodes: list[Inline] = []
    pos = 0
    for m in _INLINE_RE.finditer(text):
        if m.start() > pos:
            _push_text(nodes, text[pos : m.start()])
        pos = m.end()
        if m.group("escape"):
            _push_text(nodes, m.group("escape")[1:], raw=True)
        elif m.group("code") is not None:
            nodes.append(CodeSpan(m.group("code")))
        elif m.group("img_src") is not None:
            # 段落中の画像はリンクテキストとして扱う(図は単独行で書く運用)
            _push_text(nodes, m.group("img_alt") or "")
        elif m.group("link_href") is not None:
            nodes.append(Link(m.group("link_href"), parse_inline(m.group("link_text"))))
        elif m.group("strong") is not None:
            nodes.append(Strong(parse_inline(m.group("strong"))))
        elif m.group("emph") is not None:
            nodes.append(Emph(parse_inline(m.group("emph"))))
        elif m.group("rb_base") is not None:
            nodes.append(Ruby(_unescape(m.group("rb_base")), m.group("rb_ruby")))
        else:
            nodes.append(Ruby(m.group("rb_auto_base"), m.group("rb_auto_ruby")))
    if pos < len(text):
        _push_text(nodes, text[pos:])
    return nodes


def _push_text(nodes: list[Inline], value: str, *, raw: bool = False) -> None:
    if not value:
        return
    if not raw:
        value = _unescape(value)
    if nodes and isinstance(nodes[-1], Text):
        nodes[-1].value += value
    else:
        nodes.append(Text(value))


def _unescape(text: str) -> str:
    return _ESCAPE_RE.sub(r"\1", text)


def inline_to_text(nodes: Iterable[Inline]) -> str:
    """見出しテキストや文字数カウント用に、装飾を落としたプレーンテキストを返す。"""
    parts: list[str] = []
    for n in nodes:
        if isinstance(n, Text):
            parts.append(n.value)
        elif isinstance(n, CodeSpan):
            parts.append(n.value)
        elif isinstance(n, Ruby):
            parts.append(n.base)
        elif isinstance(n, (Strong, Emph, Link)):
            parts.append(inline_to_text(n.children))
    return "".join(parts)


# -------------------------------------------------------------------- ブロックの解析

_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*$")
_BULLET_RE = re.compile(r"^(\s*)[-*+]\s+(.*)$")
_ORDERED_RE = re.compile(r"^(\s*)\d+[.)]\s+(.*)$")
_FENCE_RE = re.compile(r"^\s*(?P<fence>`{3,}|~{3,})\s*(?P<lang>[\w+-]*)\s*$")
_RULE_RE = re.compile(r"^\s*(?:-{3,}|\*{3,}|\*(?:\s+\*){2,})\s*$")
_IMAGE_RE = re.compile(r"^!\[(?P<caption>[^\]]*)\]\((?P<src>[^)\s]+)\)\s*$")
_PAGEBREAK_RE = re.compile(r"^\s*<!--\s*(?:pagebreak|改ページ)\s*-->\s*$", re.IGNORECASE)
_COMMENT_RE = re.compile(r"^\s*<!--.*-->\s*$")


def parse_file(path: str | Path) -> Chapter:
    """Markdownファイル1つを Chapter に変換する。"""
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    meta, body = _split_front_matter(text)
    blocks = parse_blocks(body)
    for block in blocks:
        if isinstance(block, ImageBlock):
            block.base_dir = p.parent

    title = str(meta.get("title") or "").strip()
    if not title:
        for b in blocks:
            if isinstance(b, Heading) and b.level == 1:
                title = b.text
                break
    if not title:
        title = p.stem

    kind = str(meta.get("type") or "body").strip().lower()
    if kind not in ("front", "body", "back"):
        kind = "body"

    in_toc = meta.get("toc", True)
    in_toc = bool(in_toc) if isinstance(in_toc, bool) else str(in_toc).lower() != "false"
    page_break = meta.get("page_break", True)
    page_break = (
        bool(page_break) if isinstance(page_break, bool) else str(page_break).lower() != "false"
    )

    return Chapter(
        source=p,
        title=title,
        blocks=blocks,
        meta=meta,
        kind=kind,
        in_toc=in_toc,
        page_break=page_break,
    )


def parse_manuscript(paths: Sequence[str | Path]) -> Document:
    """原稿ファイル群をまとめて解析し、見出しに通し番号を振る。"""
    chapters = [parse_file(p) for p in paths]
    counter = 0
    for ch in chapters:
        for b in ch.blocks:
            if isinstance(b, Heading):
                counter += 1
                b.index = counter
                if not ch.in_toc:
                    b.in_toc = False
    return Document(chapters)


def _split_front_matter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---"):
        return {}, text
    lines = text.splitlines()
    if lines[0].strip() != "---":
        return {}, text
    for i in range(1, len(lines)):
        if lines[i].strip() in ("---", "..."):
            raw = "\n".join(lines[1:i])
            try:
                meta = yaml.safe_load(raw) or {}
            except yaml.YAMLError:
                return {}, text
            if not isinstance(meta, dict):
                return {}, text
            return meta, "\n".join(lines[i + 1 :])
    return {}, text


def parse_blocks(text: str) -> list[Block]:
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    blocks: list[Block] = []
    para: list[str] = []
    i = 0

    def flush_para() -> None:
        if para:
            joined = "".join(para) if _is_cjk_wrap(para) else " ".join(para)
            blocks.append(Paragraph(parse_inline(joined.strip())))
            para.clear()

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            flush_para()
            i += 1
            continue

        fence = _FENCE_RE.match(line)
        if fence:
            flush_para()
            marker = fence.group("fence")[0]
            body: list[str] = []
            i += 1
            while i < len(lines) and not re.match(rf"^\s*{marker}{{3,}}\s*$", lines[i]):
                body.append(lines[i])
                i += 1
            i += 1
            blocks.append(CodeBlock(fence.group("lang"), "\n".join(body)))
            continue

        if _PAGEBREAK_RE.match(line):
            flush_para()
            blocks.append(PageBreak())
            i += 1
            continue

        if _COMMENT_RE.match(line):
            i += 1
            continue

        heading = _HEADING_RE.match(stripped)
        if heading:
            flush_para()
            level = min(3, len(heading.group(1)))
            inlines = parse_inline(heading.group(2))
            blocks.append(Heading(level, inlines, inline_to_text(inlines)))
            i += 1
            continue

        if _RULE_RE.match(line):
            flush_para()
            blocks.append(SceneBreak())
            i += 1
            continue

        image = _IMAGE_RE.match(stripped)
        if image:
            flush_para()
            blocks.append(ImageBlock(image.group("src"), image.group("caption")))
            i += 1
            continue

        if stripped.startswith(">"):
            flush_para()
            quote_lines: list[str] = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote_lines.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            paragraphs: list[list[Inline]] = []
            buf: list[str] = []
            for q in quote_lines:
                if q.strip():
                    buf.append(q.strip())
                elif buf:
                    paragraphs.append(parse_inline("".join(buf) if _is_cjk_wrap(buf) else " ".join(buf)))
                    buf = []
            if buf:
                paragraphs.append(parse_inline("".join(buf) if _is_cjk_wrap(buf) else " ".join(buf)))
            blocks.append(Quote(paragraphs))
            continue

        if _BULLET_RE.match(line) or _ORDERED_RE.match(line):
            flush_para()
            ordered = bool(_ORDERED_RE.match(line))
            items: list[ListItem] = []
            while i < len(lines):
                m = _ORDERED_RE.match(lines[i]) if ordered else _BULLET_RE.match(lines[i])
                if not m:
                    other = _BULLET_RE.match(lines[i]) if ordered else _ORDERED_RE.match(lines[i])
                    if other or not lines[i].strip():
                        break
                    # 継続行(インデントされた続き)は直前の項目にぶら下げる
                    if items and lines[i].startswith((" ", "\t")):
                        items[-1].inlines.extend(parse_inline(" " + lines[i].strip()))
                        i += 1
                        continue
                    break
                indent = len(m.group(1).replace("\t", "  "))
                items.append(ListItem(min(2, indent // 2), parse_inline(m.group(2).strip())))
                i += 1
            blocks.append(ListBlock(ordered, items))
            continue

        para.append(stripped)
        i += 1

    flush_para()
    return blocks


def _is_cjk_wrap(lines: Sequence[str]) -> bool:
    """日本語原稿なら行を連結するときに空白を入れない。"""
    joined = "".join(lines)
    cjk = sum(1 for c in joined if "　" <= c <= "鿿" or "＀" <= c <= "￯")
    return cjk * 2 >= len(joined) if joined else False


def _block_char_count(block: Block) -> int:
    if isinstance(block, Heading):
        return len(block.text)
    if isinstance(block, Paragraph):
        return len(inline_to_text(block.inlines))
    if isinstance(block, ListBlock):
        return sum(len(inline_to_text(it.inlines)) for it in block.items)
    if isinstance(block, Quote):
        return sum(len(inline_to_text(p)) for p in block.paragraphs)
    if isinstance(block, CodeBlock):
        return len(block.text)
    if isinstance(block, ImageBlock):
        return len(block.caption)
    return 0
