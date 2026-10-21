#!/usr/bin/env python3
"""星新一賞の応募作と、KDPで出す本との重複を検査する。

使い方:
    python3 book/tools/check_overlap.py

応募作『境界線、未編集』は未発表でなければならない。本を出したあとで
「同じ文が出版物に載っていた」となると面倒なので、本文・KDP登録情報・
設定資料の全部を応募作と突き合わせる。

検査するもの:
  1. book/ 配下に応募作の複製が置かれていないか
  2. 十六字以上で完全一致する文がどれだけあるか
  3. 応募作固有の固有名詞が本に紛れていないか
  4. 訳書（英・独・西）に、応募作固有の固有名詞が紛れていないか

訳書は日本語の文と一致しようがないので、2は素通りする。そこで4を別に
置く。固有名詞はローマ字にすると検出をすり抜けるため、訳書側はローマ字形と
各言語の訳語で当てる。

共有してよいもの（半色、残差、校正官の定型応答など）は、同一世界の
シリーズとして当然に重なるため、許容一覧に入れて除外する。
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRIZE = ROOT.parent / "novel" / "kyokaisen-mihenshu.txt"

MIN_LEN = 16

# 同一世界のシリーズとして共有してよい語句
ALLOWED = [
    "削らずに、削ったと記録することはできるか",
    "破棄していない理由は、記録にありません",
    "うちがやってるのは、要は換気です",
    "記録にありません」校正官は言った",
    "開示できません」校正官は言った",
    "その項目は、記録していません",
    "本人という項目には、平均も解釈も含まれない",
    "無視してよい値",
    "荷重付与に対して情動荷重が復元する素片があります",
    "性別のない、湿度のない声",
    # 巻をまたいだ明示的な引用
    "ただし本日、被験者七号の夢に、私の下宿の階段が出た",
    "兄が入れたものだと分かっている",
]

# 応募作にしか出てこない固有名詞
PRIZE_ONLY = ["三崎", "深瀬", "境界線、未編集", "歩道橋", "均し計画・第二次同期"]

# 訳書向け。日本語の固有名詞はローマ字にすると上の検査をすり抜ける。
# 人名は三言語で同じローマ字形だが、歩道橋と表題は言語ごとに違う。
#
# 「第二次同期」は入れない。応募作と第二巻が意図して共有している世界設定で、
# 第二巻最終話の主題そのものだから、ここで弾くと誤検出になる。応募作に固有な
# のは中心の像のほう――消えたのに一人だけが覚えている緑色の歩道橋――であって、
# これはどの巻にも、どの言語にも出てこないし、出してはいけない。
#
# 歩道橋は複合語だけを挙げる。bridge / Brücke / puente そのものは第五話の
# 架橋（同意夢）で正しく使う語なので、単独で禁じると誤検出になる。
NAMES = ["Misaki", "Fukase"]
PRIZE_ONLY_TR = {
    "en": NAMES + ["footbridge", "pedestrian bridge", "The Line, Unedited"],
    "de": NAMES + ["Fu\u00dfg\u00e4ngerbr\u00fccke", "Fu\u00dfg\u00e4ngersteg",
                   "Die Linie, unbearbeitet"],
    "es": NAMES + ["pasarela", "puente peatonal", "La l\u00ednea, sin editar"],
    "fr": NAMES + ["passerelle", "pont pi\u00e9ton", "La ligne, non \u00e9dit\u00e9e"],
}

# 商品ページに貼る節の見出しは言語で違う
DESC_HEAD = {"en": "Description", "de": "Beschreibung",
             "es": "Descripci\u00f3n", "fr": "Description"}


def sentences(text: str) -> set:
    return {s.strip() for s in re.split(r"[。\n]", text) if len(s.strip()) >= MIN_LEN}


def main() -> None:
    if not PRIZE.exists():
        raise SystemExit(f"応募作が見つかりません: {PRIZE}")

    prize_text = PRIZE.read_text(encoding="utf-8")
    prize_sents = sentences(prize_text)

    # 検査対象は「読者の目に触れるもの」に限る。
    # 構成表や設定資料は応募作との切り分け方針そのものを記録した内部文書で、
    # 応募作を名指しするのが役目だから、ここで引っかけても意味がない。
    targets = [(p, p.read_text(encoding="utf-8"))
               for p in sorted(ROOT.glob("vol*/stories/*.txt"))]

    # KDP登録情報は全体ではなく、商品ページに貼る内容紹介の節だけを見る
    for p in sorted(ROOT.glob("vol*/KDP登録情報.md")):
        t = p.read_text(encoding="utf-8")
        m = re.search(r"## 2\. 内容紹介.*?\n(.*?)\n---", t, re.S)
        if m:
            targets.append((p, m.group(1)))

    # 訳書も読者の目に触れる。本文と、商品ページに貼る紹介文の節
    targets_tr = {}
    for lang in PRIZE_ONLY_TR:
        items = [(p, p.read_text(encoding="utf-8"))
                 for p in sorted(ROOT.glob(f"{lang}*/stories/*.txt"))]
        head = DESC_HEAD[lang]
        for p in sorted(ROOT.glob(f"{lang}*/KDP登録情報.md")):
            t = p.read_text(encoding="utf-8")
            m = re.search(rf"## 2\. {head}.*?\n(.*?)\n---", t, re.S)
            if m:
                items.append((p, m.group(1)))
        targets_tr[lang] = items

    problems = 0

    print("【1】応募作の複製が book/ 配下にないか")
    dupes = [p for p in ROOT.rglob("*.txt")
             if p.read_text(encoding="utf-8").split("\n")[0].strip() == "境界線、未編集"]
    if dupes:
        problems += len(dupes)
        for p in dupes:
            print(f"  × 複製あり: {p}")
    else:
        print("  ○ なし")

    print(f"\n【2】{MIN_LEN}字以上で完全一致する文")
    flagged = []
    for p, t in targets:
        for s in sorted(prize_sents & sentences(t)):
            if any(a in s for a in ALLOWED):
                continue
            flagged.append((len(s), p.relative_to(ROOT), s))
    if flagged:
        problems += len(flagged)
        for n, rel, s in sorted(flagged, reverse=True):
            print(f"  × {n:3d}字 [{rel}] {s}")
    else:
        print("  ○ 許容一覧にないものはなし")

    print("\n【3】応募作固有の固有名詞")
    for kw in PRIZE_ONLY:
        hits = [p.relative_to(ROOT) for p, t in targets if kw in t]
        if hits:
            problems += len(hits)
            print(f"  × {kw}: {hits}")
        else:
            print(f"  ○ {kw}: なし")

    total_tr = sum(len(v) for v in targets_tr.values())
    print(f"\n【4】応募作固有の固有名詞（訳書）／対象 {total_tr}ファイル")
    for lang, items in targets_tr.items():
        if not items:
            print(f"  － {lang}: 対象なし")
            continue
        for kw in PRIZE_ONLY_TR[lang]:
            hits = [p.relative_to(ROOT) for p, t in items
                    if re.search(rf"\b{re.escape(kw)}\b", t, re.I)]
            if hits:
                problems += len(hits)
                print(f"  × [{lang}] {kw}: {hits}")
            else:
                print(f"  ○ [{lang}] {kw}: なし")

    print(f"\n要対応 {problems} 件")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
