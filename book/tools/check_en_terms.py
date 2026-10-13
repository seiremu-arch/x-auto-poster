#!/usr/bin/env python3
"""英語版の用語ゆれ・表記ゆれを機械で検査する。

使い方:
    python3 book/tools/check_en_terms.py

GLOSSARY.md で固定した語の「やってはいけない変形」と、
英国綴り・組み方の規則を正規表現で当てる。十二話を通して読む代わりに、
ずれやすいところだけを機械に見せる。
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STORIES = sorted(ROOT.glob("en[0-9]/stories/[0-9][0-9]_*.txt"))

# (説明, 正規表現) ─ 当たったら報告する
CHECKS = [
    ("技師は technician（engineer は不可）", r"\bengineers?\b"),
    ("半色は half-shade（ハイフンなし・colour 綴りは不可）", r"\bhalf[ ]shade\b|\bhalf-?colou?r\b"),
    ("校正官は the Proofreader（大文字・ハイフンなし）", r"\bproofreader\b|\bProof[- ]reader\b"),
    ("情動荷重は affective load", r"\bemotional load\b|\bemotion load\b|\baffect load\b"),
    ("素片は fragment", r"\bshards?\b|\bsegments? of memory\b|\bmemory pieces?\b"),
    ("照合機は the Comparator", r"\bcollator\b|\bmatching machine\b"),
    ("残差は residual（residue は不可）", r"\bresidues?\b"),
    ("均し計画は the Levelling Plan（大文字）", r"\blevelling plan\b"),
    ("幸福指数は the Happiness Index（大文字）", r"\bhappiness index\b"),
    ("校正官の声は no humidity（moisture は不可）", r"no moisture in it"),
    ("水は paper cup（plastic/paper-cup は不可）", r"\bplastic cup\b|\bpaper-cup\b"),
    ("百分率は per cent（percent は不可）", r"\bpercent\b"),
    # size / prize / seize は正しい綴りなので、iz の前を4字以上に絞る
    ("英国綴り: -ise/-isation", r"\b\w{4,}iz(e|es|ed|ing|ation|ations)\b"),
    ("英国綴り: colour/behaviour/favour など", r"\bcolors?\b|\bbehavior\b|\bfavor(s|ed|ite)?\b|\bhonor\b"),
    ("英国綴り: centre/metre", r"\bcenters?\b|\bmeters?\b(?! of )"),
    ("英国綴り: defence/offence", r"\bdefense\b|\boffense\b"),
    ("英国綴り: grey", r"\bgray\b"),
    ("漢数字の残り（〇・一二三…）", r"[〇一二三四五六七八九十]"),
    ("全角文字の残り（字下げの U+3000 以外）", r"[^\x00-\x7F　—–‘’“”…¥]"),
    ("二重空白", r"[a-z,.] {2,}[A-Za-z]"),
    ("行末の空白", r"[ \t]+$"),
    ("曲がっていない引用符（本文は \" で統一）", r"[“”]"),
]

# 例外: 固有名詞・意図した表記
ALLOWED = {
    r"\bmeters?\b(?! of )": ["parameters"],
    r"\b\w{4,}iz(e|es|ed|ing|ation|ations)\b": ["capsize", "capsized",
                                                 "downsize", "oversize"],
}


def main() -> int:
    hits = 0
    for path in STORIES:
        text = path.read_text(encoding="utf-8")
        lines = text.split("\n")
        for label, pattern in CHECKS:
            rx = re.compile(pattern, re.MULTILINE)
            for i, line in enumerate(lines, start=1):
                for m in rx.finditer(line):
                    word = m.group(0)
                    if any(word.lower() in a for a in ALLOWED.get(pattern, [])):
                        continue
                    rel = path.relative_to(ROOT)
                    print(f"{rel}:{i}  {label}  → {word!r}")
                    hits += 1

    print()
    print(f"対象 {len(STORIES)}ファイル")
    print(f"要対応 {hits} 件" if hits else "用語ゆれなし")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
