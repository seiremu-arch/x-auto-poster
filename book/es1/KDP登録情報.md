# スペイン語版『La Oficina de Sueños』KDP登録情報

第一巻のスペイン語版です。貼り付ける中身はスペイン語、説明は日本語で書いてあります。

主戦場は amazon.es ですが、amazon.com.mx と amazon.com（米国のヒスパニック市場）
にも同時に出ます。この三つで英語版に次ぐ読者数になります。

---

## 1. 本の詳細

| 項目 | 内容 |
|---|---|
| Título | La Oficina de Sueños |
| Subtítulo | Doce noches |
| Serie | La Oficina de Sueños（Libro 1） |
| 巻番号 | 1 |
| Autor | Kazu A. Suzuki |
| 出版言語 | Español |
| ISBN | 不要 |

---

## 2. Descripción（そのまま貼り付け可）

Los sueños no pueden borrarse. Solo pueden aligerarse.

Mientras usted duerme, el cerebro ablanda un recuerdo, vuelve a unirlo y lo deja asentarse de nuevo. La edición de sueños es el oficio de asistir a esos pocos segundos y alterar, muy poco, la mano que vuelve a unir.

No puede hacerse más que bajar el peso de un recuerdo. En una noche solo pueden moverse 0,05 como máximo. En el oficio lo llaman la media tinta.

El límite no existe por una limitación de la técnica. Si se adelgaza un recuerdo demasiado deprisa, el rastro de la reescritura se va con él. Mientras el rastro permanece, una persona puede decirse: esto es un sueño editado. Lo que el límite protege no es el sueño de quien duerme. Es el margen que queda después, al despertar, para dudar de la propia memoria.

Doce relatos enlazados, situados en un país donde esa técnica ha llegado hasta el último rincón de la vida corriente.

- Una muchacha de trece años que pide que dejen en paz su pesadilla — «Media tinta»
- Una mujer que espera cuatro años y siete meses y se retira el día que le toca — «La lista de espera del olvido»
- Una viuda a quien entregan la disculpa que su marido nunca consiguió decir, sintetizada a partir de sus diarios, y una hija que la llama falsificación — «El legado»
- Una madre a la que cada mes le leen una historia clara y consoladora, traducida de los sueños de un hijo sin lenguaje — «El traductor»
- Un técnico que eleva el remordimiento de un agresor de 0,07 a 0,81 a lo largo de quince noches — «La condena»
- Un centro de trabajo donde la tramitación del duelo es obligatoria en cuarenta y ocho horas, y un hombre que no la acepta — «Duelo por delegación»

No hay villanos. Solo hay personas que hacen su trabajo correctamente, conforme a la norma, y un campo que la norma nunca previó.

Cada relato se sostiene solo. Cuanto más se avanza, más claro queda qué ha venido llamando felicidad este país.

ÍNDICE
I. Media tinta
II. La lista de espera del olvido
III. El legado
IV. El traductor
V. El sueño en segunda persona
VI. Impuesto sobre el sueño
VII. Duelo por delegación
VIII. La condena
IX. El derecho a no despertar
X. La herencia
XI. Índice de Felicidad 98
XII. El sujeto silencioso

Unas 23.000 palabras.

---

## 3. Palabras clave（7つ）

1. `ciencia ficción literaria`
2. `distopía futuro cercano`
3. `relatos enlazados`
4. `memoria e identidad`
5. `ciencia ficción contemplativa cuentos`
6. `distopía burocrática novela`
7. `ciencia ficción japonesa en español`

**入れてはいけないもの**：他の作家名や既存作品名。他の言語版と同じ注意です。

---

## 4. Categorías（最大3つ）

1. Ficción → Ciencia ficción → Antologías y relatos
2. Ficción → Literatura y ficción general
3. Ficción → Ciencia ficción → Distopías

---

## 5. 価格とロイヤリティ

| 項目 | 推奨 |
|---|---|
| ロイヤリティ | 70%プラン |
| 価格 | 3,99 €（スペイン） |
| KDPセレクト | 登録する |

70%プランが使えるのは **2,99 €〜9,99 €** の範囲です。ドイツ語版と揃えてあります。

**付加価値税。** スペインの電子書籍は軽減税率（4%）です。ドイツ（7%）より低い
ので、同じ 3,99 € でも手取りはスペインのほうが少し多くなります。メキシコ
（amazon.com.mx）は税率も通貨も別なので、登録画面で自動換算させたうえで
税抜額を確認してください。

---

## 6. アップロードするファイル

| 用途 | ファイル |
|---|---|
| 原稿 | `book/dist/La Oficina de Sueños.epub` |
| 表紙 | `book/dist/cover_es1.jpg`（1600×2560px、1.6:1） |

```bash
python3 book/tools/build_epub.py es1
python3 book/tools/build_cover.py es1
```

（検証: 日本語版第一巻の表紙と、字のない下半分を画素比較して差分ゼロを確認済み。
ñ も正しく出ています）

---

## 7. 翻訳について

**日本語の原文から訳しています**（英語版・ドイツ語版からの重訳ではありません）。
原文51,718字 → 西文23,429 words（比0.453）。

### 会話はレイヤ（—）で組んであります

これがスペイン語版でいちばん大きな判断です。スペイン語の文芸書は会話を
引用符ではなくレイヤで組みます。引用符で組むと英語からの翻訳書に見え、
文芸書の体裁になりません。

```
—No lo borre, por favor.
—No voy a borrarlo —dijo Kaji—. No existe una técnica para borrar.
```

なお、原文が「地の文＋「会話」」を一段落に収めている箇所は、スペイン語でも
一段落に保っています。二段落に割るのもスペイン語としては正しいのですが、
原文と段落が一対一で対応しなくなり、欠落検出の検査が使えなくなるためです。

### 主な用語

| 日本語 | Español | 理由 |
|---|---|---|
| 夢編集局 | La Oficina de Sueños | 「Oficina de Edición de Sueños」は題として長い。本文では初出のみ正式名、以降は la Oficina |
| 半色 | la media tinta | 「medio color」は西語に無い。印刷の網点の語で、色と半歩の両方を保つ |
| 校正官 | el Corrector | 原文の編集／校正という出版の比喩を残す |
| 素片 | el fragmento | |
| 情動荷重 | la carga afectiva | |
| 残差 | el residuo | 西語の統計用語 |
| 夢裁判 | La condena | 「El juicio del sueño」は平板でカフカを連想させる |

小数点は読点（0,05）、千の位は点（114.206）。スペイン語圏の慣行どおりです。
語彙は中立にしてあり、voseo や地域色の強い言い回しは避けました。amazon.es と
amazon.com.mx のどちらでも同じように読めます。

---

## 8. 出版前チェックリスト

- [x] 全十二話の翻訳を終えた
- [x] `check_tr_structure.py` が0件で通ることを確認した
- [x] `check_tr_terms.py` が0件で通ることを確認した
- [x] `check_overlap.py` が0件で通ることを確認した
- [x] 表紙の帯が日本語版第一巻と一致していることを画素比較で確認した
- [ ] Kindle Previewerで表示を三機種確認した（ñ・アクセント記号・レイヤを特に）
- [ ] Descripción を貼り付けた
- [ ] Palabras clave 7つを入れた
- [ ] Categorías を3つ選んだ
- [ ] 価格を設定し、税抜額を確認した（西4%・墨は別税率）
- [ ] KDPセレクトの可否を決めた
