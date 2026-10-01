# 企画書 — イタリア語版『La voce più bassa』

日本語版 `books/inner-voice/` の**書き直し**であって、翻訳ではない
(方針と反証条件は Vault `899744d0ff`)。芯・章構成・実践の番号は揃え、場面と例を決め直す。

## 書誌

| 項目 | 内容 |
| --- | --- |
| Titolo | La voce più bassa |
| Sottotitolo | Sette esercizi per distinguere la tua voce dal rumore nella tua testa |
| Autore | Kazu A. Suzuki(他の五言語と同一表記) |
| 言語 | イタリア語(Amazon.it) |
| 分量 | 14,400 words 前後(日本語版 33,075字 ÷ 実測 2.29字/word。→ Vault `4fc805514a` の追記) |
| 想定価格 | 4,99 € |

## 芯にする一文

> La tua voce più bassa non parlerà mai più forte. Non resta che abbassare il tuo volume.

スペイン語版と同じく、`bassa`(低い声)と `abbassare`(下げる)が響き合う。
六言語のどれかを直すときは六つとも直す(`--check` が一致を見る)。

## 決め直すもの

**イタリア語では、新しく決め直すものがない。** これはこの書き直しで初めて。

- 人称は `tu`。このジャンルの標準で、フランス語の `tu` のようなコーチング調の連想もない
- 地域差はスペイン語ほど大きくない(イタリアとスイスのイタリア語圏)
- 性の一致は既存の判断に従う。読者側は `0045c354b1`、著者側は `dba7c10f3f`
  (新しく書く原稿なので、著者の一人称も中立にする)

ただしイタリア語は、性の一致を避けるのがスペイン語より難しい。`essere` を取る近過去
(`sono tornato/a`、`sono andato/a`)と再帰動詞(`mi sono lamentato/a`)で性が出る。
`avere` を取る動詞・半過去・言い換えで避け、`check_style.py` で最初の章から検査する。

## 検証すること

claim `dd52672aca` は「次の言語でも、章ごとの分量のずれは第5章がプラス、第7章がマイナスに出る」と
予測している。**イタリア語版がその最初のテストになる。** 全章を書いたら結果をあのノートに追記する。

## 日本語版から差し替えるもの

| 章 | 日本語版の場面 | イタリア語版の場面 |
| --- | --- | --- |
| 序章 | 眠れない夜に二十行書く | 同じ |
| 1 | 金曜の飲みの誘い「その仕事、辞めたら?」 | una cena del venerdì con un'amica: «E licenziati, no?» |
| 2 | 誘いに即答した三日後 | «Ci sono!» scritto in tre secondi in un gruppo |
| 3 | 内見した部屋の玄関で肩が上がる | la terza visita a un appartamento(そのまま) |
| 4 | レンジの二分・信号待ち | il microonde, l'ascensore, la fila alla cassa |
| 5 | 会議で部長に数字を指摘される | una riunione di sette persone, una cifra sbagliata |
| 6 | 三年ぶりの分岐点は金曜の夜、誘いを断った | 同じ形 |
| 7 | 三週間目に何も来なくなった | 同じ |

## 出す前に確かめること

- **タイトルの重複。** Amazon.it で «La voce più bassa» を検索する
- `check_style.py` が0件(命令形・禁止語・性の一致)

## 現在地

- [x] 企画・構成
- [x] Prologo
- [x] Capitolo 1 Quante voci stanno parlando
- [x] Capitolo 2 Distinguere dalla velocità
- [x] Capitolo 3 Distinguere nel corpo
- [x] Capitolo 4 Fare spazio
- [x] Capitolo 5 Scrivere per ascoltare
- [ ] Capitoli 6〜7
- [ ] Chiusura / Appendice
- [ ] 通しの推敲 / EPUB / 表紙 / KDP登録(`LISTING.md`)
