# ブラジルポルトガル語版『A Repartição dos Sonhos』KDP登録情報

第一巻のブラジルポルトガル語版です。貼り付ける中身はポルトガル語、説明は
日本語で書いてあります。

主戦場は amazon.com.br です。ポルトガル語の読者はブラジルに約二億人、
ポルトガルに約千万人いて、七言語でいちばん話者が多い言語になります。
**正書法はブラジルで統一**してあります。

---

## 1. 本の詳細

| 項目 | 内容 |
|---|---|
| Título | A Repartição dos Sonhos |
| Subtítulo | Doze noites |
| Série | A Repartição dos Sonhos（Livro 1） |
| 巻番号 | 1 |
| Autor | Kazu A. Suzuki |
| 出版言語 | Português |
| ISBN | 不要（KDPが内部管理番号を自動付与） |

---

## 2. Descrição（そのまま貼り付け可）

Os sonhos não se apagam. Só se podem tornar mais leves.

Enquanto você dorme, o cérebro amolece uma lembrança, religa-a e a deixa fixar-se de novo. A edição de sonhos é o ofício que acompanha esses poucos segundos e altera, só um pouco, a mão que religa.

Não há como fazer outra coisa além de reduzir o peso de uma lembrança. Em uma noite, 0,05 no máximo. No ofício, chamam isso de meia-tinta.

O limite não existe por insuficiência da técnica. Afinando uma lembrança depressa demais, o vestígio da reescrita vai junto com ela. Enquanto o vestígio permanece, a pessoa pode dizer a si mesma: este é um sonho editado. O que o limite protege não é o sonho de quem dorme. É a margem que sobra depois, ao acordar, para duvidar da própria memória.

Doze contos ligados, num país onde essa técnica entrou até o último canto da vida comum.

- Uma menina de treze anos que pede que deixem o seu pesadelo em paz — Meia-tinta
- Uma mulher que espera quatro anos e sete meses e recusa o procedimento no dia da sua vez — A fila do esquecimento
- Uma viúva que recebe o pedido de desculpas que o marido nunca conseguiu dizer, sintetizado dos seus diários, e uma filha que chama aquilo de falsificação — O testamento
- Uma mãe a quem se lê todo mês uma história clara e consoladora, traduzida dos sonhos de um filho sem palavras — O tradutor
- Um técnico que eleva o remorso de um homicida de 0,07 a 0,81 ao longo de quinze noites — A pena
- Um trabalho onde o procedimento do luto é obrigatório em quarenta e oito horas, e um homem que não se conforma — O luto por procuração

Não há vilões. Há apenas pessoas que fazem o seu trabalho corretamente, conforme as normas, e um campo que as normas nunca previram.

Cada conto se sustenta sozinho. Quanto mais se avança, mais claro fica o que este país vem chamando de felicidade.

SUMÁRIO
I. Meia-tinta
II. A fila do esquecimento
III. O testamento
IV. O tradutor
V. O sonho em segunda pessoa
VI. Imposto sobre sonhos
VII. O luto por procuração
VIII. A pena
IX. O direito de não acordar
X. A herança
XI. Índice de Felicidade 98
XII. O sujeito silencioso

Cerca de 24.800 palavras.

---

## 3. Palavras-chave（7つ）

1. `ficção científica literária`
2. `distopia futuro próximo`
3. `contos interligados`
4. `memória e identidade`
5. `ficção científica contemplativa contos`
6. `distopia burocrática romance`
7. `ficção científica japonesa em português`

**入れてはいけないもの**：他の作家名や既存作品名。他の言語版と同じ注意です。

---

## 4. Categorias（最大3つ）

1. Literatura e Ficção → Ficção científica → Antologias e contos
2. Literatura e Ficção → Ficção literária
3. Literatura e Ficção → Ficção científica → Distopia

---

## 5. 価格とロイヤリティ

| 項目 | 推奨 |
|---|---|
| ロイヤリティ | 70%プラン |
| 価格 | R$ 9,90（ブラジル） |
| KDPセレクト | 登録する |

ブラジルで70%プランが使えるのは **R$ 5,99〜R$ 24,99** の範囲です（登録画面で
範囲が表示されるので、そこで確認してください）。R$ 9,90 は現地の電子書籍の
相場の中ほどです。

**税金。** ブラジルの書籍は**憲法上の免税**（imunidade tributária）の対象で、
電子書籍も2017年の最高裁（STF）判断で同じ扱いになりました。他の六言語と違い、
付加価値税で手取りが削られません。

**KDPセレクト。** 90日間の独占は**言語版ごと**に数えます。ポルトガル語版を
セレクトに入れても、他の六言語版の扱いには影響しません。

---

## 6. アップロードするファイル

| 用途 | ファイル |
|---|---|
| 原稿 | `book/dist/A Repartição dos Sonhos.epub` |
| 表紙 | `book/dist/cover_pt1.jpg`（1600×2560px、1.6:1） |

```bash
python3 book/tools/build_epub.py pt1
python3 book/tools/build_cover.py pt1
```

（検証: 日本語版第一巻の表紙と画素比較して、差分は題字と著者名の矩形
`(168, 303)-(1286, 1055)` の内側だけ。英・独・西・仏・伊・蘭の第一巻と
まったく同じ矩形で、帯の地模様が一致していることを確認済み。EPUBは
mimetype が無圧縮で先頭、CRC・XML整形式・`dc:language` が pt、
`page-progression-direction` が ltr、章12・spine14。本文の travessão は
1203個、ASCII引用符0個、約物前の空白0個）

---

## 7. 翻訳について

**日本語の原文から訳しています**（他の言語版からの重訳ではありません）。
原文51.718字 → 葡文24.752 words（比0.479）。仏語0.495・蘭語0.493に次ぎ、
伊語0.438より9%ほど嵩みます。

### 正書法はブラジル

`registro`・`fato`・`objeto`・`atual`。ポルトガル本国の `registo`・`facto`・
`objecto`・`actual` は使いません。検査を置いてあります。

### 会話は travessão（—）で組んであります

ブラジル文芸の標準です。西語版・仏語版と同じ組み方で、伊語版のカポラーリ、
蘭語版の二重引用符とは別の判断になります。

```
　— Não apague, por favor.
　— Não vou apagar — disse Kaji. — Não existe técnica para apagar.
```

書類からの一文も同じ `　— ` で始まるので、**記号だけでは会話と書類が
区別できません**。西語版・仏語版はこのために検査を置けていませんでした。

葡語版では**段落で突き合わせる検査**を置きました。原文の段落が `　「` で
始まるもの（丸ごと発話）だけを見て、対応する葡語の段落が `　— ` で始まる
ことを確かめます。書類の一文は原文で `　――` で始まるので検査の対象に
入りません。これで区別がつきます。

入れ子の引用符は、英・独・西・伊・蘭と同じく落としてあります。

### 約物の前に空白を入れません

`assim:` であって `assim :` ではありません。**仏語とは逆の規則**です。

### 数字

小数点は読点（`0,038`）、千の位は点（`114.206`）、百分率は `por cento`。
独・西・伊・蘭と同じ体系です。

### 西語の混入検査を別に置いています

西語はポルトガル語と近いので、一語残っても**読んでいて気づきにくい**。
独語↔蘭語と同じ関係です。ポルトガル語に存在しない綴りだけを並べました
（`y` / `muy` / `pero` / `entonces` / `ahora` / `cuando` / `dijo` /
`hacia` / `estaba` / `había` / `también` / `siempre` / `aquí` /
`después` / `sin` / `con` / `del` / `es` / `hay` / `así` / `qué`）。
葡語にもある `nunca`・`antes`・`porque` は入れていません。`as` は葡語の
冠詞なので `así` だけを見ます。

### この版で難しかった語

| 日本語 | Português | 理由 |
|---|---|---|
| 夢編集局 | A Repartição dos Sonhos | `Escritório` は中立だが、`repartição` はブラジルで官公庁そのものを指す語で、窓口と書式の気配が最初から付いてくる。原文の 局 がまさにそれ |
| 半色 | a meia-tinta | 印刷の網点の語。原文の色と半歩の両方が残る。仏 demi-teinte・西 media tinta・伊 mezzatinta と同じく語が用意されていた |
| 夢裁判 | A pena | pena は刑罰と苦痛の両方を負う。仏 peine・西 pena・伊 pena と同じ二重性 |
| 涙の代筆 | O luto por procuração | `por procuração` は法律の「委任による」。原文の事務的な語感をそのまま運ぶ |
| 校正官 | o Corretor | ブラジルでは `corretor` は不動産仲介を先に連想させるが、`corretor ortográfico`（文章を直す機械）の語でもあり、原文の意味はそちら。`revisor` は人間の校正者なので不可 |
| 混入率 | a taxa de contaminação | 第十二話の指標。第二巻XIIが四十一年後にこれを開く |
| 共有者 | o condômino | 共同所有者を指す法律語。同じ出来事を分け持つという意味を素直に負う |
| 間 | a folga | 第二巻IVの「余りじゃなくて、間だ」。機械の遊び（公差）と「余地」の両方を負う |

### 巻をまたぐ引用

第二巻第八話は、この巻の第二話・第四話・第十二話から文をそのまま引用します。
葡語の五件は、訳す**前**に `check_tr_quotes.py` の対応表へ登録しました。

---

## 8. 出版前チェックリスト

- [x] 全十二話の翻訳を終えた
- [x] `check_tr_structure.py` が0件で通ることを確認した
- [x] `check_tr_terms.py` が0件で通ることを確認した
- [x] `check_tr_quotes.py` で第一巻側の引用が通ることを確認した
- [x] `check_overlap.py` が0件で通ることを確認した（七言語）
- [x] 表紙の帯が日本語版第一巻と一致していることを画素比較で確認した
- [x] EPUBの構造を確認した（mimetype・CRC・XML・lang・方向・章数・travessão）
- [ ] Kindle Previewerで表示を三機種確認した（ã・õ・ç の出かたを特に）
- [ ] Descrição を貼り付けた
- [ ] Palavras-chave 7つを入れた
- [ ] Categorias を3つ選んだ
- [ ] 価格を設定し、70%プランの範囲内か確認した（R$ 5,99〜24,99）
- [ ] KDPセレクトの可否を決めた
