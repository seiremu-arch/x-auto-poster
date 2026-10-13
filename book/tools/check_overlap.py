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

    print(f"\n要対応 {problems} 件")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
