# KDP-gegevens — *Het laatste kasboek: Een erfenis in drie delen*（オランダ語版）

オランダ語版は、ほかの版とは別の KDP タイトル（別ASIN）として登録する。
以下はそのまま KDP の入力欄に貼れる。**残るのは表紙と価格の2つ。**

---

## 1. 入稿ファイル

| ファイル | 用途 |
| --- | --- |
| `Het_laatste_kasboek_1_Een_erfenis_in_drie_delen.epub` | **KDPにアップロードするのはこれ**（横書き・左開き） |
| `Het_laatste_kasboek_1_Een_erfenis_in_drie_delen.md` | 統合原稿（読み返し用） |

EPUB3・リフロー、`dc:language` は `nl`、`page-progression-direction="ltr"`。
本文は `../manuscript-nl/*.md`、方針と対訳表は `../TRANSLATION-nl.md`。
本文を直したら、`../check_nl.py` で ‘ ’ の対応とアポストロフィの書き方を確かめてから組む。

```bash
python3 writing/last-ledger/check_nl.py
python3 writing/last-ledger/build_epub.py --dutch
```

---

## 2. Boekgegevens

**Taal**

```
Nederlands
```

**Titel / Ondertitel**

```
Het laatste kasboek
Een erfenis in drie delen
```

**Reeks / Nummer**

```
Het laatste kasboek / 1
```

**Auteur**

```
Voornaam: Kazu A.
Achternaam: Suzuki
```

**Beschrijving**（約250語。KDPの上限は4,000字）

```
Hij liet driehonderd miljoen yen na. Elke erfgenaam mag er maar een derde van nemen.

Dertig jaar lang beoordeelde Shuji Kamiya kredietaanvragen bij een Japanse bank, en
al een jaar verzwijgt hij voor zijn vrouw dat hij het grootste deel van zijn
afvloeiingsregeling kwijt is aan een buitenlandse beleggingsfraude. Dan komt er per
post een oud kasboek. Het is verstuurd door een man die hij maar één keer heeft
ontmoet, dertig jaar geleden: Soichiro Tono, wiens bedrijf door Kamiya's bank in 1996
werd losgelaten.

In de begeleidende brief staat: ‘Als ik door een val van de trap ben gestorven, dan
was het geen ongeluk.’

De brief is gepost op de dag voordat Soichiro van de trap viel in het lege
familiehuis.

Zijn testament verdeelt de nalatenschap in grond, bedrijf en geld, en dwingt drie
erfgenamen om elk één deel te kiezen in een gesloten envelop. Kiezen er twee
hetzelfde, dan gaat het naar een stichting. Als persoonlijke toelichting liet hij
één regel na: ‘Laat wie alles op één kaart heeft gezet geen enkele yen na.’

Kamiya, aangewezen als executeur, begint te tellen. Van de ene dag op de andere zakt
de grond van honderd naar twintig miljoen. Er is geld verdwenen naar het buitenland.
En in de muur van de trap zitten vier schroefgaten, waar eerst een leuning zat.

Een sobere, precieze financiële thriller over erfenis, fraude en een misdaad die
bestaat uit niets doen. Deel 1 van de reeks ‘Het laatste kasboek’.
```

**Trefwoorden**（7つまで）

```
japanse thriller
financiële thriller
erfenis testament mysterie
familiegeheimen japan
beleggingsfraude roman
vertaald uit het japans
literaire misdaadroman
```

**Categorieën**（KDPで3つまで。表示名はストアで変わるので、ピッカーで最も近いものを選ぶ）

```
Kindle Store › Kindle eBooks › Thrillers › Misdaad › Internationaal
Kindle Store › Kindle eBooks › Thrillers › Financieel
Kindle Store › Kindle eBooks › Literatuur & fictie › Vertaalde literatuur › Japans
```

**Inhoud voor volwassenen** Nee
**Gebieden** Alle

---

## 3. ★ AI開示（必須）

KDP は、本文・画像・**翻訳**にAIを使ったかを申告させる。このオランダ語版は
**AIの支援で翻訳した**ので、*Vertalingen*（Translations）は **Ja／Yes** と答える。
誤って申告すると販売停止になることがある。

---

## 4. ★ 表紙（未着手）

- 1600 × 2560 px、JPEG または TIFF、RGB、72dpi以上、50MB未満
- 文字：**HET LAATSTE KASBOEK** ／ *Een erfenis in drie delen* ／ **Kazu A. Suzuki**
- ほかの版と同じ絵に文字だけ載せ替えると、シリーズとしてそろう

---

## 5. 価格

- 約37,800語。紙換算でおよそ160〜180ページ
- 主な市場は Amazon.nl（オランダ）。ベルギーのフランデレン地方もオランダ語圏
- 価格は**税込で設定する**（オランダの電子書籍は低税率のBTW 9%）。
  70%ロイヤリティを選べる価格帯は、KDPの価格欄に表示される範囲に従う
- 新人作家の第1巻なら **2,99〜3,99 €** が置きやすい（ほかのユーロ圏の版と同じ）
- オランダには本の定価制度（Wet op de vaste boekenprijs）がある。電子書籍に
  どう及ぶかは時期によって扱いが変わってきたので、KDPセレクトに入れず他のストアでも売り、
  ストアごとに値段を変えたいときは、事前に確認する

---

## 6. 出版前チェックリスト

- [x] 著者名 `Kazu A. Suzuki`（`dc:creator`、扉、Colofon）
- [x] EPUB の XML 検証済み、`mimetype` 非圧縮で先頭
- [x] ‘ ’ の対応とアポストロフィ（`check_nl.py`）
- [ ] 表紙画像（1600 × 2560 px）
- [ ] KDP プレビューアで確認：左開き、段落の字下げ、`※` の区切り
- [ ] 目次（Inhoud）から全章に飛べるか
- [ ] 帳簿の最新の一行が *10 februari 2026…* になっているか（和暦の中で唯一の西暦）
- [ ] AI開示（3.）
- [ ] 内容紹介の末尾に第2巻の予告を入れるか
