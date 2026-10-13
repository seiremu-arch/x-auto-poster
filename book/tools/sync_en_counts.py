#!/usr/bin/env python3
"""英語版PROGRESS.mdの字数・語数を、実際の本文ファイルから同期する。

使い方:
    python3 book/tools/sync_en_counts.py

表の各行を、ローマ数字（第1列）で本文ファイルと突き合わせ、
  Source  … 対応する vol1 の原文字数（空白を除く）
  Words   … en1 の語数（題名行・節番号を除く）
  State   … 訳了なら **done**、未訳なら pending
を上書きする。手で語数を書くとずれるため、機械に寄せる。
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROGRESS = ROOT / "en1" / "PROGRESS.md"
SECTION_RE = re.compile(r"^(?:[一二三四五六七八九十]+|[IVXLC]+)$")


def numeral(path: Path) -> str:
    """本文一行目「V. The Second-Person Dream」から「V」を取る。"""
    head = path.read_text(encoding="utf-8").split("\n")[0].strip()
    return head.split(".", 1)[0].strip()


def chars(path: Path) -> int:
    body = "\n".join(path.read_text(encoding="utf-8").split("\n")[1:])
    return len(re.sub(r"\s", "", body))


def words(path: Path) -> int:
    lines = path.read_text(encoding="utf-8").split("\n")[1:]
    return sum(
        len(line.split())
        for line in lines
        if line.strip() and not SECTION_RE.match(line.strip())
    )


def main() -> None:
    ja = {}
    for p in sorted((ROOT / "vol1" / "stories").glob("[0-9][0-9]_*.txt")):
        ja[p.name[:2]] = chars(p)

    en = {}
    for p in sorted((ROOT / "en1" / "stories").glob("[0-9][0-9]_*.txt")):
        en[numeral(p)] = (p.name[:2], words(p))

    lines = PROGRESS.read_text(encoding="utf-8").split("\n")
    changed = []

    for i, line in enumerate(lines):
        if not line.startswith("| ") or line.startswith("| # ") or "---" in line:
            continue
        cells = [c.strip() for c in line.split("|")[1:-1]]
        if len(cells) != 6:
            continue
        num = cells[0]
        if num not in en:
            continue
        key, w = en[num]
        before = tuple(cells[3:6])
        cells[3] = f"{ja[key]:,}"
        cells[4] = f"{w:,}"
        cells[5] = "**done**"
        if tuple(cells[3:6]) != before:
            lines[i] = "| " + " | ".join(cells) + " |"
            changed.append((num, before, tuple(cells[3:6])))

    if changed:
        PROGRESS.write_text("\n".join(lines), encoding="utf-8")
        for num, before, after in changed:
            print(f"{num}: {' / '.join(before)} → {' / '.join(after)}")
    else:
        print("ずれなし")

    total_w = sum(w for _, w in en.values())
    total_c = sum(ja[k] for k, _ in en.values())
    print(f"訳了 {len(en)}話　原文 {total_c:,}字 → 英文 {total_w:,} words"
          f"（比 {total_w / total_c:.3f} words/字）")


if __name__ == "__main__":
    main()
