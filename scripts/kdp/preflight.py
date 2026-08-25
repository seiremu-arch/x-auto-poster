"""入稿前チェック(プリフライト)。

KDPの登録画面ではじかれる・審査で差し戻される前に、原稿とメタデータの
問題をローカルで洗い出す。``error`` が1件でもあればビルドを止める。
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from .config import BookConfig
from .images import ImageError, KDP_SAFE_FORMATS, probe
from .mdparse import Document, Heading

# KDPの登録フォームの上限
MAX_TITLE = 200
MAX_SUBTITLE = 200
MAX_DESCRIPTION = 4000
MAX_KEYWORDS = 7
MAX_KEYWORD_LEN = 50
MAX_CATEGORIES = 3

#: ペーパーバックの本文画像に求められる解像度
PRINT_MIN_DPI = 300
#: 表紙の推奨アスペクト比(高さ / 幅)と最小短辺
COVER_TARGET_RATIO = 1.6
COVER_MIN_WIDTH = 1000
COVER_RECOMMENDED_WIDTH = 1600

TODO_RE = re.compile(r"\b(TODO|FIXME|XXX)\b|※要確認|★")


@dataclass
class Issue:
    level: str  # error / warn / info
    message: str
    where: str = ""

    def format(self) -> str:
        icon = {"error": "ERROR", "warn": "WARN ", "info": "INFO "}.get(self.level, "INFO ")
        loc = f" [{self.where}]" if self.where else ""
        return f"{icon}{loc} {self.message}"


@dataclass
class Report:
    issues: list[Issue] = field(default_factory=list)
    stats: dict[str, object] = field(default_factory=dict)

    def add(self, level: str, message: str, where: str = "") -> None:
        self.issues.append(Issue(level, message, where))

    @property
    def errors(self) -> list[Issue]:
        return [i for i in self.issues if i.level == "error"]

    @property
    def warnings(self) -> list[Issue]:
        return [i for i in self.issues if i.level == "warn"]

    def ok(self, strict: bool = False) -> bool:
        return not self.errors and (not strict or not self.warnings)

    def render(self) -> str:
        lines = [i.format() for i in self.issues] or ["問題は見つかりませんでした。"]
        return "\n".join(lines)


def run(book: BookConfig, document: Document, *, profiles: list[str] | None = None) -> Report:
    """メタデータ・原稿・画像をまとめて検査する。"""
    report = Report()
    profiles = profiles or ["ebook"]
    _check_metadata(book, report)
    _check_manuscript(book, document, report)
    _check_toc(book, document, report)
    _check_images(book, document, report, profiles)
    _check_cover(book, report)

    report.stats = {
        "chapters": len(document.chapters),
        "headings": len(document.headings(3)),
        "characters": document.char_count(),
        "images": len(document.images()),
    }
    return report


# ---------------------------------------------------------------------- メタデータ


def _check_metadata(book: BookConfig, report: Report) -> None:
    where = "book.yaml"
    if len(book.title) > MAX_TITLE:
        report.add("error", f"title が {MAX_TITLE} 文字を超えています({len(book.title)}文字)", where)
    if len(book.subtitle) > MAX_SUBTITLE:
        report.add("error", f"subtitle が {MAX_SUBTITLE} 文字を超えています", where)
    if not book.description:
        report.add("warn", "description(内容紹介)が空です。KDPの登録時に必要になります", where)
    elif len(book.description) > MAX_DESCRIPTION:
        report.add(
            "error",
            f"description が {MAX_DESCRIPTION} 文字を超えています({len(book.description)}文字)",
            where,
        )
    if not book.keywords:
        report.add("warn", "keywords が空です。KDPでは7個まで登録できます", where)
    if len(book.keywords) > MAX_KEYWORDS:
        report.add("error", f"keywords は {MAX_KEYWORDS} 個までです({len(book.keywords)}個)", where)
    for kw in book.keywords:
        if len(kw) > MAX_KEYWORD_LEN:
            report.add("warn", f"キーワードが長すぎます: {kw}", where)
    if len(book.categories) > MAX_CATEGORIES:
        report.add(
            "warn", f"categories は {MAX_CATEGORIES} 個までを想定しています", where
        )
    if not book.published:
        report.add("info", "published(発行日)が未設定です。奥付は日付なしで出力されます", where)
    if book.isbn and not _valid_isbn(book.isbn):
        report.add("error", f"ISBNの形式が不正です: {book.isbn}", where)


def _valid_isbn(isbn: str) -> bool:
    digits = isbn.replace("-", "").replace(" ", "")
    if len(digits) == 13 and digits.isdigit():
        total = sum((1 if i % 2 == 0 else 3) * int(d) for i, d in enumerate(digits))
        return total % 10 == 0
    if len(digits) == 10 and digits[:9].isdigit():
        total = sum((10 - i) * int(d) for i, d in enumerate(digits[:9]))
        check = digits[9].upper()
        total += 10 if check == "X" else (int(check) if check.isdigit() else -1)
        return total % 11 == 0
    return False


# ------------------------------------------------------------------------ 原稿


def _check_manuscript(book: BookConfig, document: Document, report: Report) -> None:
    if not document.chapters:
        report.add("error", "原稿ファイルが1つも見つかりません", "manuscript")
        return

    for chapter in document.chapters:
        where = str(chapter.source.relative_to(book.root)) if _under(chapter.source, book.root) else str(chapter.source)
        h1s = [h for h in chapter.headings if h.level == 1]
        if not h1s:
            report.add("warn", "見出し(#)がありません。章タイトルがファイル名から補われます", where)
        elif len(h1s) > 1:
            report.add(
                "warn",
                f"1ファイルに # 見出しが {len(h1s)} 個あります。章ごとにファイルを分けると"
                "改ページと目次が安定します",
                where,
            )
        _check_heading_levels(chapter.headings, where, report)

        text = chapter.source.read_text(encoding="utf-8")
        for m in TODO_RE.finditer(text):
            line = text.count("\n", 0, m.start()) + 1
            report.add("warn", f"{line}行目に未処理のメモが残っています: {m.group(0)}", where)
        if chapter.word_count() < 200:
            report.add("info", f"本文が短いです({chapter.word_count()}文字)", where)


def _check_heading_levels(headings: list[Heading], where: str, report: Report) -> None:
    prev = 0
    for h in headings:
        if prev and h.level > prev + 1:
            report.add(
                "warn",
                f"見出しレベルが飛んでいます(h{prev} → h{h.level}): {h.text}",
                where,
            )
        prev = h.level


def _check_toc(book: BookConfig, document: Document, report: Report) -> None:
    depth = book.ebook.toc.depth
    entries = document.headings(depth)
    if book.ebook.toc.style == "none":
        report.add("warn", "電子書籍の目次が無効になっています(toc.style: none)", "book.yaml")
        return
    if not entries:
        report.add(
            "error",
            "目次に載せる見出しがありません。各章の先頭に # 見出しを置いてください",
            "manuscript",
        )
    elif len(entries) < 2:
        report.add("warn", "目次の項目が1つしかありません", "manuscript")


# ------------------------------------------------------------------------ 画像


def _check_images(
    book: BookConfig, document: Document, report: Report, profiles: list[str]
) -> None:
    for block in document.images():
        path = block.resolve(book.root)
        where = block.src
        if path is None:
            report.add("error", "画像ファイルが見つかりません", where)
            continue
        try:
            info = probe(path)
        except (OSError, ImageError) as exc:
            report.add("error", str(exc), where)
            continue
        if info.mime not in KDP_SAFE_FORMATS:
            report.add("error", f"KDPが受け付けない画像形式です: {info.mime}", where)
        size_mb = path.stat().st_size / (1024 * 1024)
        if size_mb > 5:
            report.add("warn", f"画像が大きすぎます({size_mb:.1f}MB)。5MB以下を推奨します", where)
        if "print" in profiles:
            layout = book.print_
            m = layout.margins
            content_mm = layout.width_mm - m.inside_mm - m.outside_mm - m.gutter_mm
            content_in = max(content_mm, 1.0) / 25.4
            effective_dpi = info.width_px / content_in if content_in else 0
            if info.width_px < 600 or effective_dpi < PRINT_MIN_DPI:
                report.add(
                    "warn",
                    f"ペーパーバックには解像度が不足しています(版面幅いっぱいで約{effective_dpi:.0f}dpi、"
                    f"推奨{PRINT_MIN_DPI}dpi)",
                    where,
                )


def _check_cover(book: BookConfig, report: Report) -> None:
    path = book.cover_path()
    if path is None:
        report.add("info", "cover が未設定です。表紙はKDPの登録画面で個別にアップロードします", "book.yaml")
        return
    if not path.is_file():
        report.add("error", f"表紙画像が見つかりません: {book.cover}", "book.yaml")
        return
    try:
        info = probe(path)
    except (OSError, ImageError) as exc:
        report.add("error", str(exc), book.cover)
        return
    if info.mime not in ("image/jpeg", "image/tiff"):
        report.add("warn", "表紙はJPEGまたはTIFFが推奨です", book.cover)
    if info.width_px < COVER_MIN_WIDTH:
        report.add(
            "error",
            f"表紙の幅が {COVER_MIN_WIDTH}px 未満です({info.width_px}px)",
            book.cover,
        )
    elif info.width_px < COVER_RECOMMENDED_WIDTH:
        report.add(
            "warn",
            f"表紙は幅{COVER_RECOMMENDED_WIDTH}px以上(1600×2560px)を推奨します(現在{info.width_px}px)",
            book.cover,
        )
    ratio = info.height_px / info.width_px if info.width_px else 0
    if abs(ratio - COVER_TARGET_RATIO) > 0.15:
        report.add(
            "warn",
            f"表紙の縦横比が推奨(1:{COVER_TARGET_RATIO})から外れています(1:{ratio:.2f})",
            book.cover,
        )


def _under(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False
