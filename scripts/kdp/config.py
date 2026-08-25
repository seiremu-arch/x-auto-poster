"""book.yaml の読み込みと検証。

1冊分のメタデータ・組版設定・原稿ファイルの並び順をここで確定させる。
以降のビルダ(docx / epub)は BookConfig だけを見れば良いようにする。
"""

from __future__ import annotations

import datetime as _dt
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

import yaml

MM_PER_INCH = 25.4

#: KDPペーパーパックで選べる代表的な判型(幅mm, 高さmm)。
#: 数値を直接 ``{"width_mm": .., "height_mm": ..}`` で書くこともできる。
TRIM_SIZES: dict[str, tuple[float, float]] = {
    "5x8": (127.0, 203.2),
    "5.06x7.81": (128.5, 198.4),
    "5.25x8": (133.4, 203.2),
    "5.5x8.5": (139.7, 215.9),
    "6x9": (152.4, 228.6),
    "6.14x9.21": (156.0, 234.0),
    "7x10": (177.8, 254.0),
    "8x10": (203.2, 254.0),
    "8.5x11": (215.9, 279.4),
    # 日本語書籍でよく使う判型
    "a5": (148.0, 210.0),
    "b6": (128.0, 182.0),
    "shinsho": (105.0, 173.0),
    "shiroku": (127.0, 188.0),
    "bunko": (105.0, 148.0),
    # 日本語表記の別名
    "四六": (127.0, 188.0),
    "新書": (105.0, 173.0),
    "文庫": (105.0, 148.0),
}

TOC_STYLES = ("link", "field", "both", "none")
PROFILES = ("ebook", "print")


class ConfigError(Exception):
    """book.yaml の内容が不正なときに送出する。"""

    def __init__(self, errors: Iterable[str]) -> None:
        self.errors = list(errors)
        super().__init__("\n".join(f"- {e}" for e in self.errors))


def mm_to_twips(mm: float) -> int:
    """ミリメートルを twip(1/1440インチ)に変換する。"""
    return int(round(mm / MM_PER_INCH * 1440))


def _as_str(value: Any, default: str = "") -> str:
    if value is None:
        return default
    if isinstance(value, (_dt.date, _dt.datetime)):
        return value.isoformat()
    return str(value).strip()


def _as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [v.strip() for v in value.split(",") if v.strip()]
    return [_as_str(v) for v in value if _as_str(v)]


def _as_bool(value: Any, default: bool) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    return _as_str(value).lower() in ("1", "true", "yes", "on")


def _as_float(value: Any, default: float) -> float:
    if value is None:
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _as_int(value: Any, default: int) -> int:
    if value is None:
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


@dataclass
class TocConfig:
    """目次(Table of Contents)の生成設定。"""

    title: str = "目次"
    #: 目次に載せる見出しの深さ(1なら大見出しのみ、2なら中見出しまで)
    depth: int = 2
    #: link=リンク付き目次 / field=Wordの目次フィールド(ページ番号付き) / both / none
    style: str = "link"
    page_break_after: bool = True

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None, *, default_style: str) -> "TocConfig":
        data = data or {}
        return cls(
            title=_as_str(data.get("title"), "目次"),
            depth=max(1, min(3, _as_int(data.get("depth"), 2))),
            style=_as_str(data.get("style"), default_style).lower() or default_style,
            page_break_after=_as_bool(data.get("page_break_after"), True),
        )


@dataclass
class Margins:
    top_mm: float = 20.0
    bottom_mm: float = 20.0
    inside_mm: float = 19.0
    outside_mm: float = 13.0
    gutter_mm: float = 0.0

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None, base: "Margins | None" = None) -> "Margins":
        base = base or cls()
        data = data or {}
        return cls(
            top_mm=_as_float(data.get("top"), base.top_mm),
            bottom_mm=_as_float(data.get("bottom"), base.bottom_mm),
            inside_mm=_as_float(data.get("inside"), base.inside_mm),
            outside_mm=_as_float(data.get("outside"), base.outside_mm),
            gutter_mm=_as_float(data.get("gutter"), base.gutter_mm),
        )


@dataclass
class LayoutConfig:
    """プロファイル(ebook / print)ごとの組版設定。"""

    profile: str = "ebook"
    width_mm: float = 152.4
    height_mm: float = 228.6
    margins: Margins = field(default_factory=Margins)
    body_font: str = "游明朝"
    heading_font: str = "游ゴシック"
    base_font_pt: float = 10.5
    line_spacing: float = 1.6
    #: 本文段落の1字下げ(全角字数)。0で無効。
    first_line_indent_chars: float = 1.0
    mirror_margins: bool = False
    page_numbers: bool = False
    toc: TocConfig = field(default_factory=TocConfig)

    @property
    def is_print(self) -> bool:
        return self.profile == "print"


@dataclass
class FrontMatterConfig:
    title_page: bool = True
    #: 権利表記ページ(前付)。日本語書籍は末尾の奥付で済ませることが多いので既定はオフ
    copyright_page: bool = False
    #: 奥付(著者・発行日・発行者)をページ末尾に置く
    colophon: bool = True
    copyright_notice: str = ""
    colophon_note: str = ""


@dataclass
class BookConfig:
    """1冊分の設定。book.yaml の内容そのもの。"""

    root: Path
    slug: str
    title: str
    subtitle: str = ""
    author: str = ""
    publisher: str = ""
    language: str = "ja"
    isbn: str = ""
    published: str = ""
    copyright_year: str = ""
    description: str = ""
    keywords: list[str] = field(default_factory=list)
    categories: list[str] = field(default_factory=list)
    cover: str = ""
    series: str = ""
    manuscript_patterns: list[str] = field(default_factory=lambda: ["manuscript/*.md"])
    frontmatter: FrontMatterConfig = field(default_factory=FrontMatterConfig)
    ebook: LayoutConfig = field(default_factory=LayoutConfig)
    print_: LayoutConfig = field(default_factory=LayoutConfig)
    raw: dict[str, Any] = field(default_factory=dict)

    # ------------------------------------------------------------------ 読み込み
    @classmethod
    def load(cls, path: str | Path) -> "BookConfig":
        """ディレクトリ、または book.yaml のパスから設定を読み込む。"""
        p = Path(path)
        if p.is_dir():
            candidates = [p / "book.yaml", p / "book.yml"]
            for c in candidates:
                if c.is_file():
                    p = c
                    break
            else:
                raise ConfigError([f"{p} に book.yaml が見つかりません"])
        if not p.is_file():
            raise ConfigError([f"設定ファイルが見つかりません: {p}"])

        with p.open(encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}
        if not isinstance(data, dict):
            raise ConfigError([f"{p} のトップレベルはマッピングである必要があります"])
        return cls.from_dict(data, root=p.parent)

    @classmethod
    def from_dict(cls, data: dict[str, Any], *, root: Path) -> "BookConfig":
        errors: list[str] = []

        title = _as_str(data.get("title"))
        if not title:
            errors.append("title は必須です")
        author = _as_str(data.get("author"))
        if not author:
            errors.append("author は必須です")

        slug = _as_str(data.get("slug")) or _slugify(title) or _slugify(root.name) or "book"

        manuscript = data.get("manuscript")
        if isinstance(manuscript, str):
            patterns = [manuscript]
        elif isinstance(manuscript, list) and manuscript:
            patterns = [_as_str(m) for m in manuscript if _as_str(m)]
        else:
            patterns = ["manuscript/*.md"]

        ebook = _layout_from_dict(data.get("ebook"), profile="ebook")
        print_ = _layout_from_dict(data.get("print"), profile="print")

        for layout in (ebook, print_):
            if layout.toc.style not in TOC_STYLES:
                errors.append(
                    f"{layout.profile}.toc.style は {'/'.join(TOC_STYLES)} のいずれかにしてください"
                    f"(現在: {layout.toc.style})"
                )

        fm_data = data.get("frontmatter") or {}
        frontmatter = FrontMatterConfig(
            title_page=_as_bool(fm_data.get("title_page"), True),
            copyright_page=_as_bool(fm_data.get("copyright_page"), False),
            colophon=_as_bool(fm_data.get("colophon"), True),
            copyright_notice=_as_str(fm_data.get("copyright_notice")),
            colophon_note=_as_str(fm_data.get("colophon_note")),
        )

        if errors:
            raise ConfigError(errors)

        published = _as_str(data.get("published"))
        return cls(
            root=root,
            slug=slug,
            title=title,
            subtitle=_as_str(data.get("subtitle")),
            author=author,
            publisher=_as_str(data.get("publisher")),
            language=_as_str(data.get("language"), "ja") or "ja",
            isbn=_as_str(data.get("isbn")),
            published=published,
            copyright_year=_as_str(data.get("copyright_year")) or published[:4],
            description=_as_str(data.get("description")),
            keywords=_as_list(data.get("keywords")),
            categories=_as_list(data.get("categories")),
            cover=_as_str(data.get("cover")),
            series=_as_str(data.get("series")),
            manuscript_patterns=patterns,
            frontmatter=frontmatter,
            ebook=ebook,
            print_=print_,
            raw=data,
        )

    # -------------------------------------------------------------------- 参照系
    def layout(self, profile: str) -> LayoutConfig:
        if profile == "print":
            return self.print_
        if profile == "ebook":
            return self.ebook
        raise ConfigError([f"不明なプロファイル: {profile}(使えるのは {'/'.join(PROFILES)})"])

    def manuscript_files(self) -> list[Path]:
        """book.yaml の manuscript 指定を展開し、原稿ファイルを順番に返す。

        パターンごとにファイル名でソートするので、``01-``, ``02-`` のような
        接頭辞を付けておけば章順がそのまま決まる。明示的にファイルを列挙した
        場合は書いた順を尊重する。
        """
        files: list[Path] = []
        seen: set[Path] = set()
        for pattern in self.manuscript_patterns:
            if any(ch in pattern for ch in "*?["):
                matched = sorted(self.root.glob(pattern))
            else:
                matched = [self.root / pattern]
            for m in matched:
                rp = m.resolve()
                if rp in seen:
                    continue
                seen.add(rp)
                files.append(m)
        return files

    def cover_path(self) -> Path | None:
        if not self.cover:
            return None
        return self.root / self.cover

    @property
    def full_title(self) -> str:
        return f"{self.title} {self.subtitle}".strip() if self.subtitle else self.title

    @property
    def copyright_line(self) -> str:
        if self.frontmatter.copyright_notice:
            return self.frontmatter.copyright_notice
        year = self.copyright_year or str(_dt.date.today().year)
        return f"© {year} {self.author}"


def _layout_from_dict(data: dict[str, Any] | None, *, profile: str) -> LayoutConfig:
    data = data or {}
    is_print = profile == "print"

    trim = data.get("trim")
    width_mm, height_mm = _resolve_trim(trim, data)

    default_margins = (
        Margins(top_mm=20.0, bottom_mm=20.0, inside_mm=19.0, outside_mm=13.0)
        if is_print
        else Margins(top_mm=15.0, bottom_mm=15.0, inside_mm=15.0, outside_mm=15.0)
    )
    margins = Margins.from_dict(data.get("margins"), default_margins)

    return LayoutConfig(
        profile=profile,
        width_mm=width_mm,
        height_mm=height_mm,
        margins=margins,
        body_font=_as_str(data.get("body_font"), "游明朝") or "游明朝",
        heading_font=_as_str(data.get("heading_font"), "游ゴシック") or "游ゴシック",
        base_font_pt=_as_float(data.get("base_font_pt"), 10.5 if is_print else 11.0),
        line_spacing=_as_float(data.get("line_spacing"), 1.6),
        first_line_indent_chars=_as_float(data.get("first_line_indent_chars"), 1.0),
        mirror_margins=_as_bool(data.get("mirror_margins"), is_print),
        page_numbers=_as_bool(data.get("page_numbers"), is_print),
        toc=TocConfig.from_dict(data.get("toc"), default_style="field" if is_print else "link"),
    )


def _resolve_trim(trim: Any, data: dict[str, Any]) -> tuple[float, float]:
    """判型指定を (幅mm, 高さmm) に解決する。"""
    if isinstance(trim, dict):
        return (
            _as_float(trim.get("width_mm"), 152.4),
            _as_float(trim.get("height_mm"), 228.6),
        )
    key = _as_str(trim).lower().replace(" ", "").replace("jis-", "").replace("判", "")
    if key in TRIM_SIZES:
        return TRIM_SIZES[key]
    m = re.fullmatch(r"(\d+(?:\.\d+)?)x(\d+(?:\.\d+)?)(mm)?", key)
    if m:
        w, h = float(m.group(1)), float(m.group(2))
        if m.group(3) == "mm":
            return w, h
        return w * MM_PER_INCH, h * MM_PER_INCH
    return (
        _as_float(data.get("width_mm"), 152.4),
        _as_float(data.get("height_mm"), 228.6),
    )


def _slugify(text: str) -> str:
    """出力ファイル名に使える ASCII のスラッグを作る。

    日本語だけのタイトルからは作れないので、その場合は空文字を返して
    呼び出し側(ディレクトリ名 → ``book``)にフォールバックさせる。
    """
    slug = re.sub(r"[^A-Za-z0-9]+", "-", text).strip("-").lower()
    return slug[:60] if len(slug) >= 2 else ""
