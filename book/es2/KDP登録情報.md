# スペイン語版『La Nivelación』KDP登録情報

第二巻のスペイン語版です。貼り付ける中身はスペイン語、説明は日本語で書いてあります。

主戦場は amazon.es ですが、amazon.com.mx と amazon.com（米国のヒスパニック市場）
にも同時に出ます。第一巻と同じ三市場です。

---

## 1. 本の詳細

| 項目 | 内容 |
|---|---|
| Título | La Nivelación |
| Subtítulo | La Oficina de Sueños, Libro Dos |
| Serie | La Oficina de Sueños（Libro 2） |
| 巻番号 | 2 |
| Autor | Kazu A. Suzuki |
| 出版言語 | Español |
| ISBN | 不要 |

シリーズ名はスペイン語版第一巻と**一字一句同じ**（`La Oficina de Sueños`）に
してください。違うとシリーズページが別々に作られます。

---

## 2. Descripción（そのまま貼り付け可）

La Nivelación. Así se llama un proyecto estatal que acerca a la media, noche tras noche, el peso de los recuerdos de un millón de personas.

Mientras usted duerme, el cerebro ablanda un recuerdo, vuelve a unirlo y lo deja asentarse de nuevo. La edición de sueños interviene en esos pocos segundos para bajar el peso, y en una noche solo pueden moverse 0,05 como máximo. En el oficio lo llaman la media tinta.

Si el Libro I, La Oficina de Sueños, trataba de un técnico y un solicitante sentados frente a frente, estos doce relatos ocurren después: cuando la técnica se ha hecho primero una industria, después un sistema y por fin algo del tamaño de un país.

- Una sociedad en que bastan tres horas de sueño, y una empresa que en los cuarenta minutos restantes vende los sentimientos de otros — «La ciudad que no duerme»
- Una intervención prenatal que forma amparo, confianza y curiosidad en un feto. Aquello sobre lo que actuaba no eran los niños — «Cimientos»
- La pena que se transfiere a un agresor ya les ha sido quitada a los deudos en el instante de la extracción — «La inyección de empatía»
- Grado de automatización, 98,4 por ciento, y el último artesano que carga con el 1,6 restante — «El último artesano»
- Un hombre a quien durante siete noches se le hizo más pesado sin su consentimiento y que se niega a que lo devuelvan — «Lesiones»
- Un incendio con diecinueve muertos que nadie recuerda y que no está escrito en ninguna parte — «El registro»

No hay villanos. Solo hay personas que, en sus departamentos, hacen su trabajo correctamente. Distribución cambia algo por la tasa de utilización; Análisis de Incidencias, por el coste de corregir; Gestión Técnica, por falta de plantilla. No hay indicio alguno de que hablaran entre sí.

Qué ocurrió cuando los tres razonamientos cayeron en el mismo trimestre se aclara en el último relato, «El informe de cierre».

Cada relato se sostiene solo. No hace falta el Libro I.

ÍNDICE
I. La ciudad que no duerme
II. Cimientos
III. La inyección de empatía
IV. El último artesano
V. ¿Sueña la máquina?
VI. Lesiones
VII. El registro
VIII. El mar de los sueños
IX. El sueño de mañana
X. El último fallo
XI. Residuo
XII. El informe de cierre

Unas 22.700 palabras.

---

## 3. Palabras clave（7つ）

1. `ciencia ficción literaria`
2. `distopía futuro cercano`
3. `relatos enlazados`
4. `distopía burocrática novela`
5. `memoria e identidad`
6. `ciencia ficción contemplativa cuentos`
7. `ciencia ficción japonesa en español`

第一巻と同じ七語です。順番だけ、この巻の中身（官僚機構の側に寄っている）に
合わせて四番目を上げました。

**入れてはいけないもの**：他の作家名や既存作品名。他の言語版と同じ注意です。

---

## 4. Categorías（最大3つ）

1. Ficción → Ciencia ficción → Antologías y relatos
2. Ficción → Ciencia ficción → Distopías
3. Ficción → Literatura y ficción general

第一巻は2番と3番が逆です。この巻はディストピアの比重が高いので入れ替えました。

---

## 5. 価格とロイヤリティ

| 項目 | 推奨 |
|---|---|
| ロイヤリティ | 70%プラン |
| 価格 | 3,99 €（スペイン） |
| KDPセレクト | 登録する |

70%プランが使えるのは **2,99 €〜9,99 €** の範囲です。第一巻・ドイツ語版と
揃えてあります。

**付加価値税。** スペインの電子書籍は軽減税率（4%）です。ロイヤリティは税抜額に
対してかかります。メキシコ（amazon.com.mx）は税率も通貨も別なので、登録画面で
自動換算させたうえで税抜額を確認してください。

**KDPセレクト。** 90日間の独占になりますが、これは**言語版ごと**に数えます。
スペイン語版をセレクトに入れても、日本語版・英語版・ドイツ語版の扱いには
影響しません。

---

## 6. アップロードするファイル

| 用途 | ファイル |
|---|---|
| 原稿 | `book/dist/La Nivelación.epub` |
| 表紙 | `book/dist/cover_es2.jpg`（1600×2560px、1.6:1） |

```bash
python3 book/tools/build_epub.py es2
python3 book/tools/build_cover.py es2
```

（検証: 日本語版第二巻の表紙と、字のない下半分を画素比較して差分ゼロを確認済み。
英語版・ドイツ語版の第二巻とも一致します。EPUBは mimetype が無圧縮で先頭、
CRC・XML整形式・`dc:language` が es、`page-progression-direction` が ltr、
章12・spine14 を確認済み）

---

## 7. 翻訳について

**日本語の原文から訳しています**（英語版・ドイツ語版からの重訳ではありません）。
原文48,719字 → 西文22,734 words（比0.467）。

会話はレイヤ（—）で組んでいます。理由と書式は第一巻の登録情報に書いたとおりです。
小数点は読点（0,038）、千の位は点（1.027.400）。

### この巻で新しく出た用語

| 日本語 | Español | 理由 |
|---|---|---|
| 均し計画 | el Plan de Nivelación | 表題の `La Nivelación` は本文の計画名と同語源にしてある |
| 第二次同期 | la Segunda Sincronización | 第一巻XIIの `sincronización` を受ける |
| 共有者数 | el número de copartícipes | XIで研究者が論文で名づける造語。copartícipe は実在の語で、同じ出来事を分け持つ者という意味を素直に負う |
| 窪み | la hondonada | Xの「同じ形の窪み」。臨床語に読まれる `depresión` を避けた |
| 保持記録 | los registros conservados | VIII・X・XI・XIIを貫く。書く欄がなかったものの集まり |
| 下方編集 | la edición a la baja | |
| 引きずり | el arrastre | 第一巻Iから継承 |
| 先行確定 | la fijación previa | IXの配分用語 |

### 巻をまたぐ引用

第八話は、第一巻の第二話・第四話・第十二話と、この巻の第六話に出た文を、
保管庫に残った記録としてそのまま引用します。五件すべてが一字一句一致することを
`check_tr_quotes.py` で確認済みです（英・独・西の三言語を同時に見ます）。

---

## 8. 出版前チェックリスト

- [x] 全十二話の翻訳を終えた
- [x] `check_tr_structure.py` が0件で通ることを確認した（字下げ・三字下げの塊も）
- [x] `check_tr_terms.py` が0件で通ることを確認した
- [x] `check_tr_quotes.py` が0件で通ることを確認した
- [x] `check_overlap.py` が0件で通ることを確認した（英・独・西の三言語）
- [x] 表紙の帯が日本語版第二巻と一致していることを画素比較で確認した
- [x] EPUBの構造を確認した（mimetype・CRC・XML・lang・方向・章数）
- [ ] Kindle Previewerで表示を三機種確認した（ñ・アクセント記号・レイヤを特に）
- [ ] Descripción を貼り付けた
- [ ] Palabras clave 7つを入れた
- [ ] Categorías を3つ選んだ
- [ ] シリーズ名が第一巻と一字一句同じか確認した
- [ ] 価格を設定し、税抜額を確認した（西4%・墨は別税率）
- [ ] KDPセレクトの可否を決めた
