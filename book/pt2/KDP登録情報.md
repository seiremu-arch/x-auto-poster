# ブラジルポルトガル語版『O Nivelamento』KDP登録情報

第二巻のブラジルポルトガル語版です。貼り付ける中身はポルトガル語、説明は
日本語で書いてあります。

主戦場は amazon.com.br です。正書法はブラジルで統一してあります。

---

## 1. 本の詳細

| 項目 | 内容 |
|---|---|
| Título | O Nivelamento |
| Subtítulo | A Repartição dos Sonhos, Livro Dois |
| Série | A Repartição dos Sonhos（Livro 2） |
| 巻番号 | 2 |
| Autor | Kazu A. Suzuki |
| 出版言語 | Português |
| ISBN | 不要（KDPが内部管理番号を自動付与） |

シリーズ名はポルトガル語版第一巻と**一字一句同じ**（`A Repartição dos Sonhos`）に
してください。`ç` と `ã` の有無も違いとして数えられます。

---

## 2. Descrição（そのまま貼り付け可）

O Nivelamento. É o nome de um plano estatal que traz para a média, noite após noite, o peso das lembranças de um milhão de pessoas.

Enquanto você dorme, o cérebro amolece uma lembrança, religa-a e a deixa fixar-se de novo. A edição de sonhos intervém nesses poucos segundos e reduz o peso: em uma noite se pode deslocar 0,05 no máximo. No ofício, chamam isso de meia-tinta.

Se o Livro I, A Repartição dos Sonhos, tratava de um técnico e de um requerente sentados frente a frente, estes doze contos vêm depois: quando a técnica se tornou primeiro um setor da economia, depois um sistema, e por fim algo do tamanho de um país.

- Uma sociedade em que três horas de sono bastam, e uma empresa que nos quarenta minutos restantes vende os sentimentos dos outros — A cidade que não dorme
- Uma intervenção antes do nascimento que forma segurança, confiança e curiosidade num feto. Aquilo sobre o que ela agia não eram as crianças — Fundações
- A tristeza transferida a um autor já foi retirada dos parentes no instante da colheita — A injeção de empatia
- Taxa de processamento automático de 98,4 por cento, e o último artesão que carrega o 1,6 restante — O último artesão
- Um homem a quem, por sete noites e sem o seu consentimento, tornaram as coisas mais pesadas, e que recusa que as recoloquem no lugar — Lesão corporal
- Um incêndio com dezenove mortos de que ninguém se lembra e que não está escrito em lugar nenhum — O cadastro

Não há vilões. Há apenas pessoas que, nos seus setores, fazem o seu trabalho corretamente. A Distribuição muda algo pela taxa de operação; a Análise de Falhas, pelo tamanho do custo da correção; a Gestão Técnica, por falta de pessoal. Não há vestígio de que tenham conversado entre si.

O que se produziu quando os três raciocínios caíram no mesmo trimestre se esclarece no último conto, O relatório final.

Cada conto se sustenta sozinho. O Livro I não é necessário.

SUMÁRIO
I. A cidade que não dorme
II. Fundações
III. A injeção de empatia
IV. O último artesão
V. A máquina sonha?
VI. Lesão corporal
VII. O cadastro
VIII. O mar dos sonhos
IX. O sonho de amanhã
X. O último bug
XI. Resíduo
XII. O relatório final

Cerca de 23.800 palavras.

---

## 3. Palavras-chave（7つ）

1. `ficção científica literária`
2. `distopia futuro próximo`
3. `contos interligados`
4. `distopia burocrática romance`
5. `memória e identidade`
6. `ficção científica contemplativa contos`
7. `ficção científica japonesa em português`

第一巻と同じ七語です。順番だけ、この巻の中身（官僚機構の側に寄っている）に
合わせて四番目を上げました。他の六言語の第二巻と同じ入れ替えです。

---

## 4. Categorias（最大3つ）

1. Literatura e Ficção → Ficção científica → Antologias e contos
2. Literatura e Ficção → Ficção científica → Distopia
3. Literatura e Ficção → Ficção literária

第一巻は2番と3番が逆です。この巻はディストピアの比重が高いので入れ替えました。

---

## 5. 価格とロイヤリティ

| 項目 | 推奨 |
|---|---|
| ロイヤリティ | 70%プラン |
| 価格 | R$ 9,90（ブラジル） |
| KDPセレクト | 登録する |

ブラジルで70%プランが使えるのは **R$ 5,99〜R$ 24,99** の範囲です（登録画面で
確認してください）。第一巻と揃えてあります。

**税金。** ブラジルの書籍は憲法上の免税（imunidade tributária）の対象で、
電子書籍も2017年の最高裁（STF）判断で同じ扱いです。七言語でいちばん手取りが
多くなります。

**KDPセレクト。** 90日間の独占は**言語版ごと**に数えます。

---

## 6. アップロードするファイル

| 用途 | ファイル |
|---|---|
| 原稿 | `book/dist/O Nivelamento.epub` |
| 表紙 | `book/dist/cover_pt2.jpg`（1600×2560px、1.6:1） |

```bash
python3 book/tools/build_epub.py pt2
python3 book/tools/build_cover.py pt2
```

（検証: 日本語版第二巻の表紙と画素比較して、差分は題字と著者名の矩形
`(168, 307)-(1297, 947)` の内側だけ。英・独・西・仏・伊・蘭の第二巻と
まったく同じ矩形で、帯の地模様が一致していることを確認済み。EPUBは
mimetype が無圧縮で先頭、CRC・XML整形式・`dc:language` が pt、
`page-progression-direction` が ltr、章12・spine14。本文の travessão は
1037個、ASCII引用符0個、約物前の空白0個、ピリオドは千の位だけ）

---

## 7. 翻訳について

**日本語の原文から訳しています**（他の言語版からの重訳ではありません）。
原文48.719字 → 葡文23.750 words（比0.487）。仏語0.507・蘭語0.494に次ぎます。

会話は travessão（—）で組んでいます。書類の一文も同じ記号なので、段落で
突き合わせる検査を置いてあります。理由は第一巻の登録情報に書いたとおりです。
約物の前に空白は入れません（仏語と逆）。小数点は読点（0,038）、千の位は点
（1.027.400）。正書法はブラジル。

### この巻で新しく出た用語

| 日本語 | Português | 理由 |
|---|---|---|
| 均し計画 | o Plano de Nivelamento | 表題の `O Nivelamento` は本文の計画名と同語源。`nivelamento` は工学の語であると同時に、差を縮める政策の語でもある |
| 第二次同期 | a Segunda Sincronização | 第一巻XIIの `sincronização` を受ける |
| 共有者数 | o número de condôminos | XIで研究者が論文で名づける造語。`condômino` は共同所有者を指す法律語で、同じ出来事を分け持つという意味を素直に負う |
| 窪み | a cavidade | Xの「同じ形の窪み」。`depressão` は臨床のうつと衝突するので使わない |
| 保持記録 | os registros retidos | V・VIII・X・XI・XIIを貫く |
| 混入率 | a taxa de contaminação | XIIが第一巻XIIの読み手報告を四十一年後に開く。第一巻の訳語をそのまま使う |
| 分散 | a variância | 統計の用語。XIIの完了要件はこの一語で書かれている |
| 間 | a folga | IVの「余りじゃなくて、間だ」。機械の遊び（公差）と「余地」の両方を負うので、上限と実際に押す量のあいだという原文の意味がそのまま入る |
| 先行確定 | a fixação antecipada | IXの配分用語 |
| 余剰成分 | o componente excedente | V・Xに共通 |
| 最後のバグ | o último bug | 原文は 不具合（公式語）と バグ（現場の通称）を書き分けている。葡語も同じ対が使えるので、公式分類は falha leve conhecida、通称は bug |
| 混線 | — | 第一巻VIでは `mistura`。蘭語の overspraak に当たる一語は葡語にないので、現象を記述する形にした |

### 巻をまたぐ引用

第八話は、第一巻の第二話・第四話・第十二話と、この巻の第六話に出た文を、
保管庫に残った記録としてそのまま引用します。五件すべてが一字一句一致することを
`check_tr_quotes.py` で確認済みです（七言語を同時に見ます）。

### 葡語版で足した検査

- **travessão の段落検査**：原文が `　「` で始まる段落は、葡文も `　— ` で
  始まること。西語版・仏語版にはない検査で、段落で突き合わせることで
  会話と書類の一文を区別できるようにした
- **ポルトガル本国の綴り**：`registo` / `facto` / `objecto` / `actual` /
  `contacto` / `director` / `óptimo` / `eléctrico` / `exacto`
- **西語の機能語の混入**：葡語に存在しない綴りだけを並べた
- **綴り字記号の落ち**：`numero` / `indice` / `tecnico` / `condomino` /
  `genero` / `orgao` / `residuo` / `periodo` / `proprio` / `ultimo`。
  ただし `tecnicamente` は強勢が移るため記号が付かないのが正しい。
  最初に `tecnic\w*` で括ってこの副詞を鳴らしてしまったので、名詞・
  形容詞の形だけを見るように絞り直した

いずれも、誤った入力を食わせて実際に鳴ることを確かめてから入れています。

---

## 8. 出版前チェックリスト

- [x] 全十二話の翻訳を終えた
- [x] `check_tr_structure.py` が0件で通ることを確認した
- [x] `check_tr_terms.py` が0件で通ることを確認した
- [x] `check_tr_quotes.py` が0件で通ることを確認した（引用5件・定型句3件）
- [x] `check_overlap.py` が0件で通ることを確認した（七言語）
- [x] 表紙の帯が日本語版第二巻と一致していることを画素比較で確認した
- [x] EPUBの構造を確認した（mimetype・CRC・XML・lang・方向・章数・travessão）
- [ ] Kindle Previewerで表示を三機種確認した（ã・õ・ç の出かたを特に）
- [ ] Descrição を貼り付けた
- [ ] Palavras-chave 7つを入れた
- [ ] Categorias を3つ選んだ
- [ ] シリーズ名が第一巻と一字一句同じか確認した（ç・ã も）
- [ ] 価格を設定し、70%プランの範囲内か確認した（R$ 5,99〜24,99）
- [ ] KDPセレクトの可否を決めた
