#!/usr/bin/env python3
"""巻をまたいで引用される文が、一字一句同じかを検査する。

使い方:
    python3 book/tools/check_en_quotes.py

第二巻第八話（夢の海）は、保管庫に残った記録として、第一巻の各話と
第二巻第六話に出てきた文をそのまま引用している。原文では同じ文字列なので、
訳文でも同じでなければ繋がりが切れる。通しで読んでも「似ているが少し違う」は
見落とすので、文字列一致で確かめる。言語ごとに別々に見る。

日本語側で同じであることも併せて確認する。原文がずれていれば、
訳文を揃えても意味がない。ただし、地の文と記録の抜粋では中黒と読点が
入れ替わる（光、痛み、閉じる ↔ 光・痛み・閉じる）。これは文体の違いで
あって不一致ではないので、区切り記号は正規化してから比べる。
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def normalise(s: str) -> str:
    """中黒と読点の違いを吸収する。地の文と記録の抜粋で入れ替わるため。"""
    return s.replace("\u30fb", "\u3001")


# (説明, 日本語の文字列, {言語: 訳文}, 出現すべきファイル（言語接頭辞なし）)
QUOTES = [
    (
        "読み手の欄外記載（第一巻XII → 第二巻VIII）",
        "ただし本日、被験者七号の夢に、私の下宿の階段が出た",
        {
            "en": "However, the stair of my lodgings appeared today "
                  "in Subject 7's dream.",
            "de": "Allerdings erschien heute im Traum von Proband sieben "
                  "die Treppe meiner Pension.",
        },
        [("1", "12"), ("2", "08")],
    ),
    (
        "被害回復拒否の自由記述（第二巻VI → 第二巻VIII）",
        "兄が入れたものだと分かっている。分かっていても、思ってしまう",
        {
            "en": "I know it is something my brother put there. "
                  "Knowing it, I feel it all the same.",
            "de": "Ich wei\u00df, dass es etwas ist, das mein Bruder "
                  "hineingelegt hat. Ich wei\u00df es, und ich empfinde "
                  "es trotzdem.",
        },
        [("2", "06"), ("2", "08")],
    ),
    (
        "辞退の自由記述（第一巻II → 第二巻VIII）",
        "蓮見律子は、待機期間中に自力で荷重を下げ、処置を辞退した",
        {
            "en": "Hasumi Ritsuko lowered her own load during the waiting "
                  "period and withdrew from the procedure.",
            "de": "Hasumi Ritsuko hat w\u00e4hrend der Wartezeit ihre Last "
                  "aus eigener Kraft gesenkt und ist von der Bearbeitung "
                  "zur\u00fcckgetreten.",
        },
        [("1", "02"), ("2", "08")],
    ),
    (
        "翻訳の不採用候補（第一巻IV → 第二巻VIII）",
        "光・痛み・閉じる",
        {"en": "light, pain, closing", "de": "Licht, Schmerz, Schlie\u00dfen"},
        [("1", "04"), ("2", "08")],
    ),
    (
        "翻訳の不採用候補・その二（第一巻IV → 第二巻VIII）",
        "動く・止まる・分からない",
        {"en": "moving, stopping, not knowing",
         "de": "Bewegen, Anhalten, Nichtwissen"},
        [("1", "04"), ("2", "08")],
    ),
]

LANGS = ["en", "de", "es"]


def main() -> int:
    problems = 0

    for lang in LANGS:
        if not (ROOT / f"{lang}1").is_dir():
            continue
        print(f"【{lang}】")
        for label, ja, trs, slots in QUOTES:
            tr = trs[lang]
            missing = []
            for vol, num in slots:
                hits = sorted((ROOT / f"{lang}{vol}" / "stories")
                              .glob(f"{num}_*.txt"))
                if not hits:
                    missing.append(f"{lang}{vol}/{num}（ファイルなし）")
                    continue
                if tr.lower() not in hits[0].read_text(
                        encoding="utf-8").lower():
                    missing.append(str(hits[0].relative_to(ROOT)))

            if missing:
                problems += len(missing)
                print(f"  × {label}")
                print(f"      訳文: {tr}")
                for m in missing:
                    print(f"      見つからない: {m}")
            else:
                print(f"  ○ {label}")

    # 原文側も同じ文字列であることを確かめる。訳文を揃える前に原文を見る
    print("【原文】")
    for label, ja, _trs, slots in QUOTES:
        hits_n = 0
        for vol, num in slots:
            hits = sorted((ROOT / f"vol{vol}" / "stories").glob(f"{num}_*.txt"))
            if hits and normalise(ja) in normalise(
                    hits[0].read_text(encoding="utf-8")):
                hits_n += 1
        if hits_n != len(slots):
            problems += 1
            print(f"  × {label}: 原文側は {hits_n}/{len(slots)} ファイルにしかない")
        else:
            print(f"  ○ {label}")

    print()
    print(f"要対応 {problems} 件" if problems else "引用の不一致なし")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
