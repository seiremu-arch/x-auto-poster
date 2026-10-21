# Edizione italiana, Libro II — Stato

Traduzione del Libro II, `book/vol2/stories/` → `book/it2/stories/`.

La terminologia è fissata in [`GLOSSARY.md`](../it/GLOSSARY.md), condiviso col
Libro I. Compilare con `python3 book/tools/build_epub.py it2`.

**Si traduce dall'originale giapponese.**

---

## Stato

| # | Giapponese | Italiano | Origine | Parole | Stato |
|---|---|---|---|---|---|
| I | 眠らない都市 | La città che non dorme | 4.336 | 2.012 | **fatto** |
| II | 胎夢 | Fondazioni | 4.240 | — | in attesa |
| III | 共感注射 | L'iniezione di empatia | 4.432 | — | in attesa |
| IV | 最後の夢職人 | L'ultimo artigiano | 4.226 | — | in attesa |
| V | ＡＩは夢を見るか | La macchina sogna? | 3.963 | — | in attesa |
| VI | 夢の犯罪 | Lesioni | 3.933 | — | in attesa |
| VII | 消えた現実 | Il registro | 3.982 | — | in attesa |
| VIII | 夢の海 | Il mare dei sogni | 3.889 | — | in attesa |
| IX | 明日の夢 | Il sogno di domani | 3.879 | — | in attesa |
| X | 最後のバグ | L'ultimo bug | 3.843 | — | in attesa |
| XI | 残差 | Residuo | 3.906 | — | in attesa |
| XII | 完了報告 | La relazione di chiusura | 4.090 | — | in attesa |

Giapponese in totale, 48.719 caratteri. Le cifre di questa tabella le scrive
`python3 book/tools/sync_tr_counts.py it2`, non la mano.

---

## Che cosa è nuovo in questo libro

Il Piano di Livellamento passa dal fondo al centro. Il Libro I lo menziona; il
Libro II tratta della sua chiusura.

L'ottavo racconto cita alla lettera dal Libro I — dai racconti secondo, quarto
e dodicesimo — e dal sesto di questo libro. Se la traduzione si scosta anche di
una parola, il legame fra i libri si rompe. `check_tr_quotes.py` lo verifica
meccanicamente, per lingua, e le cinque frasi italiane vi sono registrate
**prima** di essere scritte: la tabella è la specifica, non il verbale.

---

## Il racconto presentato al premio

Il Libro II è quello che corre più vicino a『境界線、未編集』, perché entrambi
trattano della Seconda Sincronizzazione. Si condivide il mondo — la mezzatinta,
il Piano di Livellamento, la Seconda Sincronizzazione —, non una frase, né un
personaggio, né un'immagine. La passerella pedonale verde del racconto
presentato non compare in nessuno dei due libri e non deve comparire.

---

## Controlli

```bash
python3 book/tools/sync_tr_counts.py it2
python3 book/tools/check_tr_structure.py
python3 book/tools/check_tr_terms.py
python3 book/tools/check_tr_quotes.py
python3 book/tools/check_overlap.py
python3 book/tools/build_epub.py it2
python3 book/tools/build_cover.py it2
```
