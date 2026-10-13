#!/usr/bin/env python3
"""構成表の字数を、実際の本文ファイルから同期する。

使い方:
    python3 book/tools/sync_counts.py

00_構成表.md の各行にある「**完成**（N字）」を、対応する本文ファイルの
実文字数（空白・改行を除く）で上書きする。題名で突き合わせるので、
構成表の題と本文一行目の題が一致している必要がある。

手で字数を書くと毎回ずれるため、この作業を機械に寄せる。
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TABLE = ROOT / "00_構成表.md"


def count(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    body = "\n".join(text.split("\n")[1:])  # 題名行を除く
    return len(re.sub(r"\s", "", body))


def main() -> None:
    # 題名 -> 実文字数
    counts = {}
    for vol in ("vol1", "vol2"):
        for p in sorted((ROOT / vol / "stories").glob("[0-9][0-9]_*.txt")):
            title = p.read_text(encoding="utf-8").split("\n")[0].strip()
            counts[title] = count(p)

    lines = TABLE.read_text(encoding="utf-8").split("\n")
    changed = []

    for i, line in enumerate(lines):
        if "**完成**" not in line or not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.split("|")]
        title = cells[2] if len(cells) > 2 else ""
        if title not in counts:
            continue
        actual = counts[title]
        m = re.search(r"\*\*完成\*\*（([\d,]+)字）", line)
        if not m:
            continue
        written = int(m.group(1).replace(",", ""))
        if written != actual:
            lines[i] = line.replace(m.group(0), f"**完成**（{actual:,}字）")
            changed.append((title, written, actual))

    if changed:
        TABLE.write_text("\n".join(lines), encoding="utf-8")
        for title, before, after in changed:
            print(f"{title}: {before:,} → {after:,}")
    else:
        print("ずれなし")

    for vol, label in (("vol1", "第一巻"), ("vol2", "第二巻")):
        files = sorted((ROOT / vol / "stories").glob("[0-9][0-9]_*.txt"))
        total = sum(count(p) for p in files)
        print(f"{label}: {len(files)}話 {total:,}字")


if __name__ == "__main__":
    main()
