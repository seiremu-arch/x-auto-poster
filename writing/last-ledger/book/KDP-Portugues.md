# Ficha KDP — *O último livro-caixa: Uma herança em três partes*（ポルトガル語・ブラジル版）

ポルトガル語版は、ほかの版とは別の KDP タイトル（別ASIN）として登録する。
以下はそのまま KDP の入力欄に貼れる。**残るのは表紙と価格の2つ。**

---

## 1. 入稿ファイル

| ファイル | 用途 |
| --- | --- |
| `O_ultimo_livro-caixa_1_Uma_heranca_em_tres_partes.epub` | **KDPにアップロードするのはこれ**（横書き・左開き） |
| `O_ultimo_livro-caixa_1_Uma_heranca_em_tres_partes.md` | 統合原稿（読み返し用） |

EPUB3・リフロー、`dc:language` は `pt-BR`、`page-progression-direction="ltr"`。
本文は `../manuscript-pt/*.md`、方針と対訳表は `../TRANSLATION-pt.md`。
本文を直したら、`../check_pt.py` で台詞のダッシュと “ ” の対応を確かめてから組む。

```bash
python3 writing/last-ledger/check_pt.py
python3 writing/last-ledger/build_epub.py --portuguese
```

---

## 2. Detalhes do livro

**Idioma**

```
Português
```

**Título / Subtítulo**

```
O último livro-caixa
Uma herança em três partes
```

**Série / Número**

```
O último livro-caixa / 1
```

**Autor**

```
Nome: Kazu A.
Sobrenome: Suzuki
```

**Descrição**（約250語。KDPの上限は4,000字）

```
Ele deixou trezentos milhões de ienes. Cada herdeiro só poderá ficar com um terço.

Por trinta anos, Shuji Kamiya analisou propostas de crédito num banco japonês, e há um
ano esconde da mulher que perdeu quase toda a indenização de aposentadoria num golpe
de investimento estrangeiro. Então chega pelo correio um velho livro-caixa. Quem o
envia é um homem que ele viu uma única vez, trinta anos atrás: Soichiro Tono, cuja
empresa o banco de Kamiya deixou afundar em 1996.

A carta que o acompanha diz: “Se morri caindo da escada, não foi um acidente”.

Foi postada na véspera do dia em que Soichiro caiu da escada da velha casa da
família, vazia.

O testamento divide a herança em terreno, empresa e dinheiro, e obriga três herdeiros
a escolher, cada um, uma parte num envelope lacrado. Se dois escolherem a mesma, ela
vai para uma fundação. Como nota pessoal, ele deixou uma única linha: “A quem apostou
tudo numa coisa só, não deixem nem um iene”.

Nomeado testamenteiro, Kamiya começa a contar. De um dia para o outro, o terreno cai
de cem para vinte milhões. Há dinheiro que sumiu no exterior. E na parede da escada
restam quatro furos de parafuso, onde antes havia um corrimão.

Um romance policial financeiro, sóbrio e preciso, sobre herança, golpe e um crime
que consiste em não fazer nada. Livro 1 da série “O último livro-caixa”.
```

**Palavras-chave**（7つまで）

```
romance policial japonês
thriller financeiro
mistério herança testamento
segredos de família japão
golpe de investimento romance
traduzido do japonês
literatura policial
```

**Categorias**（KDPで3つまで。表示名はストアで変わるので、ピッカーで最も近いものを選ぶ）

```
Loja Kindle › eBooks Kindle › Policial, suspense e mistério › Policial › Internacional
Loja Kindle › eBooks Kindle › Policial, suspense e mistério › Suspense › Financeiro
Loja Kindle › eBooks Kindle › Literatura e ficção › Literatura estrangeira › Japonesa
```

**Conteúdo adulto** Não
**Territórios** Todos

---

## 3. ★ AI開示（必須）

KDP は、本文・画像・**翻訳**にAIを使ったかを申告させる。このポルトガル語版は
**AIの支援で翻訳した**ので、*Traduções*（Translations）は **Sim／Yes** と答える。
誤って申告すると販売停止になることがある。

---

## 4. ★ 表紙（未着手）

- 1600 × 2560 px、JPEG または TIFF、RGB、72dpi以上、50MB未満
- 文字：**O ÚLTIMO LIVRO-CAIXA** ／ *Uma herança em três partes* ／ **Kazu A. Suzuki**
- ほかの版と同じ絵に文字だけ載せ替えると、シリーズとしてそろう

---

## 5. 価格

- 約36,800語。紙換算でおよそ160〜180ページ
- 主な市場は Amazon.com.br（ブラジル）。ポルトガル本国の読者は Amazon.es などから買う
- 価格はブラジル・レアル（BRL）で別に設定する。ほかの版の価格から自動換算にせず、
  ブラジルの電子書籍の相場に合わせて**手で決める**
- Amazon.com.br での70%ロイヤリティには、KDPセレクトへの登録が条件になっている
  （ブラジル・日本・メキシコ・インドのストアでの扱い）。登録の有無と価格帯は、
  KDPの価格欄とロイヤリティの説明で最新の条件を確かめてから決める
- KDPセレクトに入れると、その期間は電子書籍をAmazon以外で売れない。
  ほかの言語版をKDPセレクトに入れていなくても、この版だけ入れることはできる

---

## 6. 出版前チェックリスト

- [x] 著者名 `Kazu A. Suzuki`（`dc:creator`、扉、Créditos）
- [x] EPUB の XML 検証済み、`mimetype` 非圧縮で先頭
- [x] 台詞のダッシュと “ ” の対応（`check_pt.py`）
- [ ] 表紙画像（1600 × 2560 px）
- [ ] KDP プレビューアで確認：左開き、段落の字下げ、`※` の区切り、台詞のダッシュ
- [ ] 目次（Sumário）から全章に飛べるか
- [ ] 帳簿の最新の一行が *10 de fevereiro de 2026…* になっているか（和暦の中で唯一の西暦）
- [ ] AI開示（3.）
- [ ] KDPセレクトに入れるかどうか（5.）
- [ ] 内容紹介の末尾に第2巻の予告を入れるか
