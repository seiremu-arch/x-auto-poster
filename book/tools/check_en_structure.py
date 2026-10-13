#!/usr/bin/env python3
"""英語版が原文の構造を取りこぼしていないかを検査する。

使い方:
    python3 book/tools/check_en_structure.py

原文と訳文を、節ごとの段落数で突き合わせる。翻訳でいちばん起きやすい事故は
誤訳ではなく「一段落まるごと落とす」ことで、通しで読んでも気づきにくい。
節の数と、節ごとの段落数が合っていれば、落ちていないと言える。

語数の比は見ない。会話の多い話は日本語のほうが短く済むので、比が下がること
自体は異常ではない。見るのは構造のほうだけにする。
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAIRS = {"en1": "vol1", "en2": "vol2"}

JA_SEC = re.compile(r"^[一二三四五六七八九十]+$")
EN_SEC = re.compile(r"^[IVXLC]+$")


QUOTE = "\u3000\u3000\u3000"  # 書類の表題などの引用に使う三字下げ


def paragraphs(chunk: list, sec_re: re.Pattern) -> int:
    """段落を数える。三字下げの引用は、連続していれば一塊として数える。

    長い書類の表題は、英語では二行に割るのが自然で、日本語では一行に収まる。
    行数で突き合わせるとここが必ずずれるので、引用の連続は一つと見る。
    """
    n = 0
    in_quote = False
    for line in chunk:
        if not line.strip() or sec_re.fullmatch(line.strip()):
            continue
        if line.startswith(QUOTE):
            if not in_quote:
                n += 1
            in_quote = True
        else:
            in_quote = False
            n += 1
    return n


def blocks(lines: list, sec_re: re.Pattern) -> list:
    """節の区切りで分け、節ごとの段落数を返す。"""
    heads = [i for i, l in enumerate(lines) if sec_re.fullmatch(l.strip())]
    return [paragraphs(lines[a:b], sec_re)
            for a, b in zip(heads, heads[1:] + [len(lines)])]


def main() -> int:
    problems = 0
    checked = 0

    for en_vol, ja_vol in PAIRS.items():
        en_dir = ROOT / en_vol / "stories"
        if not en_dir.is_dir():
            continue
        for en_path in sorted(en_dir.glob("[0-9][0-9]_*.txt")):
            num = en_path.name[:2]
            ja_hits = sorted((ROOT / ja_vol / "stories").glob(f"{num}_*.txt"))
            if not ja_hits:
                print(f"× {en_vol}/{en_path.name}: 対応する原文が見つからない")
                problems += 1
                continue

            ja = blocks(ja_hits[0].read_text(encoding="utf-8").split("\n"), JA_SEC)
            en = blocks(en_path.read_text(encoding="utf-8").split("\n"), EN_SEC)
            checked += 1

            if len(ja) != len(en):
                print(f"× {en_vol}/{en_path.name}: 節の数が違う "
                      f"（原文 {len(ja)} / 訳文 {len(en)}）")
                problems += 1
                continue

            bad = [(i + 1, a, b) for i, (a, b) in enumerate(zip(ja, en)) if a != b]
            if bad:
                problems += len(bad)
                for sec, a, b in bad:
                    print(f"× {en_vol}/{en_path.name}: 第{sec}節の段落数が違う "
                          f"（原文 {a} / 訳文 {b}）")

    print()
    print(f"対象 {checked}話")
    print(f"要対応 {problems} 件" if problems else "構造のずれなし")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
