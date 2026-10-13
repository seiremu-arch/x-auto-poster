# English Edition — Progress

Translation of Volume I, `book/vol1/stories/` → `book/en1/stories/`.

Terminology is fixed in [`GLOSSARY.md`](GLOSSARY.md). Settle a term there before
using it. Build with `python3 book/tools/build_epub.py en1`.

---

## Status

| # | Japanese | English | Source | Words | State |
|---|---|---|---|---|---|
| I | 半色 | Half-Shade | 4,997 | 2,431 | **done** |
| II | 忘却の順番待ち | The Waiting List for Forgetting | 4,540 | 2,101 | **done** |
| III | 夢の遺言 | The Bequest | 4,555 | 2,063 | **done** |
| IV | 夢の翻訳者 | The Translator | 3,915 | 1,712 | **done** |
| V | 二人称の夢 | The Second-Person Dream | 3,454 | 1,529 | **done** |
| VI | 夢税 | Dream Tax | 3,391 | 1,556 | **done** |
| VII | 涙の代筆 | Grief by Proxy | 4,476 | 2,038 | **done** |
| VIII | 夢裁判 | The Sentence | 4,577 | 2,064 | **done** |
| IX | 目覚めない権利 | The Right Not to Wake | 4,503 | 2,050 | **done** |
| X | 夢の相続 | Inheritance | 4,587 | 2,143 | **done** |
| XI | 幸福指数九八 | Happiness Index 98 | 4,218 | 2,026 | **done** |
| XII | 沈黙の被験者 | The Silent Subject | 4,508 | 2,210 | **done** |

All twelve translated. Japanese 51,721 characters → English 23,923 words, a
ratio of 0.463 words per character.

Counts in this table are written by `python3 book/tools/sync_en_counts.py`, not
by hand. Run it after each story.

---

## Decisions already made in story I

Story I is the style benchmark. Later stories follow it rather than re-deciding.

**Section numbers.** Roman numerals, centred, one per section. The Japanese uses
漢数字 and the English title line already carries a Roman numeral, so the two
could collide; the title keeps "I." with a full stop and the section heads do not.

**The 0.05 explanation.** Rendered as "What the ceiling protects is not the dream
of the sleeping person. It is the room left afterwards, on waking, to doubt one's
own memory." This is the book's spine and recurs in later stories; it must come
out the same way each time.

Note that the Japanese edition reworded this sentence to keep it clear of the
award entry. The English follows the reworded Japanese, not the entry.

**Dialogue.** Double quotes, no em-dash interruptions. The Japanese 「」 carry no
attribution much of the time; English needs a little more, but add only what the
reader cannot otherwise follow.

**The Proofreader's pause.** "A pause set at the structural break in the sentence."
Used sparingly. The Japanese edition cut this from eight occurrences to three, and
the English keeps the same three.

**Names.** Family name first, no macrons. Suginoto Saya, not Saya Suginoto.
Consistent with the setting being plainly Japanese.

---

## Checks

`python3 book/tools/check_en_terms.py` holds the terminology read-through. It
applies the forbidden variants of every fixed term in `GLOSSARY.md`, plus the
British-spelling and typographic rules, across all twelve files. Currently clean.

The check is only worth what its patterns are worth, so it was verified by
feeding it a line of deliberate errors (engineer / half shade / Proof-reader /
emotional load / residue / percent / realized / color / gray / 〇・〇五) and
confirming it caught each one.

`python3 book/tools/check_en_structure.py` compares the English against the
Japanese section by section, by paragraph count. This is the check that matters
most: the failure a translation actually suffers is not a mistranslated word but
a dropped paragraph, and reading through does not reliably catch one.

**It found one.** Ten paragraphs were missing from section III of story I — the
whole afternoon scene with the section chief, including one of the book's
recurring lines ("What we do here is ventilation, basically") and Kaji's reply,
"The window. It is that girl's window." The term checker could not see it,
because nothing that was there was wrong. Restored.

It also found a sentence in story V that is in the English and not in the
Japanese ("The procedure took forty minutes"). Removed — this is a translation,
so an invented sentence is a defect even when it reads well.

`python3 book/tools/check_overlap.py` separately confirms that no sentence from
the award entry has reached the published text, English or Japanese.

---

## Remaining work after the twelve stories

- [x] English KDP listing: title, description, keywords, categories —
      `book/en1/KDP登録情報.md`
- [x] Cover with English title — `book/dist/cover_en1.jpg`. Same random seed as
      the Japanese cover, so the bands are identical band for band; only the type
      changes. Verified by comparing the typeless lower half pixel for pixel.
- [x] Read the twelve through for terminology drift — mechanised, see Checks
- [ ] Decide whether Volume II follows
