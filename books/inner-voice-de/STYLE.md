# Stilregeln — Die leiseste Stimme

日本語版 `books/inner-voice/STYLE.md` と同じ立場を、ドイツ語で守るためのもの。
**読者が自分で確かめられることだけを書く。**

## Anrede und Haltung

- **`du`.** Nicht `Sie`(理由は Vault `7586251f89`)
- Ich-Form für alles Eigene. „Ich mache das so", nicht „So macht man das"
- Dem Leser nie einen Zustand zuschreiben. Nicht „du bist erschöpft",
  sondern „wenn du erschöpft bist"
- Nicht belehren, sondern **daneben stehen.** „Probier es" statt „du musst"
- Wenn ich von Erfahrung schreibe, gehören die Male dazu, die nicht funktioniert haben

### Imperativ: nur in den Schritten und in Bedingungssätzen

`du` macht es leicht, in Anweisungen zu kippen. Erlaubt ist der Imperativ an zwei Stellen:

1. in den **numerierten Schritten** einer Übung
2. im **Bedingungssatz** — „Setz die Namen zurück, und es wird ein normales Meeting."
   Das ist keine Anweisung, sondern die Erklärung einer Folge

Verboten ist die **nackte Anweisung** im laufenden Text und in Überschriften.
Nicht „Benutz den Körper nur, um …", sondern „Der Körper ist nur dafür da, …".
Nicht „## Teile die Frage in drei", sondern „## Die Frage, in drei geteilt".

```bash
python books/inner-voice-de/check_style.py
```

Das Skript kennt die Verbliste, die Ausnahme für Bedingungssätze und die verbotenen Wörter.
Es endet mit Exit-Code 1, wenn es etwas findet.

## Wörter, die nicht vorkommen

Alles, was sich nicht überprüfen lässt. Nicht im Text, nicht auf dem Cover,
nicht in der Beschreibung.

> das Universum / Schwingung(en) / manifestieren / Gesetz der Anziehung /
> höheres Selbst / dein wahres Selbst / Seelenplan / Energie (auch nicht als Bild) /
> Erwachen / Unterbewusstsein (ohne Definition) / Ego (ohne Definition)

Ebenso keine absoluten Behauptungen über Wirkung: **immer / nie (über Ergebnisse) /
jeder / garantiert / wird dein Leben verändern / erwiesen**.

Der `grep` darauf braucht ein menschliches Auge: „nicht immer", „immer noch" und
„jeder Zeile" sind in Ordnung. Verboten ist nur die Behauptung über eine Wirkung.

Eine Ausnahme, wie in der japanischen und der englischen Ausgabe: der Satz im Vorwort,
der sagt, dass in diesem Buch kein Universum und keine Schwingungen vorkommen.
Ein Wort einmal zu nennen, um es abzulehnen, ist nicht dasselbe wie sich darauf zu stützen.

```bash
grep -niE "Universum|Schwingung|manifestier|Gesetz der Anziehung|höheres Selbst|wahres Selbst|Seelenplan|Erwachen|garantiert|verändert dein Leben|Intuition|Bauchgefühl" \
  books/inner-voice-de/manuscript/*.md
```

## Begriffe (über alle Kapitel gleich halten)

| Konzept | Begriff | 日本語版 |
| --- | --- | --- |
| die vier Stimmen | die ängstliche Stimme / die Sollte-Stimme / die geborgte Stimme / die leiseste Stimme | 不安の声 / べき論の声 / 借りものの声 / 内なる声 |
| Kriterium 1 | die Geschwindigkeit (die Reihenfolge, in der etwas kommt) | 速さ |
| Kriterium 2 | der Körper — es löst sich oder es zieht sich zusammen | 体 — ゆるむ / 締まる |
| was wir herstellen | Raum (nicht Stille) | 余白 |
| was wir tun | zählen, unterscheiden, zurückkommen | 数える / 聞き分ける / 戻る |

Die leiseste Stimme heißt nie „Intuition", „Bauchgefühl" oder „inneres Wissen".
Diese Wörter behaupten etwas, das dieses Buch nicht behauptet.

## Sätze

- Ein Gedanke pro Satz. Zwei Gedanken werden zwei Sätze
- Drei bis vier Sätze pro Absatz. Der Punkt steht im ersten
- Szenen beginnen mit einem konkreten Moment, nicht mit einem Abstraktum.
  Nicht „Angst ist", sondern „um elf, nachdem das Licht aus ist"
- Höchstens zwei Bilder pro Kapitel
- Nur **Handgriffe** dürfen flach behauptet werden. „Nimm ein Blatt Papier" ist in Ordnung
- Schachtelsätze vermeiden. Wenn ein Satz zwei Nebensätze tief geht, teile ihn

## Sicherheit

- Körperliche Symptome werden nie durch diese Übungen gedeutet
- Nichts schreiben, was sich als „du brauchst keine Ärztin" lesen lässt
- Klar sagen: wenn Schlaf, Appetit oder Stimmung nicht zurückkommen, hören die Übungen
  auf und es beginnt jemand mit Ausbildung. In Kapitel 3 **und** im Anhang
