#!/usr/bin/env python3
"""英語版の用語ゆれ・表記ゆれを機械で検査する。

使い方:
    python3 book/tools/check_en_terms.py

GLOSSARY.md で固定した語の「やってはいけない変形」と、
英国綴り・組み方の規則を正規表現で当てる。十二話を通して読む代わりに、
ずれやすいところだけを機械に見せる。

人名も見る。原文に読み仮名がない姓は訳者が読みを決めることになり、
決め方を間違えても英文だけ読んでいるかぎり気づけない（杉本を Suginoto と
読んでいた事例がある）。原文に姓があるのに対応する英語名がない話は、
読みを決め直したか、落としたかのどちらかなので報告する。
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

# 原文の姓 -> 英語表記。第二巻は原文の読み仮名、第一巻は通用する読みによる。
# 「その話に原文の姓が出るなら、英文にもこの綴りが出る」ことだけを見る。
NAMES = {
    "vol1": {
        "01": [("梶", "Kaji"), ("杉本", "Sugimoto")],
        "02": [("戸並", "Tonami"), ("蓮見", "Hasumi")],
        "03": [("桐山", "Kiriyama"), ("宮田", "Miyata")],
        "04": [("桜井", "Sakurai"), ("志村", "Shimura")],
        "05": [("芦田", "Ashida"), ("望月", "Mochizuki")],
        "06": [("沢田", "Sawada")],
        "07": [("桑野", "Kuwano"), ("戸倉", "Tokura")],
        "08": [("宮下", "Miyashita"), ("岸", "Kishi")],
        "09": [("有村", "Arimura"), ("木内", "Kiuchi")],
        "10": [("塚原", "Tsukahara")],
        "11": [("須賀", "Suga")],
        "12": [("堀", "Hori")],
    },
    "vol2": {
        "01": [("伴", "Ban")],
        "02": [("瀬能", "Seno")],
        "03": [("早瀬", "Hayase"), ("湯浅", "Yuasa")],
        "04": [("名越", "Nagoshi")],
        "05": [("神保", "Jinbo")],
        "06": [("蓼沼", "Tadenuma"), ("桑島", "Kuwashima")],
        "07": [("岩見", "Iwami")],
        "08": [("久留須", "Kurusu")],
        "09": [("硲", "Hazama")],
        "10": [("荻堂", "Ogido")],
        "11": [("黛", "Mayuzumi")],
        "12": [("湊", "Minato")],
    },
}

# 例外: 固有名詞・意図した表記
ALLOWED = {
    r"\bmeters?\b(?! of )": ["parameters"],
    r"\b\w{4,}iz(e|es|ed|ing|ation|ations)\b": ["capsize", "capsized",
                                                 "downsize", "oversize"],
}


def check_names() -> int:
    """原文に姓があるのに、訳文に対応する英語名がない話を報告する。"""
    bad = 0
    for en_vol, ja_vol in (("en1", "vol1"), ("en2", "vol2")):
        for num, pairs in NAMES[ja_vol].items():
            en_hits = sorted((ROOT / en_vol / "stories").glob(f"{num}_*.txt"))
            ja_hits = sorted((ROOT / ja_vol / "stories").glob(f"{num}_*.txt"))
            if not en_hits or not ja_hits:
                continue
            en_text = en_hits[0].read_text(encoding="utf-8")
            ja_text = ja_hits[0].read_text(encoding="utf-8")
            for ja_name, en_name in pairs:
                if ja_name not in ja_text:
                    print(f"{ja_vol}/{num}: 原文に『{ja_name}』がない"
                          f"（人名表のほうが古い可能性）")
                    bad += 1
                elif en_name not in en_text:
                    print(f"{en_vol}/{en_hits[0].name}: "
                          f"『{ja_name}』に対応する {en_name} が訳文にない")
                    bad += 1
    return bad


def main() -> int:
    hits = check_names()
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
