# Edición española, Libro II — Estado

Traducción del Libro II, `book/vol2/stories/` → `book/es2/stories/`.

La terminología está fijada en [`GLOSSARY.md`](../es/GLOSSARY.md), compartido
con el Libro I. Compilar con `python3 book/tools/build_epub.py es2`.

**Se traduce del original japonés.**

---

## Estado

| # | Japonés | Español | Origen | Palabras | Estado |
|---|---|---|---|---|---|
| I | 眠らない都市 | La ciudad que no duerme | 4.336 | 2.019 | **hecho** |
| II | 胎夢 | Cimientos | 4.240 | 1.836 | **hecho** |
| III | 共感注射 | La inyección de empatía | 4.432 | 1.863 | **hecho** |
| IV | 最後の夢職人 | El último artesano | 4.226 | 1.913 | **hecho** |
| V | ＡＩは夢を見るか | ¿Sueña la máquina? | 3.963 | 1.776 | **hecho** |
| VI | 夢の犯罪 | Lesiones | 3.933 | 1.749 | **hecho** |
| VII | 消えた現実 | El registro | 3.982 | 1.820 | **hecho** |
| VIII | 夢の海 | El mar de los sueños | 3.889 | 1.867 | **hecho** |
| IX | 明日の夢 | El sueño de mañana | 3.879 | 1.946 | **hecho** |
| X | 最後のバグ | El último fallo | 3.843 | 1.921 | **hecho** |
| XI | 残差 | Residuo | 3.906 | — | pendiente |
| XII | 完了報告 | El informe de cierre | 4.090 | — | pendiente |

Japonés en total, 48.719 caracteres. Las cifras las escribe
`python3 book/tools/sync_tr_counts.py es2`.

---

## Lo nuevo de este libro

El Plan de Nivelación pasa del fondo al centro. El Libro I lo menciona; el
Libro II trata de su cierre.

El octavo relato cita literalmente del Libro I —de los relatos segundo, cuarto
y duodécimo— y del sexto de este libro. Si la traducción se aparta aunque sea
en una palabra, se rompe la conexión entre libros. `check_tr_quotes.py` lo
comprueba de forma mecánica, por lengua.

---

## El relato presentado al premio

El Libro II es el que corre más cerca de『境界線、未編集』, porque ambos tratan
de la Segunda Sincronización. Se comparte el mundo —la media tinta, el Plan de
Nivelación, la Segunda Sincronización—, no una frase, ni un personaje, ni una
imagen. La pasarela peatonal verde del relato presentado no aparece en ninguno
de los dos libros y no debe aparecer.

---

## Comprobaciones

```bash
python3 book/tools/sync_tr_counts.py es2
python3 book/tools/check_tr_structure.py
python3 book/tools/check_tr_terms.py
python3 book/tools/check_tr_quotes.py
python3 book/tools/check_overlap.py
python3 book/tools/build_epub.py es2
python3 book/tools/build_cover.py es2
```
