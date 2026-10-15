# Edición española, Libro I — Estado

Traducción del Libro I, `book/vol1/stories/` → `book/es1/stories/`.

La terminología está fijada en [`GLOSSARY.md`](../es/GLOSSARY.md). Un término se
decide allí antes de usarse. Compilar con `python3 book/tools/build_epub.py es1`.

**Se traduce del original japonés, no de la edición inglesa ni de la alemana.**

---

## Estado

| # | Japonés | Español | Origen | Palabras | Estado |
|---|---|---|---|---|---|
| I | 半色 | Media tinta | 4.997 | 2.394 | **hecho** |
| II | 忘却の順番待ち | La lista de espera del olvido | 4.540 | 1.983 | **hecho** |
| III | 夢の遺言 | El legado | 4.555 | 2.031 | **hecho** |
| IV | 夢の翻訳者 | El traductor | 3.915 | 1.670 | **hecho** |
| V | 二人称の夢 | El sueño en segunda persona | 3.454 | 1.553 | **hecho** |
| VI | 夢税 | Impuesto sobre el sueño | 3.391 | 1.546 | **hecho** |
| VII | 涙の代筆 | Duelo por delegación | 4.476 | 1.961 | **hecho** |
| VIII | 夢裁判 | La condena | 4.577 | 2.006 | **hecho** |
| IX | 目覚めない権利 | El derecho a no despertar | 4.503 | 2.044 | **hecho** |
| X | 夢の相続 | La herencia | 4.587 | 2.044 | **hecho** |
| XI | 幸福指数九八 | Índice de Felicidad 98 | 4.218 | 1.982 | **hecho** |
| XII | 沈黙の被験者 | El sujeto silencioso | 4.508 | 2.215 | **hecho** |

Japonés en total, 51.721 caracteres. Las cifras de esta tabla las escribe
`python3 book/tools/sync_tr_counts.py es1`, no la mano.

---

## Decidido en el relato I

**Diálogo con raya.** Es la norma española. Entrecomillar delataría una
traducción del inglés.

**Narración y diálogo en el mismo párrafo.** Cuando el japonés pone en un solo
párrafo una frase de narración seguida de 「habla」, el español mantiene **un
solo párrafo** y abre la raya en la misma línea:

> El jefe rio un poco y luego se puso serio. —Lo que hacemos aquí es, en el
> fondo, ventilar.

Partirlo en dos párrafos sería igual de correcto en español, pero haría que la
traducción dejara de corresponder párrafo a párrafo con el original, y con ello
`check_tr_structure.py` dejaría de servir para detectar omisiones. Esa
comprobación vale más que la variante tipográfica.

**Coma decimal.** 0,05 y 0,91, no 0.05. Con punto, un lector español lee un
separador de millares.

**Usted.** Kaji y Saya se tratan de usted, aunque Saya tenga trece años. El
japonés va en forma cortés de principio a fin, y la relación entre la Oficina y
quien acude es justamente el asunto del libro.

**La pausa del Corrector.** «Una pausa que simplemente se posa donde la frase
se quiebra.» Con mesura: la versión japonesa la redujo de ocho apariciones a
tres, y el español conserva esas mismas tres.

---

## Comprobaciones

```bash
python3 book/tools/sync_tr_counts.py es1
python3 book/tools/check_tr_structure.py
python3 book/tools/check_tr_terms.py
python3 book/tools/check_overlap.py
python3 book/tools/build_epub.py es1
python3 book/tools/build_cover.py es1
```
