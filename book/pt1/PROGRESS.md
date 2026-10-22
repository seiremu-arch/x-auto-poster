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
| III | 夢の遺言 | O testamento | — | — | aguardando |
| IV | 夢の翻訳者 | O tradutor | — | — | aguardando |
| V | 二人称の夢 | O sonho em segunda pessoa | — | — | aguardando |
| VI | 夢税 | Imposto sobre sonhos | — | — | aguardando |
| VII | 涙の代筆 | O luto por procuração | — | — | aguardando |
| VIII | 夢裁判 | A pena | — | — | aguardando |
| IX | 目覚めない権利 | O direito de não acordar | — | — | aguardando |
| X | 夢の相続 | A herança | — | — | aguardando |
| XI | 幸福指数九八 | Índice de Felicidade 98 | — | — | aguardando |
| XII | 沈黙の被験者 | O sujeito silencioso | — | — | aguardando |

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
