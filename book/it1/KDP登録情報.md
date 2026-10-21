# イタリア語版『L'Ufficio dei Sogni』KDP登録情報

第一巻のイタリア語版です。貼り付ける中身はイタリア語、説明は日本語で書いてあります。

主戦場は amazon.it です。

---

## 1. 本の詳細

| 項目 | 内容 |
|---|---|
| Titolo | L'Ufficio dei Sogni |
| Sottotitolo | Dodici notti |
| Serie | L'Ufficio dei Sogni（Libro 1） |
| 巻番号 | 1 |
| Autore | Kazu A. Suzuki |
| 出版言語 | Italiano |
| ISBN | 不要 |

---

## 2. Descrizione（そのまま貼り付け可）

I sogni non si cancellano. Si possono soltanto alleggerire.

Mentre dormite, il cervello ammorbidisce un ricordo, lo rilega e lo lascia fissarsi di nuovo. L'edizione dei sogni è il mestiere che assiste a quei pochi secondi e modifica, di molto poco, la mano che rilega.

Non si può fare altro che abbassare il peso di un ricordo. In una notte, 0,05 al massimo. Nel mestiere lo chiamano la mezzatinta.

Il limite non esiste per insufficienza della tecnica. Se si assottiglia un ricordo troppo in fretta, la traccia della riscrittura se ne va con lui. Finché la traccia resta, si può dire a sé stessi: questo è un sogno montato. Ciò che il limite protegge non è il sogno di chi dorme. È il margine che resta dopo, al risveglio, per dubitare della propria memoria.

Dodici racconti collegati, in un paese dove quella tecnica è entrata fino all'ultimo angolo della vita ordinaria.

- Una ragazza di tredici anni che chiede di lasciare in pace il proprio incubo — «Mezzatinta»
- Una donna che attende quattro anni e sette mesi e rinuncia il giorno del suo turno — «La lista d'attesa dell'oblio»
- Una vedova a cui consegnano le scuse che il marito non ha mai saputo dire, sintetizzate dai suoi diari, e una figlia che chiama quella cosa una contraffazione — «Il testamento»
- Una madre a cui leggono ogni mese una storia chiara e consolante, tradotta dai sogni di un figlio senza linguaggio — «Il traduttore»
- Un tecnico che eleva il rimorso di un omicida da 0,07 a 0,81 nel corso di quindici notti — «La pena»
- Un luogo di lavoro dove il trattamento del dolore è obbligatorio entro quarantotto ore, e un uomo che non lo accetta — «Il lutto per delega»

Non ci sono cattivi. Ci sono soltanto persone che fanno il loro lavoro correttamente, conformemente alla norma, e un campo che la norma non ha mai previsto.

Ogni racconto sta da sé. Più si avanza, più diventa chiaro che cosa questo paese chiami da sempre felicità.

INDICE
I. Mezzatinta
II. La lista d'attesa dell'oblio
III. Il testamento
IV. Il traduttore
V. Il sogno in seconda persona
VI. L'imposta sui sogni
VII. Il lutto per delega
VIII. La pena
IX. Il diritto di non svegliarsi
X. La successione
XI. Indice di Felicità 98
XII. Il soggetto silenzioso

Circa 22.700 parole.

---

## 3. Parole chiave（7つ）

1. `fantascienza letteraria`
2. `distopia futuro prossimo`
3. `racconti collegati`
4. `memoria e identità`
5. `fantascienza contemplativa racconti`
6. `distopia burocratica romanzo`
7. `fantascienza giapponese in italiano`

**入れてはいけないもの**：他の作家名や既存作品名。他の言語版と同じ注意です。

---

## 4. Categorie（最大3つ）

1. Narrativa → Fantascienza → Antologie e racconti
2. Narrativa → Narrativa letteraria
3. Narrativa → Fantascienza → Distopie

---

## 5. 価格とロイヤリティ

| 項目 | 推奨 |
|---|---|
| ロイヤリティ | 70%プラン |
| 価格 | 3,99 €（イタリア） |
| KDPセレクト | 登録する |

70%プランが使えるのは **2,99 €〜9,99 €** の範囲です。独・西・仏語版と揃えてあります。

**付加価値税。** イタリアの電子書籍は軽減税率（4%）です。スペインと同じ率で、
五言語でいちばん手取りが多くなります（独7%・仏5,5%）。ロイヤリティは税抜額に
対してかかります。

**KDPセレクト。** 90日間の独占は**言語版ごと**に数えます。イタリア語版を
セレクトに入れても、他の五言語版の扱いには影響しません。

---

## 6. アップロードするファイル

| 用途 | ファイル |
|---|---|
| 原稿 | `book/dist/L'Ufficio dei Sogni.epub` |
| 表紙 | `book/dist/cover_it1.jpg`（1600×2560px、1.6:1） |

```bash
python3 book/tools/build_epub.py it1
python3 book/tools/build_cover.py it1
```

（検証: 日本語版第一巻の表紙と、字のない下半分を画素比較して差分ゼロ。EPUBは
mimetype が無圧縮で先頭、CRC・XML整形式・`dc:language` が it、
`page-progression-direction` が ltr、章12・spine14。カポラーリの開きが
本文に900個生き残っていることも確認済み）

---

## 7. 翻訳について

**日本語の原文から訳しています**（他の言語版からの重訳ではありません）。
原文51.718字 → 伊文22.666 words（比0.438）。六言語でいちばん語数が少なく、
仏語の0.495より12%ほど締まります。

### 会話はカポラーリ（« »）で組んであります

これがイタリア語版でいちばん大きな判断です。西語・仏語はダッシュで組みますが、
イタリア語文芸書の標準はカポラーリです。ダッシュで組むとスペイン語からの
翻訳書に見えます。カポラーリの内側に空白は入れません（«così» であって
« così » ではない）。

```
«Non lo cancelli, la prego.»
«Non lo cancellerò», disse Kaji. «Non esiste una tecnica per cancellare.»
```

**書類からの引用だけはダッシュです。** 原文の `――` にあたる行で、英独西仏の
四版もすべて「全角空白＋ダッシュ」で組んでいます。会話がカポラーリなので、
行頭のダッシュは書類引用だけを意味することになり、かえって区別が明確です。

### 約物と数字

`:` `;` `?` `!` の前に空白を入れません。**これは仏語と逆の規則**で、仏語版の
直後に書いたので最も入りやすい誤りでした。千の位は点（114.206）で、
西語・独語と同じ、仏語の不可分空白とは違います。どちらも検査に入れてあります。

### 主な用語

| 日本語 | Italiano | 理由 |
|---|---|---|
| 夢編集局 | L'Ufficio dei Sogni | 「Ufficio di edizione dei sogni」は題として長い。本文では初出のみ正式名、以降は l'Ufficio |
| 半色 | la mezzatinta | 印刷の網点の語でありながら「半分の色」をそのまま言う。仏 demi-teinte・西 media tinta と同じ幸運で、英語だけ half-shade を造る必要があった。一語で書き、mezza tinta とは書かない |
| 校正官 | il Correttore | 原文の編集／校正という出版の比喩を残す |
| 素片 | il frammento | |
| 情動荷重 | il carico affettivo | |
| 残差 | il residuo | 伊語の統計用語 |
| 夢裁判 | La pena | pena は刑と悲しみの両方を負う。仏語の peine と同じ二重性で、この話が一人の男に据えつけるのはまさにその両方。英 The Sentence / 独 Das Strafmaß / 西 La condena のどれも刑の側しか運べない |
| 涙の代筆 | Il lutto per delega | 「per delega」は委任状の語で、行政の語感が残る |
| 夢の相続 | La successione | 伊語の相続法の語 |

---

## 8. 出版前チェックリスト

- [x] 全十二話の翻訳を終えた
- [x] `check_tr_structure.py` が0件で通ることを確認した（字下げ・三字下げの塊も）
- [x] `check_tr_terms.py` が0件で通ることを確認した（小数・桁区切り・約物・カポラーリも）
- [x] `check_tr_quotes.py` の定型句が0件で通ることを確認した
- [x] `check_overlap.py` が0件で通ることを確認した（英独西仏伊の五言語）
- [x] 表紙の帯が日本語版第一巻と一致していることを画素比較で確認した
- [x] EPUBの構造を確認した（mimetype・CRC・XML・lang・方向・章数・カポラーリ）
- [ ] Kindle Previewerで表示を三機種確認した（アクセント記号・カポラーリを特に）
- [ ] Descrizione を貼り付けた
- [ ] Parole chiave 7つを入れた
- [ ] Categorie を3つ選んだ
- [ ] 価格を設定し、税抜額を確認した（伊4%）
- [ ] KDPセレクトの可否を決めた
