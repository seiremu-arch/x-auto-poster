# 企画書 — ドイツ語版『Die leiseste Stimme』

日本語版 `books/inner-voice/` の**書き直し**であって、翻訳ではない
(方針と反証条件は Vault `899744d0ff`)。芯・章構成・実践の番号は揃え、
場面と例、そして**読者との距離**を決め直す。

## 書誌

| 項目 | 内容 |
| --- | --- |
| Titel | Die leiseste Stimme |
| Untertitel | Sieben Übungen, um die eigene Stimme vom Lärm im Kopf zu unterscheiden |
| Autor | Kazu A. Suzuki(日本語版・英語版と同一表記) |
| 言語 | ドイツ語(Amazon.de を主戦場にする) |
| 分量 | 14,400 words 前後(日本語版 33,075字 ÷ 実測 2.30字/word。→ Vault `899744d0ff` の追記) |
| 想定価格 | 4,99 €(70%ロイヤリティの範囲は 2,99〜9,99 €) |

## 芯にする一文

> Deine leiseste Stimme wird nicht lauter. Also bleibt nur, selbst leiser zu werden.

日本語版「内なる声は大きくならない。だから、こちらが静かになるしかない」の
ドイツ語版。三言語のどれかを直すときは三つとも直す(`--check` が一致を見る)。

## 読者との距離

**`du` で書く**(→ Vault `7586251f89`)。`Sie` では、この本が守っている距離が作れない。

`du` にしたことで命令形が増えるのがいちばんありそうな失敗なので、
手順の節の外では命令形を使わない。`STYLE.md` に検査を置いた。

## 日本語版から動かさないもの

- 四つの声とその見分け方 — die ängstliche Stimme / die Sollte-Stimme /
  die geborgte Stimme / die leiseste Stimme
- 二つの基準 — **Geschwindigkeit**(Reihenfolge)と **der Körper**
  (es löst sich / es zieht sich zusammen)
- 七つの実践の中身と番号。所要時間も変えない
- 章の順番と、各章が担う主張
- 約束しないこと(効果の断定をしない / 医療の代替にしない / 検証できない語を使わない)

## 日本語版から差し替えるもの

場面と例だけ。差し替えたら、その場面が担う声の種類を `loop.py capture --tag book-log` に残す。

| 章 | 日本語版の場面 | ドイツ語版の場面 |
| --- | --- | --- |
| 序章 | 眠れない夜に二十行書く | 同じ(文化に依存しない) |
| 1 | 金曜の飲みの誘い「その仕事、辞めたら?」 | Freitagabend beim Essen: „Dann kündige doch einfach." |
| 2 | 誘いに即答した三日後 | „Bin dabei!" in drei Sekunden in eine Gruppe getippt |
| 3 | 内見した部屋の玄関で肩が上がる | die dritte Wohnungsbesichtigung(そのまま使う) |
| 4 | レンジの二分・信号待ち | Mikrowelle, Aufzug, Kasse, Zähneputzen |
| 5 | 会議で部長に数字を指摘される | ein Meeting mit sieben Leuten, eine falsche Zahl |
| 6 | 三年ぶりの分岐点は金曜の夜、誘いを断った | 同じ形(eine Einladung abgesagt) |
| 7 | 三週間目に何も来なくなった | 同じ(文化に依存しない) |

第3章の内見は、ドイツ語圏でも住まい探しが読者の生活に入っているのでそのまま使う。

## 出す前に確かめること

- **タイトルの重複。** Amazon.de で „Die leiseste Stimme" を検索し、同名・近似の本が
  上位にいないか見る。いたら副題で差をつけるか、タイトルを変える
- 命令形が手順の節の外に出ていないか(`STYLE.md` の検査)
- 免責の文が、ドイツの読者にも医療行為の否定と読まれない書き方になっているか

## 現在地

- [x] 企画・構成(日本語版からの対応表)/ 読者との距離の判断
- [x] Vorwort
- [x] Kapitel 1 Wie viele Stimmen reden gerade
- [x] Kapitel 2 Nach der Geschwindigkeit unterscheiden
- [x] Kapitel 3 Im Körper unterscheiden
- [x] Kapitel 4 Raum schaffen
- [x] Kapitel 5 Schreiben, um zu hören
- [x] Kapitel 6 Klein entscheiden
- [x] Kapitel 7 Die Tage, an denen du nichts hörst
- [x] Schluss / Anhang
- [x] 通しの推敲(命令形・禁止語・章ごとの語数比)/ EPUB / KDP登録シート(`LISTING.md`)
- [ ] 表紙(三言語で同じデザイン、文字だけドイツ語に)
- [ ] タイトルの重複確認(Amazon.de)/ KDP登録
