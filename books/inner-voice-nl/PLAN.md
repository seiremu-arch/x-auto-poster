# 企画書 — オランダ語版『De zachtste stem』

日本語版 `books/inner-voice/` の**書き直し**であって、翻訳ではない
(方針と反証条件は Vault `899744d0ff`)。芯・章構成・実践の番号は揃え、場面と例を決め直す。

## 書誌

| 項目 | 内容 |
| --- | --- |
| Titel | De zachtste stem |
| Ondertitel | Zeven oefeningen om je eigen stem te onderscheiden van het lawaai in je hoofd |
| Auteur | Kazu A. Suzuki(他の六言語と同一表記) |
| 言語 | オランダ語(Amazon.nl。ベルギーのオランダ語圏の読者もここで買う) |
| 分量 | 15,000 words 前後(日本語版 33,075字 ÷ 実測 2.21字/word。→ Vault `4fc805514a` の追記) |
| 想定価格 | 4,99 € |

## 芯にする一文

> Je zachtste stem wordt nooit luider. Er zit niets anders op dan zelf stiller te worden.

`zachtste`(いちばん小さい)と `luider` / `stiller` が音量の語でそろう。
`zelf zachter worden` は「自分が優しくなる」とも読めるので使わない。
七言語のどれかを直すときは七つとも直す(`--check` が一致を見る)。

## 決め直すもの

- **人称は `je`。** このジャンルの標準。`u` は役所の文面の距離になる。ここは論点にならない
- **地域。** Amazon.nl はオランダとベルギー(フランデレン)の両方の読者が使う。
  スペイン語版の中立化(`cb294d65c0`)と同じ考え方で、片方でしか使わない語を避ける
  (`gsm` / `frigo` / `pinnen` など。`check_style.py` が拾う)。新しい判断ではなく、既存の判断の適用
- **性の一致。** オランダ語は形容詞・分詞が人の性で変わらない(`ik ben moe`、`ik was verrast`)。
  読者側 `0045c354b1`・著者側 `dba7c10f3f` の問題は、文法の上ではほぼ消える。
  残るのは人を指す名詞(`vriend/vriendin`、`-er/-ster`)だけで、著者自身をそういう名詞で呼ばない

## 検証すること

claim `dd52672aca` の予測(第5章がプラス、第7章がマイナス)を、イタリア語版に続けてもう一度試す。
全章を書いたら結果をあのノートに追記する。

## 日本語版から差し替えるもの

| 章 | 日本語版の場面 | オランダ語版の場面 |
| --- | --- | --- |
| 序章 | 眠れない夜に二十行書く | 同じ |
| 1 | 金曜の飲みの誘い「その仕事、辞めたら?」 | vrijdagavond eten met een vriendin: “Neem dan gewoon ontslag.” |
| 2 | 誘いに即答した三日後 | “Ik ben erbij!” in drie seconden in een groepsapp |
| 3 | 内見した部屋の玄関で肩が上がる | de derde bezichtiging(住宅難の国なのでそのまま効く) |
| 4 | レンジの二分・信号待ち | de magnetron, het stoplicht, de lift |
| 5 | 会議で部長に数字を指摘される | een vergadering met zeven mensen, een verkeerd cijfer |
| 6 | 三年ぶりの分岐点は金曜の夜、誘いを断った | de vrijdagmiddagborrel afgezegd |
| 7 | 三週間目に何も来なくなった | 同じ。電車が止まるのは «een storing» |

## 出す前に確かめること

- **タイトルの重複。** Amazon.nl で “De zachtste stem” を検索する
- `check_style.py` が0件(命令形・禁止語・地域語・引用符・書きかけの言い直し)

## 現在地

- [x] 企画・構成
- [x] Proloog
- [x] Hoofdstuk 1 Hoeveel stemmen er praten
- [x] Hoofdstuk 2 Onderscheiden aan de snelheid
- [x] Hoofdstuk 3 Onderscheiden in je lichaam
- [x] Hoofdstuk 4 Ruimte maken
- [x] Hoofdstuk 5 Schrijven om te luisteren
- [x] Hoofdstuk 6 Klein beslissen
- [x] Hoofdstuk 7 De dagen dat je niets hoort
- [x] Slot / Bijlage(全10章 15,230 words、目安の102%)
- [x] 検査 `check_style.py` 0件 / EPUB / 表紙 / 登録シート(`LISTING.md`)
- [x] 章をまたいだ通しの推敲(2026-10-03。Vault `576bfe3f5d`)
- [ ] KDP登録(手作業。DRM と KDP Select は要判断)
