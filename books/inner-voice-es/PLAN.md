# 企画書 — スペイン語版『La voz más baja』

日本語版 `books/inner-voice/` の**書き直し**であって、翻訳ではない
(方針と反証条件は Vault `899744d0ff`)。芯・章構成・実践の番号は揃え、
場面と例、そして**地域**を決め直す。

## 書誌

| 項目 | 内容 |
| --- | --- |
| Título | La voz más baja |
| Subtítulo | Siete ejercicios para distinguir tu propia voz del ruido en tu cabeza |
| Autor | Kazu A. Suzuki(他の四言語と同一表記) |
| 言語 | スペイン語(中立。Amazon.es / .com.mx / .com の三つに同じ本で届く) |
| 分量 | 14,500 words 前後(日本語版 33,075字 ÷ 実測 2.28字/word。→ Vault `899744d0ff` の追記) |
| 想定価格 | 4,99 €(Amazon.es)/ 米国・メキシコは自動換算を見て丸める |

## 芯にする一文

> Tu voz más baja nunca hablará más fuerte. Solo queda bajar tu propio volumen.

`baja`(低い声)と `bajar`(下げる)が響き合うのは、スペイン語で得た分。
五言語のどれかを直すときは五つとも直す(`--check` が一致を見る)。

## 決め直すもの:地域

**中立スペイン語で書く**(→ Vault `cb294d65c0`)。人称は `tú`。
地域で割れる語は `STYLE.md` の対応表に従い、`check_style.py` で検査する。

## 決め直すもの:性の一致

**著者にも読者にも、文法上の性を決めない**(→ Vault `c36e89b074`)。
`me sorprendió`(`me quedé sorprendido/a` ではなく)、`a solas`(`solo/sola` ではなく)のように、
一致が出ない言い方を選ぶ。フランス語版で黙って男性形に倒れたので、ここでは最初から検査する。

## 日本語版から動かさないもの

- 四つの声 — la voz ansiosa / la voz del «debería» / la voz prestada / la voz más baja
- 二つの基準 — **la velocidad**(el orden de llegada)と **el cuerpo**(se afloja / se tensa)
- 七つの実践の中身と番号。所要時間も変えない
- 章の順番と、各章が担う主張
- 約束しないこと(効果の断定をしない / 医療の代替にしない / 検証できない語を使わない)

## 日本語版から差し替えるもの

| 章 | 日本語版の場面 | スペイン語版の場面 |
| --- | --- | --- |
| 序章 | 眠れない夜に二十行書く | 同じ |
| 1 | 金曜の飲みの誘い「その仕事、辞めたら?」 | cena del viernes con una amiga: «Pues deja ese trabajo y ya.» |
| 2 | 誘いに即答した三日後 | «¡Voy!» escrito en tres segundos en un grupo |
| 3 | 内見した部屋の玄関で肩が上がる | la tercera visita a un apartamento(そのまま) |
| 4 | レンジの二分・信号待ち | el microondas, el ascensor, la fila de la caja |
| 5 | 会議で部長に数字を指摘される | una reunión de siete personas, una cifra equivocada |
| 6 | 三年ぶりの分岐点は金曜の夜、誘いを断った | 同じ形 |
| 7 | 三週間目に何も来なくなった | 同じ |

## 出す前に確かめること

- **タイトルの重複。** Amazon.es / .com.mx / .com で «La voz más baja» を検索する
- `check_style.py` が0件(命令形・禁止語・地域語・性の一致・¿¡の対応)
- 免責の文が、医療行為の否定と読まれない書き方になっているか

## 現在地

- [x] 企画・構成 / 地域と性の判断
- [x] Prólogo
- [x] Capítulo 1 ¿Cuántas voces están hablando?
- [x] Capítulo 2 Distinguir por la velocidad
- [x] Capítulo 3 Distinguir en el cuerpo
- [x] Capítulo 4 Hacer espacio
- [x] Capítulo 5 Escribir para escuchar
- [x] Capítulo 6 Decidir en pequeño
- [x] Capítulo 7 Los días en que no oyes nada
- [x] Cierre / Apéndice
- [x] 通しの推敲(五つの検査・章ごとの語数比)/ EPUB / KDP登録シート(`LISTING.md`)
- [x] 表紙(五言語で同じデザイン、文字だけスペイン語に)(`python scripts/build_cover.py inner-voice-es`)
- [ ] タイトルの重複確認(Amazon.es / .com.mx / .com)/ KDP登録
