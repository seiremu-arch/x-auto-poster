# Nederlandse editie, Deel II — Stand van zaken

Vertaling van Deel II, `book/vol2/stories/` → `book/nl2/stories/`.

De terminologie is vastgelegd in [`GLOSSARY.md`](../nl/GLOSSARY.md), gedeeld met
Deel II. Compileren met `python3 book/tools/build_epub.py nl2`.

**Er wordt uit het Japanse origineel vertaald.**

---

## Stand van zaken

| # | Japans | Nederlands | Origineel | Woorden | Status |
|---|---|---|---|---|---|
| I | 眠らない都市 | De stad die niet slaapt | 4.336 | 2.144 | **klaar** |
| II | 胎夢 | Fundamenten | 4.240 | 2.080 | **klaar** |
| III | 共感注射 | De empathie-injectie | 4.432 | 2.077 | **klaar** |
| IV | 最後の夢職人 | De laatste ambachtsman | 4.226 | 2.135 | **klaar** |
| V | ＡＩは夢を見るか | Droomt de machine? | 3.963 | 1.890 | **klaar** |
| VI | 夢の犯罪 | Mishandeling | 3.933 | 1.931 | **klaar** |
| VII | 消えた現実 | Het register | 3.982 | 2.032 | **klaar** |
| VIII | 夢の海 | De zee van dromen | 3.889 | 1.858 | **klaar** |
| IX | 明日の夢 | De droom van morgen | — | — | in afwachting |
| X | 最後のバグ | De laatste bug | — | — | in afwachting |
| XI | 残差 | Residu | — | — | in afwachting |
| XII | 完了報告 | Het eindrapport | — | — | in afwachting |

Japans in totaal, 48.719 tekens. De cijfers in deze tabel worden geschreven
door `python3 book/tools/sync_tr_counts.py nl2`, niet met de hand.

---

## Wat in dit deel nieuw is

Het Nivelleringsplan schuift van de achtergrond naar het midden. Deel I noemt
het; Deel II gaat over de sluiting ervan.

Dat 均し in het Nederlands *Nivellering* kan heten is het geluk van deze
editie. Het is hier geen technisch woord maar een politiek woord: het staat voor
overheidsbeleid dat verschillen kleiner maakt. Het Duits moest *Angleichung*
kiezen en het Engels *Levelling*; in het Nederlands zit de staat al in het woord.

Het achtste verhaal citeert letterlijk uit Deel I — uit het tweede, vierde en
twaalfde verhaal — en uit het zesde van dit deel. Wijkt de vertaling ook maar
één woord af, dan breekt de band tussen de delen. `check_tr_quotes.py` gaat dat
machinaal na, per taal, en de vijf Nederlandse zinnen staan er **voordat** ze
geschreven werden: de tabel is de specificatie, niet het verslag.

---

## Het verhaal dat voor de prijs is ingezonden

Deel II loopt het dichtst langs『境界線、未編集』, omdat beide over de Tweede
Synchronisatie gaan. Wat gedeeld wordt is de wereld — de halftint, het
Nivelleringsplan, de Tweede Synchronisatie —, geen zin, geen personage, geen
beeld. De groene voetgangersbrug van het ingezonden verhaal komt in geen van de
twee delen voor en mag er niet in komen.

---

## Controles

```bash
python3 book/tools/sync_tr_counts.py nl2
python3 book/tools/check_tr_structure.py
python3 book/tools/check_tr_terms.py
python3 book/tools/check_tr_quotes.py
python3 book/tools/check_overlap.py
python3 book/tools/build_epub.py nl2
python3 book/tools/build_cover.py nl2
```
