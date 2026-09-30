# 企画書 — 英語版『The Quietest Voice』

日本語版 `books/inner-voice/` の**書き直し**であって、翻訳ではない
(方針と反証条件は Vault `fcfb3b0ebf`)。芯・章構成・実践の番号は揃え、場面と例を差し替える。

## 書誌

| 項目 | 内容 |
| --- | --- |
| Title | The Quietest Voice |
| Subtitle | Seven practices for telling your own voice from the noise in your head |
| Author | Kazu A. Suzuki(日本語版と同一表記) |
| 言語 | 英語(Amazon.com を主戦場にする) |
| 分量 | 14,500 words 前後(日本語版 33,075字 ÷ 実測 2.28字/word。→ Vault `fcfb3b0ebf` の追記) |
| 想定価格 | $4.99(70%ロイヤリティの範囲は $2.99〜$9.99) |

## 芯にする一文

> Your quietest voice never gets louder. So the only way to hear it is to get quieter yourself.

日本語版の「内なる声は大きくならない。だから、こちらが静かになるしかない」の英語版。
どちらかを直すときは両方を直す(`--check` が3か所の一致を見る)。

## 日本語版から動かさないもの

- 四つの声(anxious / should / borrowed / quietest)とその見分け方
- 二つの基準 — **speed**(order of arrival)と **body**(loosens / tightens)
- 七つの実践の中身と番号。所要時間も変えない
- 章の順番と、各章が担う主張
- 約束しないこと(効果の断定をしない / 医療の代替にしない / 検証できない語を使わない)

## 日本語版から差し替えるもの

場面と例だけ。差し替えたら、その場面が担う声の種類を `loop.py capture --tag book-log` に残す。

| 章 | 日本語版の場面 | 英語版の場面 |
| --- | --- | --- |
| 序章 | 眠れない夜に二十行書く | 同じ(文化に依存しない) |
| 1 | 金曜の飲みの誘い「その仕事、辞めたら?」 | a friend at dinner: "You should just quit." |
| 2 | 誘いに即答した三日後 | replying "Sure, I'm in" to a group text in three seconds |
| 3 | 内見した部屋の玄関で肩が上がる | the third apartment viewing — perfect on paper, shoulders rise in the hallway |
| 4 | レンジの二分・信号待ち | the microwave, the elevator, the checkout line |
| 5 | 会議で部長に数字を指摘される | a manager flags a number in a meeting of seven |
| 6 | 三年ぶりの分岐点は金曜の夜、誘いを断った | 同じ形(declining one invitation) |
| 7 | 三週間目に何も来なくなった | 同じ(文化に依存しない) |

## 出す前に確かめること

- **タイトルの重複。** Amazon.com で "The Quietest Voice" を検索し、同名・近似の本が
  上位にいないか見る。いたら副題で差をつけるか、タイトルを変える
- 実践の言い方が命令形になりすぎていないか(日本語版は「〜してみる」の距離を保っている)
- 免責の文が、米国の読者にも医療行為の否定と読まれない書き方になっているか

## 現在地

- [x] 企画・構成(日本語版からの対応表)
- [x] 序章 The loudest voice is not always right
- [x] 第1章 How many voices are talking
- [x] 第2章 Speed
- [x] 第3章 The body
- [x] 第4章 Making room
- [x] 第5章 Writing to listen
- [x] 第6章 Deciding small
- [x] 第7章 The days you hear nothing
- [x] 終章 Quiet is not a destination
- [x] 巻末(実践一覧・免責・あとがき)
- [x] 通しの推敲(禁止語・絶対表現・章ごとの語数比・40語超えの文)
- [x] EPUB(`--epub`)/ KDP登録シート(`LISTING.md`)
- [ ] 表紙(日本語版と同じ仕様で英文に)
- [ ] タイトルの重複確認(Amazon.com)/ KDP登録
