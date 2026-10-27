# Edição brasileira, Livro II — Estado

Tradução do Livro II, `book/vol2/stories/` → `book/pt2/stories/`.

A terminologia está fixada em [`GLOSSARY.md`](../pt/GLOSSARY.md), comum aos
dois livros. Compilar com `python3 book/tools/build_epub.py pt2`.

**Traduz-se do original japonês.**

---

## Estado

| # | Japonês | Português | Original | Palavras | Estado |
|---|---|---|---|---|---|
| I | 眠らない都市 | A cidade que não dorme | 4.336 | 2.152 | **pronto** |
| II | 胎夢 | Fundações | 4.240 | 2.028 | **pronto** |
| III | 共感注射 | A injeção de empatia | 4.432 | 2.091 | **pronto** |
| IV | 最後の夢職人 | O último artesão | 4.226 | 2.099 | **pronto** |
| V | ＡＩは夢を見るか | A máquina sonha? | 3.963 | 1.931 | **pronto** |
| VI | 夢の犯罪 | Lesão corporal | 3.933 | 1.905 | **pronto** |
| VII | 消えた現実 | O cadastro | — | — | aguardando |
| VIII | 夢の海 | O mar dos sonhos | — | — | aguardando |
| IX | 明日の夢 | O sonho de amanhã | — | — | aguardando |
| X | 最後のバグ | O último bug | — | — | aguardando |
| XI | 残差 | Resíduo | — | — | aguardando |
| XII | 完了報告 | O relatório final | — | — | aguardando |

Japonês no total, 48.719 caracteres. Os números desta tabela são
escritos por `python3 book/tools/sync_tr_counts.py pt2`, não à mão.

---

## O que é novo neste livro

O Plano de Nivelamento passa do fundo para o centro. O Livro I o menciona; o
Livro II trata do seu encerramento.

Que 均し possa se chamar *Nivelamento* em português é a sorte desta
edição: não é só palavra de engenharia, é também
palavra de política pública, de quem reduz diferenças.

O oitavo conto cita ao pé da letra do Livro I — do segundo, do quarto e do
décimo segundo contos — e do sexto deste livro. Se a tradução se
afasta de uma palavra, o laço entre os livros se rompe.
`check_tr_quotes.py` verifica isso por máquina, língua por língua,
e as cinco frases portuguesas estão registradas lá **antes** de serem
escritas: a tabela é a especificação, não a ata.

---

## O conto inscrito no prêmio

O Livro II é o que passa mais perto de『境界線、未編集』, porque os dois
tratam da Segunda Sincronização. O que se divide é o mundo — a
meia-tinta, o Plano de Nivelamento, a Segunda Sincronização —, nenhuma
frase, nenhum personagem, nenhuma imagem. A passarela de pedestres verde do
conto inscrito não aparece em nenhum dos dois livros e não deve
aparecer.

---

## Verificações

```bash
python3 book/tools/sync_tr_counts.py pt2
python3 book/tools/check_tr_structure.py
python3 book/tools/check_tr_terms.py
python3 book/tools/check_tr_quotes.py
python3 book/tools/check_overlap.py
python3 book/tools/build_epub.py pt2
python3 book/tools/build_cover.py pt2
```
