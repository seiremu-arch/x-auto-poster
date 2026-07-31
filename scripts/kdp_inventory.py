#!/usr/bin/env python3
"""kdp/bookshelf.csv から既刊の棚卸し一覧 kdp/INVENTORY.md を生成する。

使い方:
    python scripts/kdp_inventory.py
"""

from __future__ import annotations

import csv
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "kdp" / "bookshelf.csv"
OUTPUT = ROOT / "kdp" / "INVENTORY.md"

COLUMNS = [
    "series",
    "volume",
    "title",
    "subtitle",
    "language",
    "format",
    "asin",
    "status",
    "submit_date",
    "price",
    "currency",
    "kdp_select",
    "notes",
]

STATUS_LABELS = {
    "live": "公開中",
    "in_review": "審査中",
    "draft": "下書き",
    "unpublished": "非公開",
}


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        missing = [c for c in COLUMNS if c not in (reader.fieldnames or [])]
        if missing:
            sys.exit(f"列が足りません: {', '.join(missing)}")
        rows = []
        for i, row in enumerate(reader, start=2):
            row = {k: (v or "").strip() for k, v in row.items() if k in COLUMNS}
            if not row.get("title"):
                continue
            if row["series"].startswith("EXAMPLE"):
                continue
            row["_line"] = str(i)
            rows.append(row)
        return rows


def volume_key(row: dict[str, str]) -> tuple[int, str]:
    """巻数が数値ならその順、非数値なら末尾にまとめる。"""
    raw = row.get("volume", "")
    try:
        return (int(raw), "")
    except ValueError:
        return (10**6, raw)


def find_issues(rows: list[dict[str, str]]) -> list[str]:
    issues: list[str] = []
    seen_asin: dict[str, str] = {}
    seen_slot: dict[tuple[str, str, str, str], str] = {}
    volumes: dict[tuple[str, str, str], set[int]] = defaultdict(set)

    for row in rows:
        # ASINはKDPが1タイトル1形態ごとに振る一意キー。重複＝転記ミス。
        asin = row["asin"]
        if asin:
            if asin in seen_asin:
                issues.append(
                    f"ASIN重複: {asin}（{seen_asin[asin]}行目と{row['_line']}行目）"
                )
            else:
                seen_asin[asin] = row["_line"]

        # シリーズ・巻が未記入の行は同じキーに潰れてしまうため、両方揃った行だけ照合する。
        if row["series"] and row["volume"]:
            key = (row["series"], row["volume"], row["language"], row["format"])
            if key in seen_slot:
                issues.append(
                    f"重複: {row['series']} 第{row['volume']}巻 / {row['language']} / "
                    f"{row['format']}（{seen_slot[key]}行目と{row['_line']}行目）"
                )
            else:
                seen_slot[key] = row["_line"]

        if row["status"] == "live" and not row["submit_date"]:
            issues.append(f"販売中なのに提出日が空: {row['title']}（{row['_line']}行目）")
        if row["status"] == "live" and not row["asin"]:
            issues.append(f"販売中なのにASINが空: {row['title']}（{row['_line']}行目）")
        try:
            volumes[(row["series"], row["language"], row["format"])].add(
                int(row["volume"])
            )
        except ValueError:
            pass

    unfilled = [r for r in rows if not r["series"] or not r["volume"]]
    if unfilled:
        issues.append(
            f"シリーズ／巻数が未記入: {len(unfilled)}件"
            f"（{'、'.join(r['_line'] for r in unfilled)}行目）。"
            "埋めると巻数の抜けを検出できるようになります"
        )

    for (series, language, fmt), nums in sorted(volumes.items()):
        if not nums or not series:
            continue
        gaps = sorted(set(range(1, max(nums) + 1)) - nums)
        if gaps:
            listed = "、".join(f"第{n}巻" for n in gaps)
            issues.append(f"巻数の抜け: {series} / {language} / {fmt} … {listed}")

    return issues


def render(rows: list[dict[str, str]]) -> str:
    lines = [
        "# KDP 既刊棚卸し",
        "",
        f"生成日: {date.today().isoformat()}　/　登録タイトル数: {len(rows)}",
        "",
        "> このファイルは `scripts/kdp_inventory.py` の生成物です。直接編集せず",
        "> `kdp/bookshelf.csv` を編集して再生成してください。",
        "",
    ]

    if not rows:
        lines += ["まだ1件も登録されていません。`kdp/bookshelf.csv` に記入してください。", ""]
        return "\n".join(lines)

    lines += ["## サマリー", ""]

    by_status: dict[str, int] = defaultdict(int)
    by_language: dict[str, int] = defaultdict(int)
    by_format: dict[str, int] = defaultdict(int)
    for row in rows:
        by_status[row["status"] or "(未設定)"] += 1
        by_language[row["language"] or "(未設定)"] += 1
        by_format[row["format"] or "(未設定)"] += 1

    lines += ["| ステータス | 件数 |", "| --- | --- |"]
    for status, count in sorted(by_status.items(), key=lambda x: -x[1]):
        lines.append(f"| {STATUS_LABELS.get(status, status)} | {count} |")
    lines.append("")

    lines += ["| 言語 | 件数 |", "| --- | --- |"]
    for language, count in sorted(by_language.items(), key=lambda x: -x[1]):
        lines.append(f"| {language} | {count} |")
    lines.append("")

    lines += ["| 形態 | 件数 |", "| --- | --- |"]
    for fmt, count in sorted(by_format.items(), key=lambda x: -x[1]):
        lines.append(f"| {fmt} | {count} |")
    lines.append("")

    lines += ["## シリーズ別", ""]

    by_series: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_series[row["series"] or "(シリーズ未設定)"].append(row)

    for series in sorted(by_series):
        entries = sorted(by_series[series], key=lambda r: (volume_key(r), r["language"]))
        languages = sorted({r["language"] for r in entries if r["language"]})
        lines += [
            f"### {series}",
            "",
            f"{len(entries)}件　/　言語: {'、'.join(languages) or '未設定'}",
            "",
            "| 巻 | タイトル | 言語 | 形態 | ASIN | ステータス | 提出日 | 価格 |",
            "| --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
        for row in entries:
            price = " ".join(p for p in (row["price"], row["currency"]) if p) or "-"
            lines.append(
                "| {volume} | {title} | {language} | {format} | {asin} | {status} | {date} | {price} |".format(
                    volume=row["volume"] or "-",
                    title=row["title"],
                    language=row["language"] or "-",
                    format=row["format"] or "-",
                    asin=row["asin"] or "-",
                    status=STATUS_LABELS.get(row["status"], row["status"] or "-"),
                    date=row["submit_date"] or "-",
                    price=price,
                )
            )
        lines.append("")

    issues = find_issues(rows)
    lines += ["## 要確認", ""]
    if issues:
        lines += [f"- {issue}" for issue in issues]
    else:
        lines.append("なし。")
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    if not SOURCE.exists():
        sys.exit(f"{SOURCE} がありません。")
    rows = load_rows(SOURCE)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(render(rows), encoding="utf-8")
    issues = find_issues(rows)
    print(f"{OUTPUT} を生成しました（{len(rows)}件、要確認 {len(issues)}件）")


if __name__ == "__main__":
    main()
