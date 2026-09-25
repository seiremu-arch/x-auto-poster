# KDP listing — *The Last Ledger: An Estate in Three Parts* (English edition)

The English edition is a separate KDP title (its own ASIN), not a variant of the
Japanese one. Everything below can be pasted straight into the KDP form.
**Two things are still to do: the cover and the price.**

---

## 1. Files

| File | Use |
| --- | --- |
| `The_Last_Ledger_1_An_Estate_in_Three_Parts.epub` | **Upload this to KDP** (horizontal, left-to-right) |
| `The_Last_Ledger_1_An_Estate_in_Three_Parts.md` | The whole text in one file, for proofreading |

EPUB3, reflowable, `dc:language` `en`, `page-progression-direction="ltr"`.
Source: `../manuscript-en/*.md`. Style guide and glossary: `../TRANSLATION.md`.

```bash
python3 writing/last-ledger/build_epub.py --english
```

---

## 2. Book details

**Language**

```
English
```

**Book title / Subtitle**

```
The Last Ledger
An Estate in Three Parts
```

**Series / Number**

```
The Last Ledger / 1
```

**Author**

```
First name: Kazu A.
Last name: Suzuki
```

**Contributors** — none. (If you want to credit the translation, add a
*Translator* entry here; the book itself only says it was originally published
in Japanese.)

**Description** (about 230 words; KDP allows 4,000 characters)

```
He left three hundred million yen. Each heir may take only one third of it.

Shuji Kamiya spent thirty years as a bank loan officer in Japan, and one year
hiding from his wife that he lost most of his retirement money to an overseas
investment scheme. Then an old ledger arrives in the post, sent by a man he met
once, thirty years ago: Soichiro Tono, whose company Kamiya's bank cut off in 1996.

The letter with it says: "If I died falling down the stairs, it was not an
accident."

It was posted the day before Soichiro fell to his death on the stairs of his
empty family home.

His will divides the estate into land, a business and cash, and makes each of
three heirs choose one in a sealed envelope. If two choose the same thing, it
goes to charity. In the statement of wishes he left one line: "To anyone who
staked it all on one thing, leave not a single yen."

Named as executor, Kamiya starts counting. The land drops from a hundred million
to twenty million overnight. Money has vanished overseas. And on the staircase
wall there are four screw holes where a handrail used to be.

A quiet, exact financial mystery about inheritance, fraud, and a crime that
consists of doing nothing at all. Book One of The Last Ledger.
```

**Keywords** (up to 7)

```
japanese mystery novel
financial crime fiction
inheritance mystery
family secrets japan
investment fraud thriller
translated fiction from japanese
literary crime novel
```

**Categories** (KDP lets you pick up to 3)

```
Kindle eBooks › Literature & Fiction › Mystery, Thriller & Suspense › Mystery › International Mystery & Crime
Kindle eBooks › Mystery, Thriller & Suspense › Thrillers & Suspense › Financial
Kindle eBooks › Literature & Fiction › World Literature › Asian › Japanese
```

**Adult content** No
**Territories** All territories

---

## 3. ★ AI disclosure (required)

KDP asks whether the book contains AI-generated content (text, images,
translations). This English edition was **translated with AI assistance**, so
answer **Yes** for *Translations* (and for text, if applicable to the original).
Answering this incorrectly can get a title removed.

---

## 4. ★ Cover (not done)

- Size 1600 × 2560 px (ratio 1 : 1.6)
- JPEG or TIFF, RGB, 72 dpi or more, under 50 MB
- Text: **THE LAST LEDGER** / *An Estate in Three Parts* / **Kazu A. Suzuki**
- Use the same image as the Japanese edition so the two read as one series.
  The ideas in `KDP-出版情報.md` (four screw holes / the stitched spine of the
  ledger / the steep stairs from below; navy and unbleached white; no people)
  work unchanged. The 土 character can stay as a small mark if you like.

---

## 5. Price

- About 37,700 words — a short novel, roughly 150–170 pages in print terms
- 70% royalty band: US$2.99–9.99. For a Book One by an author new to English
  readers, **US$2.99–3.99** is the usual place to start
- KDP Select (exclusive) is set per title, so the Japanese and English editions
  can be decided separately

---

## 6. Pre-publication checklist

- [x] Author set to `Kazu A. Suzuki` in the EPUB (`dc:creator`, title page, copyright page)
- [x] EPUB validates as XML; `mimetype` stored first
- [ ] Cover image (1600 × 2560 px)
- [ ] Check in the KDP previewer: left-to-right, paragraph indents, the ※ scene breaks
- [ ] Contents page links to every chapter
- [ ] The ledger's newest line reads *February 10, 2026…* — the only Western-calendar
      line among era years (this replaces the kanji/Arabic contrast of the Japanese edition)
- [ ] AI disclosure answered (section 3)
- [ ] Decide whether to add a Book Two teaser at the end of the description
