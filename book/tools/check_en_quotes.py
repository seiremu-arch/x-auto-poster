#!/usr/bin/env python3
"""巻をまたいで引用される文が、一字一句同じかを検査する。

使い方:
    python3 book/tools/check_en_quotes.py

第二巻第八話『The Sea of Dreams』は、保管庫に残った記録として、
第一巻の各話と第二巻第六話に出てきた文をそのまま引用している。原文では
同じ文字列なので、訳文でも同じでなければ繋がりが切れる。通しで読んでも
「似ているが少し違う」は見落とすので、文字列一致で確かめる。

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


# (説明, 日本語の文字列, 英語の文字列, 出現すべきファイル)
QUOTES = [
    (
        "読み手の欄外記載（第一巻XII → 第二巻VIII）",
        "ただし本日、被験者七号の夢に、私の下宿の階段が出た",
        "However, the stair of my lodgings appeared today in Subject 7's dream.",
        ["en1/stories/12_silent-subject.txt", "en2/stories/08_sea-of-dreams.txt"],
    ),
    (
        "被害回復拒否の自由記述（第二巻VI → 第二巻VIII）",
        "兄が入れたものだと分かっている。分かっていても、思ってしまう",
        "I know it is something my brother put there. "
        "Knowing it, I feel it all the same.",
        ["en2/stories/06_bodily-harm.txt", "en2/stories/08_sea-of-dreams.txt"],
    ),
    (
        "辞退の自由記述（第一巻II → 第二巻VIII）",
        "蓮見律子は、待機期間中に自力で荷重を下げ、処置を辞退した",
        "Hasumi Ritsuko lowered her own load during the waiting period "
        "and withdrew from the procedure.",
        ["en1/stories/02_waiting-list.txt", "en2/stories/08_sea-of-dreams.txt"],
    ),
    (
        "翻訳の不採用候補（第一巻IV → 第二巻VIII）",
        "光・痛み・閉じる",
        "light, pain, closing",
        ["en1/stories/04_the-translator.txt", "en2/stories/08_sea-of-dreams.txt"],
    ),
    (
        "翻訳の不採用候補・その二（第一巻IV → 第二巻VIII）",
        "動く・止まる・分からない",
        "moving, stopping, not knowing",
        ["en1/stories/04_the-translator.txt", "en2/stories/08_sea-of-dreams.txt"],
    ),
]


def main() -> int:
    problems = 0

    for label, ja, en, paths in QUOTES:
        missing = []
        for rel in paths:
            p = ROOT / rel
            if not p.exists():
                missing.append(f"{rel}（ファイルなし）")
                continue
            if en.lower() not in p.read_text(encoding="utf-8").lower():
                missing.append(rel)

        if missing:
            problems += len(missing)
            print(f"× {label}")
            print(f"    英文: {en}")
            for m in missing:
                print(f"    見つからない: {m}")
        else:
            print(f"○ {label}")

        # 原文側も同じ文字列であることを確かめる。
        # 題名が違うので、巻と先頭の番号で対応する原文を引く
        ja_hits = 0
        for rel in paths:
            en_vol, _, name = rel.split("/")
            ja_vol = {"en1": "vol1", "en2": "vol2"}[en_vol]
            hits = sorted((ROOT / ja_vol / "stories").glob(f"{name[:2]}_*.txt"))
            if hits and normalise(ja) in normalise(
                    hits[0].read_text(encoding="utf-8")):
                ja_hits += 1
        if ja_hits != len(paths):
            problems += 1
            print(f"    ※ 原文側は {ja_hits}/{len(paths)} ファイルにしかない"
                  f"（訳文を揃える前に原文を確認すること）")

    print()
    print(f"要対応 {problems} 件" if problems else "引用の不一致なし")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
