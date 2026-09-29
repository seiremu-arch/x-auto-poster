# KDP-Angaben — *Das letzte Kassenbuch: Ein Erbe in drei Teilen* (deutsche Ausgabe)

ドイツ語版は、日本語版・英語版とは別の KDP タイトル（別ASIN）として登録する。
以下はそのまま KDP の入力欄に貼れる。**残るのは表紙と価格の2つ。**

---

## 1. 入稿ファイル

| ファイル | 用途 |
| --- | --- |
| `Das_letzte_Kassenbuch_1_Ein_Erbe_in_drei_Teilen.epub` | **KDPにアップロードするのはこれ**（横書き・左開き） |
| `Das_letzte_Kassenbuch_1_Ein_Erbe_in_drei_Teilen.md` | 統合原稿（読み返し用） |

EPUB3・リフロー、`dc:language` は `de`、`page-progression-direction="ltr"`。
本文は `../manuscript-de/*.md`、方針と対訳表は `../TRANSLATION-de.md`。

```bash
python3 writing/last-ledger/build_epub.py --german
```

---

## 2. Buchdetails

**Sprache**

```
Deutsch
```

**Buchtitel / Untertitel**

```
Das letzte Kassenbuch
Ein Erbe in drei Teilen
```

**Reihe / Band**

```
Das letzte Kassenbuch / 1
```

**Autor**

```
Vorname: Kazu A.
Nachname: Suzuki
```

**Beschreibung**（約220語。KDPの上限は4,000字）

```
Er hinterließ dreihundert Millionen Yen. Jeder Erbe darf nur ein Drittel davon nehmen.

Dreißig Jahre lang hat Shuji Kamiya in einer japanischen Bank Kredite geprüft – und
ein Jahr lang vor seiner Frau verheimlicht, dass er den größten Teil seiner Abfindung
an einen ausländischen Anlagebetrüger verloren hat. Dann kommt mit der Post ein altes
Kassenbuch. Absender ist ein Mann, dem er vor dreißig Jahren ein einziges Mal begegnet
ist: Soichiro Tono, dessen Firma Kamiyas Bank 1996 fallen ließ.

Im beiliegenden Brief steht: „Wenn ich die Treppe hinuntergestürzt und gestorben bin,
war es kein Unfall.“

Abgeschickt wurde er einen Tag, bevor Soichiro im leeren Stammhaus der Familie die
Treppe hinunterstürzte.

Sein Testament teilt das Erbe in Land, Unternehmen und Geld und lässt drei Erben je
einen Teil in einem versiegelten Umschlag wählen. Wählen zwei dasselbe, geht es an
eine Stiftung. Als persönlichen Zusatz hinterließ er eine einzige Zeile: „Wer alles
auf eine Karte gesetzt hat, dem hinterlasst keinen einzigen Yen.“

Als Testamentsvollstrecker beginnt Kamiya zu zählen. Über Nacht fällt der Wert des
Landes von hundert auf zwanzig Millionen. Geld ist ins Ausland verschwunden. Und in
der Wand neben der Treppe sind vier Schraubenlöcher, wo einmal ein Geländer war.

Ein leiser, genauer Finanzkrimi über Erbe, Betrug und ein Verbrechen, das darin
besteht, nichts zu tun. Band 1 der Reihe „Das letzte Kassenbuch“.
```

**Schlüsselwörter**（7つまで）

```
japanischer krimi
finanzkrimi
erbschaft testament krimi
familiengeheimnis japan
anlagebetrug roman
aus dem japanischen übersetzt
literarischer kriminalroman
```

**Kategorien**（KDPで3つまで。表示名はストアの言語で変わるので、ピッカーで最も近いものを選ぶ）

```
Kindle-Shop › eBooks › Krimis & Thriller › Krimis › Internationale Krimis
Kindle-Shop › eBooks › Krimis & Thriller › Thriller › Wirtschaftsthriller
Kindle-Shop › eBooks › Literatur & Fiktion › Weltliteratur › Asiatische Literatur › Japan
```

**Inhalte für Erwachsene** Nein
**Verkaufsgebiete** Weltweit

---

## 3. ★ AI開示（必須）

KDP は、本文・画像・**翻訳**にAIを使ったかを申告させる。このドイツ語版は
**AIの支援で翻訳した**ので、*Übersetzungen*（Translations）は **Ja／Yes** と答える。
誤って申告すると販売停止になることがある。

---

## 4. ★ 表紙（未着手）

- 1600 × 2560 px、JPEG または TIFF、RGB、72dpi以上、50MB未満
- 文字：**DAS LETZTE KASSENBUCH** ／ *Ein Erbe in drei Teilen* ／ **Kazu A. Suzuki**
- 日本語版・英語版と同じ絵に文字だけ載せ替えると、シリーズとしてそろう

---

## 5. 価格

- 約34,600語。ドイツ語の中編〜短めの長編。紙換算でおよそ160〜180ページ
- 70%ロイヤリティの価格帯は Amazon.de で 2,99〜9,99 €（**税込で設定する**。ドイツはVAT 7%込みの表示）
- 新人作家の第1巻なら **2,99〜3,99 €** が置きやすい
- ドイツは書籍の再販価格維持制度（Buchpreisbindung）があり、電子書籍も対象。
  Amazon.de で決めた価格が、ドイツ国内の他ストアでも同じ価格でなければならない
  （KDPセレクトで Amazon 独占にするなら気にしなくてよい）

---

## 6. 出版前チェックリスト

- [x] 著者名 `Kazu A. Suzuki`（`dc:creator`、扉、Impressum）
- [x] EPUB の XML 検証済み、`mimetype` 非圧縮で先頭
- [ ] 表紙画像（1600 × 2560 px）
- [ ] KDP プレビューアで確認：左開き、段落の字下げ、`※` の区切り、„…“ の引用符
- [ ] 目次（Inhalt）から全章に飛べるか
- [ ] 帳簿の最新の一行が *10. Februar 2026…* になっているか（和暦の中で唯一の西暦）
- [ ] AI開示（3.）
- [ ] 内容紹介の末尾に第2巻の予告を入れるか
