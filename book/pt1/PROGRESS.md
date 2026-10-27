# Edição brasileira, Livro I — Estado

Tradução do Livro I, `book/vol1/stories/` → `book/pt1/stories/`.

A terminologia está fixada em [`GLOSSARY.md`](../pt/GLOSSARY.md), comum aos
dois livros. Compilar com `python3 book/tools/build_epub.py pt1`.

**Traduz-se do original japonês.**

---

## Estado

| # | Japonês | Português | Original | Palavras | Estado |
|---|---|---|---|---|---|
| I | 半色 | Meia-tinta | 4.997 | 2.517 | **pronto** |
| II | 忘却の順番待ち | A fila do esquecimento | 4.540 | 2.162 | **pronto** |
| III | 夢の遺言 | O testamento | 4.552 | 2.164 | **pronto** |
| IV | 夢の翻訳者 | O tradutor | 3.915 | 1.803 | **pronto** |
| V | 二人称の夢 | O sonho em segunda pessoa | 3.454 | 1.656 | **pronto** |
| VI | 夢税 | Imposto sobre sonhos | 3.391 | 1.615 | **pronto** |
| VII | 涙の代筆 | O luto por procuração | 4.476 | 2.091 | **pronto** |
| VIII | 夢裁判 | A pena | 4.577 | 2.136 | **pronto** |
| IX | 目覚めない権利 | O direito de não acordar | 4.503 | 2.141 | **pronto** |
| X | 夢の相続 | A herança | 4.587 | 2.199 | **pronto** |
| XI | 幸福指数九八 | Índice de Felicidade 98 | 4.218 | 2.043 | **pronto** |
| XII | 沈黙の被験者 | O sujeito silencioso | 4.508 | 2.225 | **pronto** |

Japonês no total, 51.718 caracteres. Os números desta tabela são
escritos por `python3 book/tools/sync_tr_counts.py pt1`, não à mão.

---

## O que é próprio desta edição

**A norma é a brasileira.** `registro`, `fato`, `objeto`, `atual`. As
grafias de Portugal estão proibidas e há verificação para
isso.

**O espanhol fica perto.** Uma palavra funcional do espanhol que fique para
trás não salta aos olhos em texto português, ao contrário de
uma palavra alemã ou inglesa. Há uma verificação separada
para `y`, `muy`, `pero`, `entonces`, `ahora`, `cuando`, `dijo` e outras que o
português não tem.

**O diálogo usa travessão, e as linhas de documento também.** Em
espanhol e em francês isso torna as duas coisas indistinguíveis para
uma verificação. Aqui elas se distinguem porque a comparação
é feita parágrafo por parágrafo contra o original: onde o japonês
abre com `　「`, o português tem de abrir com `　— `.

---

## Verificações

```bash
python3 book/tools/sync_tr_counts.py pt1
python3 book/tools/check_tr_structure.py
python3 book/tools/check_tr_terms.py
python3 book/tools/check_tr_quotes.py
python3 book/tools/check_overlap.py
python3 book/tools/build_epub.py pt1
python3 book/tools/build_cover.py pt1
```
