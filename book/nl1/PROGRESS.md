# Nederlandse editie, Deel I — Stand van zaken

Vertaling van Deel I, `book/vol1/stories/` → `book/nl1/stories/`.

De terminologie is vastgelegd in [`GLOSSARY.md`](../nl/GLOSSARY.md), gedeeld met
Deel II. Compileren met `python3 book/tools/build_epub.py nl1`.

**Er wordt uit het Japanse origineel vertaald.**

---

## Stand van zaken

| # | Japans | Nederlands | Origineel | Woorden | Status |
|---|---|---|---|---|---|
| I | 半色 | Halftint | 4.997 | 2.585 | **klaar** |
| II | 忘却の順番待ち | De wachtlijst van de vergetelheid | 4.540 | 2.186 | **klaar** |
| III | 夢の遺言 | Het testament | 4.552 | 2.256 | **klaar** |
| IV | 夢の翻訳者 | De vertaler | 3.915 | 1.780 | **klaar** |
| V | 二人称の夢 | De droom in de tweede persoon | 3.454 | 1.699 | **klaar** |
| VI | 夢税 | Droombelasting | 3.391 | 1.660 | **klaar** |
| VII | 涙の代筆 | Rouw bij volmacht | 4.476 | 2.174 | **klaar** |
| VIII | 夢裁判 | De boete | 4.577 | 2.189 | **klaar** |
| IX | 目覚めない権利 | Het recht niet te ontwaken | 4.503 | 2.201 | **klaar** |
| X | 夢の相続 | De erfopvolging | 4.587 | 2.269 | **klaar** |
| XI | 幸福指数九八 | Geluksindex 98 | 4.218 | 2.164 | **klaar** |
| XII | 沈黙の被験者 | De zwijgende proefpersoon | 4.508 | 2.324 | **klaar** |

Japans in totaal, 51.718 tekens. De cijfers in deze tabel worden geschreven
door `python3 book/tools/sync_tr_counts.py nl1`, niet met de hand.

---

## Wat deze editie eigen is

**De dialoog staat tussen dubbele aanhalingstekens.** De Nederlandse literaire
fictie gebruikt meestal enkele. Die zijn hier niet gekozen omdat het sluitteken
dan samenvalt met de apostrof, en openen en sluiten niet meer te tellen zijn.
De reden staat voluit in de verklarende lijst.

**Het Duits ligt dichtbij.** Een achtergebleven Duits functiewoord valt in
Nederlandse tekst niet op bij het lezen, anders dan een Frans of Spaans woord.
Daarom staat er een aparte controle op `ist`, `und`, `nicht`, `auch`, `sich`,
`wurde`, `zwischen` en een paar andere die het Nederlands niet heeft.

**Samenstellingen aan elkaar.** De verzonnen termen van deze reeks zijn bijna
alle samenstellingen (`droomredactie`, `geluksindex`, `referentieapparaat`), en
ze los schrijven is de fout die hier het makkelijkst te maken is. Ook daar staat
een controle op.

---

## Controles

```bash
python3 book/tools/sync_tr_counts.py nl1
python3 book/tools/check_tr_structure.py
python3 book/tools/check_tr_terms.py
python3 book/tools/check_tr_quotes.py
python3 book/tools/check_overlap.py
python3 book/tools/build_epub.py nl1
python3 book/tools/build_cover.py nl1
```
