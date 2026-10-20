#!/usr/bin/env python3
"""訳文が原文の構造を取りこぼしていないかを検査する。

使い方:
    python3 book/tools/check_tr_structure.py

原文と訳文を、節ごとの段落数で突き合わせる。翻訳でいちばん起きやすい事故は
誤訳ではなく「一段落まるごと落とす」ことで、通しで読んでも気づきにくい。
節の数と、節ごとの段落数が合っていれば、落ちていないと言える。

語数の比は見ない。会話の多い話は日本語のほうが短く済むので、比が下がること
自体は異常ではない。見るのは構造のほうだけにする。

あわせて字下げも見る。本文の行頭は全角空白でなければならない。タブや半角空白が
混じっても段落数は変わらないので、段落の突き合わせでは見つからない。EPUBにすると
その行だけ字下げが消えるので、ここで落とす。

三字下げの塊の数も、原文と訳文で揃えて見る。書類からの一文を三字下げの塊にするか
「　――」の行にするかは版面の問題だが、同じ箇所を言語ごとに違う扱いにすると、
同じ本の中で書類の見え方が変わる。塊が一つなら段落数は同じなので、段落の
突き合わせでは見つからない。行数は訳すと増えるので、数えるのは塊の数にする。
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAIRS = {"en1": "vol1", "en2": "vol2", "de1": "vol1", "de2": "vol2",
         "es1": "vol1", "es2": "vol2"}

JA_SEC = re.compile(r"^[一二三四五六七八九十]+$")
TR_SEC = re.compile(r"^[IVXLC]+$")  # 訳文の節番号はどの言語もローマ数字


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


INDENT = "\u3000"  # 本文の行頭はこれ以外にない


def bad_indents(lines: list, sec_re: re.Pattern) -> list:
    """行頭が全角空白でない本文行の行番号を返す。表題と節番号は除く。"""
    out = []
    for i, line in enumerate(lines, 1):
        if i == 1 or not line.strip() or sec_re.fullmatch(line.strip()):
            continue
        if not line.startswith(INDENT):
            out.append(i)
    return out


def quote_runs(lines: list) -> int:
    """三字下げの塊の数を返す。連続する三字下げの行は一塊と数える。"""
    n = 0
    in_quote = False
    for line in lines:
        if not line.strip():
            continue
        if line.startswith(QUOTE):
            if not in_quote:
                n += 1
            in_quote = True
        else:
            in_quote = False
    return n


def blocks(lines: list, sec_re: re.Pattern) -> list:
    """節の区切りで分け、節ごとの段落数を返す。"""
    heads = [i for i, l in enumerate(lines) if sec_re.fullmatch(l.strip())]
    return [paragraphs(lines[a:b], sec_re)
            for a, b in zip(heads, heads[1:] + [len(lines)])]


def main() -> int:
    problems = 0
    checked = 0

    for tr_vol, ja_vol in PAIRS.items():
        tr_dir = ROOT / tr_vol / "stories"
        if not tr_dir.is_dir():
            continue
        for tr_path in sorted(tr_dir.glob("[0-9][0-9]_*.txt")):
            num = tr_path.name[:2]
            ja_hits = sorted((ROOT / ja_vol / "stories").glob(f"{num}_*.txt"))
            if not ja_hits:
                print(f"× {tr_vol}/{tr_path.name}: 対応する原文が見つからない")
                problems += 1
                continue

            tr_lines = tr_path.read_text(encoding="utf-8").split("\n")
            ja_lines = ja_hits[0].read_text(encoding="utf-8").split("\n")
            ja = blocks(ja_lines, JA_SEC)
            tr = blocks(tr_lines, TR_SEC)
            checked += 1

            ja_q, tr_q = quote_runs(ja_lines), quote_runs(tr_lines)
            if ja_q != tr_q:
                problems += 1
                print(f"× {tr_vol}/{tr_path.name}: 三字下げの塊の数が違う "
                      f"（原文 {ja_q} / 訳文 {tr_q}）")

            for ln in bad_indents(tr_lines, TR_SEC):
                problems += 1
                print(f"× {tr_vol}/{tr_path.name}: {ln}行目の行頭が全角空白でない")

            if len(ja) != len(tr):
                print(f"× {tr_vol}/{tr_path.name}: 節の数が違う "
                      f"（原文 {len(ja)} / 訳文 {len(tr)}）")
                problems += 1
                continue

            bad = [(i + 1, a, b) for i, (a, b) in enumerate(zip(ja, tr)) if a != b]
            if bad:
                problems += len(bad)
                for sec, a, b in bad:
                    print(f"× {tr_vol}/{tr_path.name}: 第{sec}節の段落数が違う "
                          f"（原文 {a} / 訳文 {b}）")

    print()
    print(f"対象 {checked}話")
    print(f"要対応 {problems} 件" if problems else "構造のずれなし")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
