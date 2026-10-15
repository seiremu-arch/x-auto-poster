#!/usr/bin/env python3
"""翻訳版PROGRESS.mdの字数・語数を、実際の本文ファイルから同期する。

使い方:
    python3 book/tools/sync_tr_counts.py en1
    python3 book/tools/sync_tr_counts.py          # 全訳版

表の各行を、ローマ数字（第1列）で本文ファイルと突き合わせ、
  Source  … 対応する vol1 の原文字数（空白を除く）
  Words   … en1 の語数（題名行・節番号を除く）
  State   … 訳了なら **done**、未訳なら pending
を上書きする。手で語数を書くとずれるため、機械に寄せる。
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SECTION_RE = re.compile(r"^(?:[一二三四五六七八九十]+|[IVXLC]+)$")

# 訳版 -> 原書
PAIRS = {"en1": "vol1", "en2": "vol2", "de1": "vol1", "de2": "vol2",
         "es1": "vol1", "es2": "vol2"}

# 言語ごとの書式。桁区切りと「訳了」の語が違う
FORMATS = {
    "en": {"sep": ",", "done": "**done**"},
    "de": {"sep": ".", "done": "**fertig**"},
    "es": {"sep": ".", "done": "**hecho**"},
}


def group(n: int, sep: str) -> str:
    """桁区切りを言語の流儀に合わせる。ドイツ語は 4.997、英語は 4,997。"""
    return f"{n:,}".replace(",", sep)


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


def sync(vol: str) -> None:
    progress = ROOT / vol / "PROGRESS.md"
    if not progress.exists():
        print(f"[{vol}] PROGRESS.md がないので飛ばす")
        return

    ja = {}
    for p in sorted((ROOT / PAIRS[vol] / "stories").glob("[0-9][0-9]_*.txt")):
        ja[p.name[:2]] = chars(p)

    en = {}
    for p in sorted((ROOT / vol / "stories").glob("[0-9][0-9]_*.txt")):
        en[numeral(p)] = (p.name[:2], words(p))

    lines = progress.read_text(encoding="utf-8").split("\n")
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
        fmt = FORMATS[vol[:2]]
        cells[3] = group(ja[key], fmt["sep"])
        cells[4] = group(w, fmt["sep"])
        cells[5] = fmt["done"]
        if tuple(cells[3:6]) != before:
            lines[i] = "| " + " | ".join(cells) + " |"
            changed.append((num, before, tuple(cells[3:6])))

    if changed:
        progress.write_text("\n".join(lines), encoding="utf-8")
        for num, before, after in changed:
            print(f"[{vol}] {num}: {' / '.join(before)} → {' / '.join(after)}")
    elif en:
        print(f"[{vol}] ずれなし")

    if not en:
        print(f"[{vol}] 訳了 0話")
        return

    total_w = sum(w for _, w in en.values())
    total_c = sum(ja[k] for k, _ in en.values())
    print(f"[{vol}] 訳了 {len(en)}話　原文 {total_c:,}字 → 訳文 {total_w:,} words"
          f"（比 {total_w / total_c:.3f} words/字）")


def main() -> None:
    targets = sys.argv[1:] or list(PAIRS)
    for vol in targets:
        if vol not in PAIRS:
            raise SystemExit(f"不明な巻: {vol}（指定できるのは {', '.join(PAIRS)}）")
        sync(vol)


if __name__ == "__main__":
    main()
