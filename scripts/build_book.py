#!/usr/bin/env python3
"""KDP入稿ファイルをまとめてビルドするCLI。

    python scripts/build_book.py manuscripts/sample-book
    python scripts/build_book.py manuscripts/sample-book --target docx --profile print
    python scripts/build_book.py --check-only --strict

原稿(Markdown) + book.yaml から、以下を ``build/<slug>/`` に出力する。

* ``<slug>-ebook.docx`` … 電子書籍用(リンク付き目次、判型なし)
* ``<slug>-print.docx`` … ペーパーバック用(判型・見開き余白・ノンブル・目次フィールド)
* ``<slug>.epub``       … EPUB3(KDP推奨形式)
* ``<slug>-kdp-metadata.md`` … KDPの登録画面にコピペするメタデータ
* ``build-manifest.json``    … ビルド結果のサマリ
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from kdp import preflight  # noqa: E402
from kdp.config import PROFILES, BookConfig, ConfigError  # noqa: E402
from kdp.docx_builder import build_docx  # noqa: E402
from kdp.epub_builder import build_epub  # noqa: E402
from kdp.mdparse import parse_manuscript  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUT = REPO_ROOT / "build"
MANUSCRIPT_ROOT = REPO_ROOT / "manuscripts"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Markdown原稿からKDP入稿用の docx / EPUB を生成する",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "book",
        nargs="?",
        help="本のディレクトリ(book.yaml のある場所)。省略時は manuscripts/ 直下から探す",
    )
    parser.add_argument(
        "--target",
        default="all",
        help="生成する形式: docx / epub / all(既定)。カンマ区切りで複数指定可",
    )
    parser.add_argument(
        "--profile",
        default="ebook,print",
        help=f"docxのプロファイル: {'/'.join(PROFILES)}(既定: ebook,print)",
    )
    parser.add_argument("--out", default=None, help="出力先ディレクトリ(既定: build/)")
    parser.add_argument("--check-only", action="store_true", help="プリフライトだけ実行する")
    parser.add_argument("--strict", action="store_true", help="警告もエラー扱いにする")
    parser.add_argument("--quiet", action="store_true", help="サマリ以外を出力しない")
    args = parser.parse_args(argv)

    try:
        book_dir = _resolve_book_dir(args.book)
        book = BookConfig.load(book_dir)
    except ConfigError as exc:
        print(f"設定エラー:\n{exc}", file=sys.stderr)
        return 2

    sources = book.manuscript_files()
    missing = [str(p) for p in sources if not p.is_file()]
    if missing:
        print("原稿ファイルが見つかりません:\n" + "\n".join(f"- {m}" for m in missing), file=sys.stderr)
        return 2

    document = parse_manuscript(sources)

    targets = _split(args.target, {"docx", "epub", "all"})
    if "all" in targets:
        targets = {"docx", "epub"}
    profiles = _split(args.profile, set(PROFILES))

    report = preflight.run(book, document, profiles=sorted(profiles))
    if not args.quiet:
        print(f"■ プリフライト: {book.full_title}")
        print(report.render())
        print()

    if not report.ok(strict=args.strict):
        reason = "エラー" if report.errors else "警告(--strict)"
        print(f"プリフライトで{reason}が見つかったため中止しました。", file=sys.stderr)
        return 1

    if args.check_only:
        _print_summary(book, document, report, [])
        return 0

    out_dir = Path(args.out) if args.out else DEFAULT_OUT / book.slug
    out_dir.mkdir(parents=True, exist_ok=True)

    artifacts: list[dict[str, object]] = []
    warnings: list[str] = []

    if "docx" in targets:
        for profile in sorted(profiles):
            path = out_dir / f"{book.slug}-{profile}.docx"
            result = build_docx(book, document, profile, path)
            warnings.extend(result.warnings)
            artifacts.append(_artifact(result.path, f"docx/{profile}"))

    if "epub" in targets:
        path = out_dir / f"{book.slug}.epub"
        result = build_epub(book, document, path)
        warnings.extend(result.warnings)
        artifacts.append(_artifact(result.path, "epub"))

    meta_path = out_dir / f"{book.slug}-kdp-metadata.md"
    meta_path.write_text(_kdp_metadata(book, document), encoding="utf-8")
    artifacts.append(_artifact(meta_path, "metadata"))

    manifest = {
        "book": book.full_title,
        "slug": book.slug,
        "author": book.author,
        "built_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "stats": report.stats,
        "estimated_print_pages": _estimated_pages(book, document),
        "artifacts": artifacts,
        "warnings": warnings,
    }
    manifest_path = out_dir / "build-manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    if warnings and not args.quiet:
        print("■ ビルド時の警告")
        for w in dict.fromkeys(warnings):
            print(f"WARN  {w}")
        print()

    _print_summary(book, document, report, artifacts)
    return 0


# ---------------------------------------------------------------------- 補助処理


def _resolve_book_dir(arg: str | None) -> Path:
    if arg:
        return Path(arg)
    candidates = sorted(
        p.parent for p in MANUSCRIPT_ROOT.glob("*/book.y*ml") if p.suffix in (".yaml", ".yml")
    )
    if len(candidates) == 1:
        return candidates[0]
    if not candidates:
        raise ConfigError(
            [f"{MANUSCRIPT_ROOT} に book.yaml が見つかりません。対象を引数で指定してください"]
        )
    names = ", ".join(c.name for c in candidates)
    raise ConfigError([f"対象が複数あります。引数で指定してください: {names}"])


def _split(value: str, allowed: set[str]) -> set[str]:
    items = {v.strip().lower() for v in value.split(",") if v.strip()}
    unknown = items - allowed
    if unknown:
        raise SystemExit(f"不明な指定です: {', '.join(sorted(unknown))}")
    return items


def _artifact(path: Path, kind: str) -> dict[str, object]:
    return {
        "kind": kind,
        "path": str(path.relative_to(REPO_ROOT)) if _under(path) else str(path),
        "bytes": path.stat().st_size,
    }


def _under(path: Path) -> bool:
    try:
        path.resolve().relative_to(REPO_ROOT)
        return True
    except ValueError:
        return False


def _estimated_pages(book: BookConfig, document) -> int:
    """ペーパーバックの概算ページ数(背幅の計算やKDPの価格設定の目安)。"""
    lay = book.print_
    m = lay.margins
    content_w = max(lay.width_mm - m.inside_mm - m.outside_mm - m.gutter_mm, 10.0)
    content_h = max(lay.height_mm - m.top_mm - m.bottom_mm, 10.0)
    char_mm = lay.base_font_pt * 25.4 / 72  # 全角1文字ぶんの幅
    chars_per_line = max(int(content_w / char_mm), 1)
    lines_per_page = max(int(content_h / (char_mm * lay.line_spacing)), 1)
    per_page = chars_per_line * lines_per_page
    pages = -(-document.char_count() // per_page)
    return pages + len(document.chapters)  # 章扉ぶんの余白を上乗せ


def _kdp_metadata(book: BookConfig, document) -> str:
    """KDPの登録画面へコピペするためのメタデータをMarkdownで書き出す。"""
    lines = [
        f"# KDP登録用メタデータ: {book.full_title}",
        "",
        "KDPの「本の詳細」画面にそのまま貼り付けられるようにまとめたもの。",
        "",
        "## 本の詳細",
        "",
        f"- **本のタイトル**: {book.title}",
        f"- **サブタイトル**: {book.subtitle or '(なし)'}",
        f"- **著者**: {book.author}",
        f"- **出版社**: {book.publisher or '(なし)'}",
        f"- **言語**: {book.language}",
        f"- **発行日**: {book.published or '(未設定)'}",
        f"- **ISBN**: {book.isbn or '(KDPの無料ISBNを使用)'}",
        "",
        "## 内容紹介(description)",
        "",
        book.description.strip() or "(未記入)",
        "",
        f"※ {len(book.description)} / 4000 文字",
        "",
        "## キーワード(7個まで)",
        "",
    ]
    lines += [f"{i}. {kw}" for i, kw in enumerate(book.keywords, start=1)] or ["(未設定)"]
    lines += ["", "## カテゴリー", ""]
    lines += [f"- {c}" for c in book.categories] or ["- (未設定)"]
    lines += [
        "",
        "## 原稿の統計",
        "",
        f"- 章数: {len(document.chapters)}",
        f"- 見出し数: {len(document.headings(3))}",
        f"- 本文文字数: {document.char_count():,}",
        f"- ペーパーバック概算ページ数: 約{_estimated_pages(book, document)}ページ"
        f"({book.print_.width_mm:.0f}×{book.print_.height_mm:.0f}mm)",
        "",
        "## 目次",
        "",
    ]
    for chapter, heading in document.headings(book.ebook.toc.depth):
        lines.append(f"{'  ' * (heading.level - 1)}- {heading.text}")
    lines.append("")
    return "\n".join(lines)


def _print_summary(book: BookConfig, document, report, artifacts: list[dict[str, object]]) -> None:
    print(f"■ {book.full_title} / {book.author}")
    print(
        f"  章数 {len(document.chapters)} ・ 見出し {len(document.headings(3))} ・ "
        f"本文 {document.char_count():,} 文字 ・ 概算 {_estimated_pages(book, document)} ページ"
    )
    if report.warnings:
        print(f"  警告 {len(report.warnings)} 件")
    for a in artifacts:
        print(f"  → {a['path']} ({int(a['bytes']) / 1024:.1f} KB)")


if __name__ == "__main__":
    raise SystemExit(main())
