# Scheda KDP — *L'ultimo libro dei conti: Un'eredità in tre parti*（イタリア語版）

イタリア語版は、ほかの版とは別の KDP タイトル（別ASIN）として登録する。
以下はそのまま KDP の入力欄に貼れる。**残るのは表紙と価格の2つ。**

---

## 1. 入稿ファイル

| ファイル | 用途 |
| --- | --- |
| `L_ultimo_libro_dei_conti_1_Un_eredita_in_tre_parti.epub` | **KDPにアップロードするのはこれ**（横書き・左開き） |
| `L_ultimo_libro_dei_conti_1_Un_eredita_in_tre_parti.md` | 統合原稿（読み返し用） |

EPUB3・リフロー、`dc:language` は `it`、`page-progression-direction="ltr"`。
本文は `../manuscript-it/*.md`、方針と対訳表は `../TRANSLATION-it.md`。
本文を直したら、`../check_it.py` で « » の漏れと内側の空白を確かめてから組む。

```bash
python3 writing/last-ledger/check_it.py
python3 writing/last-ledger/build_epub.py --italian
```

---

## 2. Dettagli del libro

**Lingua**

```
Italiano
```

**Titolo / Sottotitolo**

```
L'ultimo libro dei conti
Un'eredità in tre parti
```

**Serie / Numero**

```
L'ultimo libro dei conti / 1
```

**Autore**

```
Nome: Kazu A.
Cognome: Suzuki
```

**Descrizione**（約240語。KDPの上限は4,000字）

```
Ha lasciato trecento milioni di yen. Ogni erede potrà prenderne solo un terzo.

Per trent'anni Shuji Kamiya ha esaminato pratiche di fido in una banca giapponese, e
da un anno nasconde alla moglie di aver perso quasi tutta la liquidazione in una truffa
d'investimento estera. Poi, per posta, arriva un vecchio libro dei conti. Lo manda un
uomo che ha visto una volta sola, trent'anni prima: Soichiro Tono, la cui azienda la
banca di Kamiya lasciò affondare nel 1996.

La lettera che lo accompagna dice: «Se sono morto cadendo dalle scale, non è stato un
incidente».

È stata spedita il giorno prima che Soichiro cadesse dalle scale della vecchia casa di
famiglia, disabitata.

Il suo testamento divide l'eredità in immobili, azienda e liquidità, e obbliga tre
eredi a scegliere ciascuno una parte in una busta chiusa. Se due scelgono la stessa,
va a una fondazione. Come nota personale ha lasciato una sola riga: «A chi ha puntato
tutto su una cosa sola, non lasciate nemmeno uno yen».

Nominato esecutore testamentario, Kamiya comincia a contare. Da un giorno all'altro il
terreno scende da cento a venti milioni. C'è denaro sparito all'estero. E sul muro
delle scale restano quattro fori di vite, là dove prima c'era un corrimano.

Un giallo finanziario sobrio e preciso, sull'eredità, sulla truffa e su un delitto che
consiste nel non fare niente. Volume 1 della serie «L'ultimo libro dei conti».
```

**Parole chiave**（7つまで）

```
giallo giapponese
thriller finanziario
mistero eredità testamento
segreti di famiglia giappone
truffa investimenti romanzo
tradotto dal giapponese
noir letterario
```

**Categorie**（KDPで3つまで。表示名はストアで変わるので、ピッカーで最も近いものを選ぶ）

```
Kindle Store › eBook Kindle › Gialli e thriller › Gialli › Internazionali
Kindle Store › eBook Kindle › Gialli e thriller › Thriller › Finanziari
Kindle Store › eBook Kindle › Letteratura e narrativa › Narrativa straniera › Asia › Giappone
```

**Contenuti per adulti** No
**Territori** Tutti

---

## 3. ★ AI開示（必須）

KDP は、本文・画像・**翻訳**にAIを使ったかを申告させる。このイタリア語版は
**AIの支援で翻訳した**ので、*Traduzioni*（Translations）は **Sì／Yes** と答える。
誤って申告すると販売停止になることがある。

---

## 4. ★ 表紙（未着手）

- 1600 × 2560 px、JPEG または TIFF、RGB、72dpi以上、50MB未満
- 文字：**L'ULTIMO LIBRO DEI CONTI** ／ *Un'eredità in tre parti* ／ **Kazu A. Suzuki**
- ほかの版と同じ絵に文字だけ載せ替えると、シリーズとしてそろう

---

## 5. 価格

- 約34,000語。紙換算でおよそ150〜170ページ
- 主な市場は Amazon.it（イタリア）。スイスのイタリア語圏の読者も Amazon.it や他国のストアから買う
- 70%ロイヤリティの価格帯は Amazon.it で 2,99〜9,99 €（**税込で設定する**。イタリアの電子書籍はIVA 4%）
- 新人作家の第1巻なら **2,99〜3,99 €** が置きやすい
- イタリアには書籍の値引きの上限を定める法律（Legge Levi、2020年改正）がある。
  電子書籍にどこまで及ぶかは解釈が分かれるので、KDPセレクトに入れず他のストアでも売り、
  ストアごとに値段や値引きを変えたいときは、事前に確認する

---

## 6. 出版前チェックリスト

- [x] 著者名 `Kazu A. Suzuki`（`dc:creator`、扉、Crediti）
- [x] EPUB の XML 検証済み、`mimetype` 非圧縮で先頭
- [x] « » の対応と内側の空白（`check_it.py`）
- [ ] 表紙画像（1600 × 2560 px）
- [ ] KDP プレビューアで確認：左開き、段落の字下げ、`※` の区切り
- [ ] 目次（Indice）から全章に飛べるか
- [ ] 帳簿の最新の一行が *10 febbraio 2026…* になっているか（和暦の中で唯一の西暦）
- [ ] AI開示（3.）
- [ ] 内容紹介の末尾に第2巻の予告を入れるか
