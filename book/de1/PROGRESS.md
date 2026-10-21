# Deutsche Ausgabe, Band I — Stand

Übersetzung von Band I, `book/vol1/stories/` → `book/de1/stories/`.

Die Terminologie ist in [`GLOSSARY.md`](../de/GLOSSARY.md) festgelegt. Ein
Begriff wird dort entschieden, bevor er benutzt wird. Bauen mit
`python3 book/tools/build_epub.py de1`.

**Übersetzt wird aus dem japanischen Original, nicht aus der englischen
Ausgabe.** Eine Weiterübersetzung würde die im Englischen getroffenen
Entscheidungen festschreiben und jede Abweichung verdoppeln.

---

## Stand

| # | Japanisch | Deutsch | Quelle | Wörter | Stand |
|---|---|---|---|---|---|
| I | 半色 | Halbton | 4.997 | 2.340 | **fertig** |
| II | 忘却の順番待ち | Die Warteliste für das Vergessen | 4.540 | 2.025 | **fertig** |
| III | 夢の遺言 | Das Vermächtnis | 4.552 | 2.010 | **fertig** |
| IV | 夢の翻訳者 | Der Übersetzer | 3.915 | 1.589 | **fertig** |
| V | 二人称の夢 | Der Traum in der zweiten Person | 3.454 | 1.465 | **fertig** |
| VI | 夢税 | Traumsteuer | 3.391 | 1.417 | **fertig** |
| VII | 涙の代筆 | Trauer in Vertretung | 4.476 | 1.908 | **fertig** |
| VIII | 夢裁判 | Das Strafmaß | 4.577 | 1.954 | **fertig** |
| IX | 目覚めない権利 | Das Recht, nicht zu erwachen | 4.503 | 1.956 | **fertig** |
| X | 夢の相続 | Der Nachlass | 4.587 | 1.984 | **fertig** |
| XI | 幸福指数九八 | Glücksindex 98 | 4.218 | 1.898 | **fertig** |
| XII | 沈黙の被験者 | Der schweigende Proband | 4.508 | 2.023 | **fertig** |

Japanisch insgesamt 51.718 Zeichen. Die Zahlen in dieser Tabelle schreibt
`python3 book/tools/sync_tr_counts.py de1`, nicht die Hand.

Deutsch fällt gegenüber dem Englischen kürzer aus, weil Komposita mehrere
englische Wörter zu einem zusammenziehen. Ein niedrigeres Verhältnis als die
0,463 der englischen Ausgabe ist daher kein Zeichen für Auslassungen. Ob etwas
fehlt, sagt `check_tr_structure.py`, nicht die Wortzahl.

---

## In Erzählung I festgelegt

Erzählung I ist der Maßstab für den Stil. Die späteren folgen ihr, statt neu zu
entscheiden.

**Abschnittsnummern.** Römische Ziffern, einzeln auf einer Zeile. Der Titel
trägt „I." mit Punkt, die Abschnittsköpfe nicht.

**Anführungszeichen.** „ … “ Deutsche Anführungszeichen. Das Japanische 「」
trägt oft keine Redeeinleitung; das Deutsche braucht etwas mehr, aber nur so
viel, wie der Leser sonst nicht folgen kann.

**Dezimalkomma.** 0,05 und 0,91, nicht 0.05. Das ist keine Kleinigkeit: mit
Punkt liest ein deutscher Leser eine Tausendertrennung.

**Siezen.** Kaji und Saya siezen einander, auch wenn Saya dreizehn ist. Das
Japanische ist durchweg in höflicher Form, und das Verhältnis zwischen Amt und
Antragstellerin ist genau das, worum es geht.

**Die Pause des Korrektors.** „Eine Pause, die einfach dort liegt, wo der Satz
bricht." Sparsam eingesetzt — die japanische Fassung hat sie von acht auf drei
Vorkommen gekürzt, und das Deutsche behält dieselben drei.

---

## Prüfungen

```bash
python3 book/tools/sync_tr_counts.py de1      # Wortzahlen abgleichen
python3 book/tools/check_tr_structure.py      # Absätze gegen das Original
python3 book/tools/check_tr_terms.py          # Terminologie, Rechtschreibung, Anführungszeichen
python3 book/tools/check_overlap.py           # Abstand zum Wettbewerbsbeitrag
python3 book/tools/build_epub.py de1
python3 book/tools/build_cover.py de1
```
