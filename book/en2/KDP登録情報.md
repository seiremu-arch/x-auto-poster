# 英語版『The Levelling』KDP登録情報

第二巻の英語版です。KDPの登録画面にそのままコピーして貼れる形でまとめてあります。
貼り付ける中身は英語、説明は日本語で書いてあります。

日本語版とも、英語版第一巻とも**別の本**として登録します。

---

## 1. 本の詳細

| 項目 | 内容 |
|---|---|
| Book Title | The Levelling |
| Subtitle | The Dream Editing Bureau, Book Two |
| Series | The Dream Editing Bureau（Book 2） |
| 巻番号 | 2 |
| Author | Kazu A. Suzuki |
| 出版言語 | English |
| ISBN | 不要（KDPが内部管理番号を自動付与） |

シリーズ名は英語版第一巻と**一字一句同じ**にしてください。違うとシリーズページが
別々に作られます。`The Dream Editing Bureau` です。

---

## 2. Description（そのまま貼り付け可）

The Levelling. The name of a state programme that brings the weight of a million people's memories towards the mean, night by night.

While you sleep, the brain softens a memory, re-joins it, and sets it again. Dream editing intervenes in those few seconds to lower the weight, and the most that may be moved in one night is 0.05. In the field they call it the half-shade.

Where Volume I, The Dream Editing Bureau, was about a technician and a client facing each other one to one, these twelve stories come after the technique has become an industry, then a scheme, and then the size of a country.

- A society where three hours of sleep is enough, and a company that sells other people's feelings in the forty minutes left over — "The Sleepless City"
- A prenatal procedure forming security, trust and curiosity in a foetus. What it works on was not the children — "Foundations"
- The grief transferred into an offender has already been taken off the bereaved at the moment it was harvested — "The Empathy Injection"
- Automation rate 98.4 per cent, and the last technician carrying the remaining 1.6 — "The Last Craftsman"
- A man made heavier over seven nights without his consent, who refuses to be put back — "Bodily Harm"
- A fire in which nineteen people died, which nobody remembers and which is written down nowhere — "The Register"

There are no villains. There are only people doing their work correctly in their own departments. Allocation revises for utilisation, Fault Analysis for the cost of correcting, Technical Management for want of staff. There is no trace of their having been in touch.

What happened when the three reasonings fell into the same quarter becomes clear in the final story, "The Completion Report".

Each story stands alone. Volume I is not required.

CONTENTS
I. The Sleepless City
II. Foundations
III. The Empathy Injection
IV. The Last Craftsman
V. Does the Machine Dream?
VI. Bodily Harm
VII. The Register
VIII. The Sea of Dreams
IX. Tomorrow's Dream
X. The Last Bug
XI. Residual
XII. The Completion Report

Approximately 22,500 words.

---

## 3. Keywords（7つ）

1. `literary science fiction`
2. `near future dystopia`
3. `linked short stories`
4. `bureaucracy dystopian fiction`
5. `memory and identity speculative fiction`
6. `quiet science fiction short story collection`
7. `japanese science fiction in english`

英語版第一巻とほぼ同じです。5番だけ、第二巻の主題（個人ではなく制度の側）に
寄せてあります。

**入れてはいけないもの**：他の作家名や既存作品名。Amazonの規約で禁じられています。

---

## 4. Categories（最大3つ）

1. Fiction → Science Fiction → Short Stories
2. Fiction → Literary
3. Fiction → Science Fiction → Dystopian

第一巻と同じにしてあります。シリーズは同じ棚に並んだほうが見つけてもらいやすい
ためです。

---

## 5. 価格とロイヤリティ

| 項目 | 推奨 |
|---|---|
| ロイヤリティ | 70%プラン |
| 価格 | $3.99（米国） |
| KDPセレクト | 登録する |

第一巻と同額にしてあります。シリーズで価格が揃っていないと、二冊目で止まる
読者が出ます。

---

## 6. アップロードするファイル

| 用途 | ファイル |
|---|---|
| 原稿 | `book/dist/The Levelling.epub` |
| 表紙 | `book/dist/cover_en2.jpg`（1600×2560px、1.6:1） |

```bash
python3 book/tools/build_epub.py en2
python3 book/tools/build_cover.py en2
```

表紙は四冊とも同じ乱数の種で帯を描いています。第一巻は帯の高さがばらついていて
赤い帯が一本はっきり残り、第二巻は高さが揃って赤が沈んでいます。四冊を並べると、
一冊目に残っていた一本が二冊目で消えかけて見えます。分散が下がったのか、
見えなくなったのかを区別できないという最終話の主題を、そのまま表紙の差に
してあります。

（検証: 日本語版第二巻の表紙と、字のない下半分を画素比較して差分ゼロを確認済み）

---

## 7. 翻訳について

全十二話を日本語から英語に書き直したものです。原文48,719字 →
英文22,452 words（比0.461）。第一巻の0.463とほぼ同じで、巻をまたいだ密度の
ばらつきはありません。

用語は `book/en/GLOSSARY.md` で第一巻と共有しています。第二巻の最終話
「The Completion Report」は、第一巻第十二話の読み手が四十一年前に書いた
記録を引用します。訳文がずれると巻をまたいだ繋がりが切れるので、
`check_en_quotes.py` で文字列一致を機械で確かめています。

---

## 8. 出版前チェックリスト

- [x] 全十二話の翻訳を終えた
- [x] `python3 book/tools/check_en_structure.py` が0件で通ることを確認した
- [x] `python3 book/tools/check_en_terms.py` が0件で通ることを確認した
- [x] `python3 book/tools/check_en_quotes.py` が0件で通ることを確認した
- [x] `python3 book/tools/check_overlap.py` が0件で通ることを確認した
- [x] 表紙の帯が日本語版第二巻と一致していることを画素比較で確認した
- [ ] Kindle Previewerで横組み表示を三機種確認した
- [ ] Description を貼り付けた
- [ ] Keywords 7つを入れた
- [ ] Categories を3つ選んだ
- [ ] シリーズ名を第一巻と一字一句同じにした
- [ ] 価格とロイヤリティを設定した
- [ ] KDPセレクトの可否を決めた

---

## 9. 四冊の対応

| | 日本語 | English |
|---|---|---|
| 第一巻 | 夢編集局（十二の夜） | The Dream Editing Bureau (Twelve Nights) |
| 第二巻 | 均し（夢編集局 第二集） | The Levelling (The Dream Editing Bureau, Book Two) |

星新一賞応募作『境界線、未編集』は、この四冊のどれにも入っていません。
`novel/` にあり、未発表のままです。第二巻は応募作と同じ「第二次同期」を
扱いますが、共有しているのは世界設定だけで、本文・登場人物・中心の像は
重なりません。`check_overlap.py` が日英の両方でこれを機械的に見ています。
