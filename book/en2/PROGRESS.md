# English Edition, Volume II — Progress

Translation of Volume II, `book/vol2/stories/` → `book/en2/stories/`.

Terminology is fixed in [`GLOSSARY.md`](../en/GLOSSARY.md), shared with Volume I.
Settle a term there before using it. Build with
`python3 book/tools/build_epub.py en2`.

---

## Status

| # | Japanese | English | Source | Words | State |
|---|---|---|---|---|---|
| I | 眠らない都市 | The Sleepless City | 4,336 | 2,017 | **done** |
| II | 胎夢 | Foundations | 4,240 | 1,949 | **done** |
| III | 共感注射 | The Empathy Injection | 4,432 | 1,864 | **done** |
| IV | 最後の夢職人 | The Last Craftsman | 4,226 | 1,931 | **done** |
| V | ＡＩは夢を見るか | Does the Machine Dream? | 3,963 | 1,796 | **done** |
| VI | 夢の犯罪 | Bodily Harm | 3,933 | 1,785 | **done** |
| VII | 消えた現実 | The Register | 3,982 | 1,890 | **done** |
| VIII | 夢の海 | The Sea of Dreams | 3,889 | 1,806 | **done** |
| IX | 明日の夢 | Tomorrow's Dream | 3,879 | 1,801 | **done** |
| X | 最後のバグ | The Last Bug | 3,843 | 1,819 | **done** |
| XI | 残差 | Residual | 3,906 | 1,844 | **done** |
| XII | 完了報告 | The Completion Report | 4,090 | 1,950 | **done** |

All twelve translated. Japanese 48,719 characters → English 22,452 words, a
ratio of 0.461 words per character — within 0.002 of Volume I's.

Counts in this table are written by `python3 book/tools/sync_en_counts.py en2`,
not by hand.

---

## Carried over from Volume I

Volume I set the style and it is not re-decided here. Roman section numerals,
double quotes, family name first, British spelling, Arabic numerals for the
loads. The recurring lines keep their Volume I wording exactly.

What is new in this volume is the Levelling Plan moving from background to
subject. Volume I mentions it; Volume II is about its completion.

---

## The award entry

Volume II is the volume that runs closest to『境界線、未編集』, because both
deal with the Second Synchronisation. They share the setting deliberately —
the half-shade, the Levelling Plan, the Second Synchronisation — and share no
text, no characters and no images.

The entry's central image is a green footbridge that one man goes on
remembering after it has gone. It appears nowhere in either volume, in either
language, and must not. `check_overlap.py` holds that line mechanically,
including the romanised forms in the English editions.

---

## Checks

```bash
python3 book/tools/sync_en_counts.py en2    # 語数の同期
python3 book/tools/check_en_terms.py        # 用語ゆれ（両巻）
python3 book/tools/check_overlap.py         # 応募作との重複（両巻・日英）
python3 book/tools/build_epub.py en2
python3 book/tools/build_cover.py en2
```
