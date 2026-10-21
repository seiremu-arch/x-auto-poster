# 英語版『The Dream Editing Bureau』KDP登録情報

第一巻の英語版です。KDPの登録画面にそのままコピーして貼れる形でまとめてあります。
貼り付ける中身は英語、説明は日本語で書いてあります。

日本語版とは**別の本**として登録します。同じ本の別言語版は、KDPでは
それぞれ独立した商品になります。

---

## 1. 本の詳細

| 項目 | 内容 |
|---|---|
| Book Title | The Dream Editing Bureau |
| Subtitle | Twelve Nights |
| Series | The Dream Editing Bureau（Book 1） |
| 巻番号 | 1 |
| Author | Kazu A. Suzuki |
| 出版言語 | English |
| ISBN | 不要（KDPが内部管理番号を自動付与） |

**翻訳者の欄は空のままで構いません。** KDPには Translator を入れる欄が
ありますが、著者本人が自分の作品を別言語で書き直した場合、入れる義務は
ありません。入れたい場合は著者名と同じものを入れます。

---

## 2. Description（そのまま貼り付け可）

Dreams cannot be erased. They can only be made lighter.

While you sleep, the brain softens a memory, re-joins it, and sets it again. Dream editing is the work of attending those few seconds and altering the hand that does the re-joining, very slightly.

All it can do is lower the weight of a memory. The most that may be moved in one night is 0.05. In the field they call it the half-shade.

The ceiling is not there because of a limit in the technique. Thin a memory too fast and the trace of the rewriting goes with it. While the trace remains, a person can still tell themselves: this is an edited dream. What the ceiling protects is not the dream of the sleeping person. It is the room left afterwards, on waking, to doubt one's own memory.

Twelve linked stories, set in a country where that technique has reached into every corner of ordinary life.

- A girl of thirteen who asks for her nightmare to be left alone — "Half-Shade"
- A woman who waits four years and seven months, and declines the procedure on the day her turn comes — "The Waiting List for Forgetting"
- A widow given the apology her husband never managed to say, synthesised from his diaries, and a daughter who calls it a forgery — "The Bequest"
- A mother who is read a clear, comforting story each month, translated from the dreams of a son who has no language — "The Translator"
- A technician who raises an offender's remorse from 0.07 to 0.81 over fifteen nights — "The Sentence"
- A workplace where grief processing is compulsory within forty-eight hours, and one man who will not take it — "Grief by Proxy"

There are no villains. There are only people doing their work correctly, according to the rules, and one field the rules never provided.

Each story stands alone. Read on, and what this country has been calling happiness comes gradually into view.

CONTENTS
I. Half-Shade
II. The Waiting List for Forgetting
III. The Bequest
IV. The Translator
V. The Second-Person Dream
VI. Dream Tax
VII. Grief by Proxy
VIII. The Sentence
IX. The Right Not to Wake
X. Inheritance
XI. Happiness Index 98
XII. The Silent Subject

Approximately 24,000 words.

---

## 3. Keywords（7つ）

KDPは7枠あります。以下をそのまま一枠ずつ入れてください。

1. `literary science fiction`
2. `near future dystopia`
3. `linked short stories`
4. `memory and identity`
5. `quiet speculative fiction short story collection`
6. `bureaucracy dystopian fiction`
7. `japanese science fiction in english`

**入れてはいけないもの**：他の作家名や既存作品名。Amazonの規約で禁じられており、
最悪の場合アカウントに影響します。日本語版と同じ注意です。

---

## 4. Categories（最大3つ）

1. Fiction → Science Fiction → Short Stories
2. Fiction → Literary
3. Fiction → Science Fiction → Dystopian

日本語版と考え方は同じです。一つ目を主戦場に置き、残りで文芸の読者にも
届くようにしています。英語のSF短編カテゴリーは日本語版より競合が強いので、
二つ目の Literary のほうが順位は取りやすいはずです。

---

## 5. 価格とロイヤリティ

| 項目 | 推奨 |
|---|---|
| ロイヤリティ | 70%プラン |
| 価格 | $3.99（米国） |
| KDPセレクト | 登録する |

70%プランが使えるのは **$2.99〜$9.99** の範囲です。$3.99 はこの分量の
短編集として標準的で、一冊あたり約$2.6が入ります。

他の国の価格は、米国価格から自動換算させて構いません。

KDPセレクトの90日間独占は、日本語版とは別に数えられます。日本語版を
セレクトに入れているかどうかは、英語版の判断に影響しません。

---

## 6. アップロードするファイル

| 用途 | ファイル |
|---|---|
| 原稿 | `book/dist/The Dream Editing Bureau.epub` |
| 表紙 | `book/dist/cover_en1.jpg`（1600×2560px、1.6:1） |

原稿は**横組み・左から右**で組んであります。日本語版の縦組み設定
（`vertical-rl` / `page-progression-direction="rtl"`）は英語版には入って
いません。`dc:language` も `en` です。

表紙は日本語版と**同じ乱数の種**で帯を描いているため、帯の並びが一本も
違いません。字だけがラテン文字の横組みに変わります。二冊を並べたときに
同じ本の別の版だと分かるようにしてあります。
（検証: 文字のない下半分を画素比較して差分ゼロを確認済み）

```bash
python3 book/tools/build_epub.py en1
python3 book/tools/build_cover.py en1
```

---

## 7. 翻訳について

全十二話を日本語から英語に書き直したものです。原文51,718字 →
英文23,782 words（比0.460）。

用語は `book/en/GLOSSARY.md` で固定しています。十二話が一つの造語体系を
共有しているため、同じ語が三通りに訳されると世界が成立しなくなります。
日本語が意図的に繰り返している文は、英語でも一字一句同じに繰り返しています。

| 日本語 | English |
|---|---|
| 半色 | half-shade |
| 素片 | fragment |
| 情動荷重 | affective load |
| 校正官 | the Proofreader |
| 照合機 | the Comparator |
| 残差 | residual |
| 均し計画 | the Levelling Plan |

綴りは英国式（-ise / colour / per cent）で統一しました。

---

## 8. 出版前チェックリスト

- [x] 全十二話の翻訳を終えた
- [x] `python3 book/tools/check_en_terms.py` が0件で通ることを確認した
- [x] `python3 book/tools/check_overlap.py` が0件で通ることを確認した
- [x] 表紙の帯が日本語版と一致していることを画素比較で確認した
- [ ] Kindle Previewerで横組み表示を三機種確認した
- [ ] `en1/stories/` に応募作『境界線、未編集』由来の文が無いことを目視確認した
- [ ] Description を貼り付けた
- [ ] Keywords 7つを入れた
- [ ] Categories を3つ選んだ
- [ ] 価格とロイヤリティを設定した
- [ ] KDPセレクトの可否を決めた
