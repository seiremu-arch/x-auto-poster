# Deutsche Ausgabe, Band II — Stand

Übersetzung von Band II, `book/vol2/stories/` → `book/de2/stories/`.

Die Terminologie ist in [`GLOSSARY.md`](../de/GLOSSARY.md) festgelegt, gemeinsam
mit Band I. Bauen mit `python3 book/tools/build_epub.py de2`.

**Übersetzt wird aus dem japanischen Original, nicht aus der englischen
Ausgabe.**

---

## Stand

| # | Japanisch | Deutsch | Quelle | Wörter | Stand |
|---|---|---|---|---|---|
| I | 眠らない都市 | Die schlaflose Stadt | 4.336 | 1.889 | **fertig** |
| II | 胎夢 | Fundamente | 4.240 | — | offen |
| III | 共感注射 | Die Empathiespritze | 4.432 | — | offen |
| IV | 最後の夢職人 | Der letzte Handwerker | 4.226 | — | offen |
| V | ＡＩは夢を見るか | Träumt die Maschine? | 3.963 | — | offen |
| VI | 夢の犯罪 | Körperverletzung | 3.933 | — | offen |
| VII | 消えた現実 | Das Register | 3.982 | — | offen |
| VIII | 夢の海 | Das Meer der Träume | 3.889 | — | offen |
| IX | 明日の夢 | Der Traum von morgen | 3.879 | — | offen |
| X | 最後のバグ | Der letzte Fehler | 3.843 | — | offen |
| XI | 残差 | Residuum | 3.906 | — | offen |
| XII | 完了報告 | Der Abschlussbericht | 4.090 | — | offen |

Japanisch insgesamt 48.719 Zeichen. Die Zahlen schreibt
`python3 book/tools/sync_tr_counts.py de2`, nicht die Hand.

---

## Was in diesem Band neu ist

Der Angleichungsplan rückt vom Hintergrund in den Mittelpunkt. Band I erwähnt
ihn; Band II handelt von seinem Abschluss.

Die achte Erzählung zitiert wörtlich aus Band I — aus der zweiten, vierten und
zwölften Erzählung — und aus der sechsten dieses Bandes. Weicht die Übersetzung
auch nur in einem Wort ab, reißt die Verbindung über die Bände hinweg.
`check_tr_quotes.py` prüft das maschinell, für jede Sprache getrennt.

---

## Der Wettbewerbsbeitrag

Band II läuft dem Beitrag『境界線、未編集』am nächsten, weil beide die Zweite
Synchronisation behandeln. Geteilt wird die Welt — der Halbton, der
Angleichungsplan, die Zweite Synchronisation —, nicht ein Satz, keine Figur,
kein Bild. Die grün gestrichene Fußgängerbrücke des Beitrags kommt in keinem
Band vor und darf es nicht.

---

## Prüfungen

```bash
python3 book/tools/sync_tr_counts.py de2
python3 book/tools/fix_de_quotes.py
python3 book/tools/check_tr_structure.py
python3 book/tools/check_tr_terms.py
python3 book/tools/check_tr_quotes.py
python3 book/tools/check_overlap.py
python3 book/tools/build_epub.py de2
python3 book/tools/build_cover.py de2
```
