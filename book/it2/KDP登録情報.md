# イタリア語版『Il Livellamento』KDP登録情報

第二巻のイタリア語版です。貼り付ける中身はイタリア語、説明は日本語で書いてあります。

主戦場は amazon.it です。

---

## 1. 本の詳細

| 項目 | 内容 |
|---|---|
| Titolo | Il Livellamento |
| Sottotitolo | L'Ufficio dei Sogni, Libro Due |
| Serie | L'Ufficio dei Sogni（Libro 2） |
| 巻番号 | 2 |
| Autore | Kazu A. Suzuki |
| 出版言語 | Italiano |
| ISBN | 不要 |

シリーズ名はイタリア語版第一巻と**一字一句同じ**（`L'Ufficio dei Sogni`）に
してください。アポストロフィも ASCII の `'` で揃えます。曲がったアポストロフィ
（`’`）を使うとシリーズページが別々に作られます。

---

## 2. Descrizione（そのまま貼り付け可）

Il Livellamento. È il nome di un piano statale che avvicina alla media, notte dopo notte, il peso dei ricordi di un milione di persone.

Mentre dormite, il cervello ammorbidisce un ricordo, lo rilega e lo lascia fissarsi di nuovo. L'edizione dei sogni interviene in quei pochi secondi e abbassa il peso: in una notte si possono spostare 0,05 al massimo. Nel mestiere lo chiamano la mezzatinta.

Se il Libro I, L'Ufficio dei Sogni, trattava di un tecnico e di un richiedente seduti uno di fronte all'altro, questi dodici racconti vengono dopo: quando la tecnica è diventata prima un'industria, poi un sistema, e infine una cosa della taglia di un paese.

- Una società in cui bastano tre ore di sonno, e un'azienda che nei quaranta minuti rimasti vende i sentimenti degli altri — «La città che non dorme»
- Un intervento prenatale che forma sicurezza, fiducia e curiosità in un feto. Ciò su cui agiva non erano i bambini — «Fondazioni»
- Il dolore trasferito a uno scrittore è già stato tolto ai familiari nell'istante del prelievo — «L'iniezione di empatia»
- Tasso di automazione 98,4 per cento, e l'ultimo artigiano che porta l'1,6 restante — «L'ultimo artigiano»
- Un uomo a cui per sette notti hanno reso le cose più pesanti senza il suo consenso, e che rifiuta che gliele si rimettano a posto — «Lesioni»
- Un incendio con diciannove morti di cui nessuno si ricorda e che non è scritto in nessun luogo — «Il registro»

Non ci sono cattivi. Ci sono soltanto persone che, nei loro servizi, fanno il loro lavoro correttamente. La Ripartizione cambia qualcosa per il tasso di utilizzo; l'Analisi anomalie, per l'entità del costo della correzione; la Gestione tecnica, per mancanza di personale. Non c'è traccia che si siano parlati.

Che cosa si sia prodotto quando i tre ragionamenti sono caduti nello stesso trimestre si chiarisce nell'ultimo racconto, «La relazione di chiusura».

Ogni racconto sta da sé. Il Libro I non è necessario.

INDICE
I. La città che non dorme
II. Fondazioni
III. L'iniezione di empatia
IV. L'ultimo artigiano
V. La macchina sogna?
VI. Lesioni
VII. Il registro
VIII. Il mare dei sogni
IX. Il sogno di domani
X. L'ultimo bug
XI. Residuo
XII. La relazione di chiusura

Circa 21.800 parole.

---

## 3. Parole chiave（7つ）

1. `fantascienza letteraria`
2. `distopia futuro prossimo`
3. `racconti collegati`
4. `distopia burocratica romanzo`
5. `memoria e identità`
6. `fantascienza contemplativa racconti`
7. `fantascienza giapponese in italiano`

第一巻と同じ七語です。順番だけ、この巻の中身（官僚機構の側に寄っている）に
合わせて四番目を上げました。英・独・西・仏の第二巻と同じ入れ替えです。

---

## 4. Categorie（最大3つ）

1. Narrativa → Fantascienza → Antologie e racconti
2. Narrativa → Fantascienza → Distopie
3. Narrativa → Narrativa letteraria

第一巻は2番と3番が逆です。この巻はディストピアの比重が高いので入れ替えました。

---

## 5. 価格とロイヤリティ

| 項目 | 推奨 |
|---|---|
| ロイヤリティ | 70%プラン |
| 価格 | 3,99 €（イタリア） |
| KDPセレクト | 登録する |

70%プランが使えるのは **2,99 €〜9,99 €** の範囲です。第一巻・独語版・西語版・
仏語版と揃えてあります。

**付加価値税。** イタリアの電子書籍は軽減税率（4%）です。スペインと同じ率で、
六言語でいちばん手取りが多くなります（独7%・仏5,5%）。ロイヤリティは税抜額に
対してかかります。

**KDPセレクト。** 90日間の独占は**言語版ごと**に数えます。イタリア語版を
セレクトに入れても、他の五言語版の扱いには影響しません。

---

## 6. アップロードするファイル

| 用途 | ファイル |
|---|---|
| 原稿 | `book/dist/Il Livellamento.epub` |
| 表紙 | `book/dist/cover_it2.jpg`（1600×2560px、1.6:1） |

```bash
python3 book/tools/build_epub.py it2
python3 book/tools/build_cover.py it2
```

（検証: 日本語版第二巻の表紙と画素比較して、差分は題字と著者名の矩形
`(168, 307)-(1297, 947)` の内側だけ。英・独・西・仏の第二巻とまったく同じ矩形で、
帯の地模様が一致していることを確認済み。EPUBは mimetype が無圧縮で先頭、
CRC・XML整形式・`dc:language` が it、`page-progression-direction` が ltr、
章12・spine14。本文のカポラーリは開き785・閉じ785で釣り合っており、
ASCII引用符は0個、約物前の不可分空白も0個（仏語版と逆）、
ピリオドは千の位だけに3箇所）

---

## 7. 翻訳について

**日本語の原文から訳しています**（他の言語版からの重訳ではありません）。
原文48.719字 → 伊文21.839 words（比0.448）。六言語でいちばん語数が少なく、
仏語の0.507より12%ほど締まります。

会話はカポラーリ（« »）で組んでいます。内側に空白は入れません。約物の前に
空白を入れないのはイタリア語の規則で、**仏語とは正反対**です（`così:` であって
`così :` ではない）。小数点は読点（0,038）、千の位は点（1.027.400）。

### この巻で新しく出た用語

| 日本語 | Italiano | 理由 |
|---|---|---|
| 均し計画 | il Piano di Livellamento | 表題の `Il Livellamento` は本文の計画名と同語源 |
| 第二次同期 | la Seconda Sincronizzazione | 第一巻XIIの `sincronizzazione` を受ける |
| 共有者数 | il numero di compartecipi | XIで研究者が論文で名づける造語。compartecipe は同じものを分け持つ者の語で、同じ出来事を分け持つという意味を素直に負う |
| 窪み | l'incavo | Xの「同じ形の窪み」 |
| 保持記録 | i registri conservati | V・VIII・X・XI・XIIを貫く |
| 混入率 | il tasso di contaminazione | XIIが第一巻XIIの読み手報告を四十一年後に開く。第一巻の訳語をそのまま使う |
| 分散 | la varianza | 統計の用語。XIIの完了要件はこの一語で書かれている |
| 下方編集 | l'edizione al ribasso | |
| 引きずり | il trascinamento | 第一巻Iから継承 |
| 先行確定 | la fissazione anticipata | IXの配分用語 |
| 余剰成分 | il componente eccedente | V・Xに共通 |
| 最後のバグ | l'ultimo bug | 原文は 不具合（公式語）と バグ（現場の通称）を書き分けている。伊語も同じ対が使えるので、公式分類は anomalia lieve nota、通称は bug |

### 巻をまたぐ引用

第八話は、第一巻の第二話・第四話・第十二話と、この巻の第六話に出た文を、
保管庫に残った記録としてそのまま引用します。五件すべてが一字一句一致することを
`check_tr_quotes.py` で確認済みです（英・独・西・仏・伊の五言語を同時に見ます）。

伊語の五件は、訳す**前**に対応表へ登録しました。表を記録ではなく仕様として
置くことで、第四話を書くときに別の言い回しを選べば検査が鳴ります。

### 伊語版で足した検査

イタリア語は過去分詞の性数一致と接続法があるので、他の五言語より人が読んで
直した箇所が多い巻です。機械で拾える分は検査に足しました。

- カポラーリ検査：原文の**段落**が `　「` で始まるなら、伊文の同じ段落に `«`
  があること。行単位で数えると、長い文書名を二行に割った話で誤報が出ます
- `scc` の連続：`sceso` を `scceso` と書く誤りが三話で出ました
- 仏語・西語の機能語の混入：`contrecuore`（伊語は `a malincuore`）、
  `rognare`（伊語では別の意味。削るは `limare`）、`grimace`（伊語は `smorfia`）

---

## 8. 出版前チェックリスト

- [x] 全十二話の翻訳を終えた
- [x] `check_tr_structure.py` が0件で通ることを確認した
- [x] `check_tr_terms.py` が0件で通ることを確認した
- [x] `check_tr_quotes.py` が0件で通ることを確認した（引用5件・定型句3件）
- [x] `check_overlap.py` が0件で通ることを確認した（英・独・西・仏・伊の五言語）
- [x] 表紙の帯が日本語版第二巻と一致していることを画素比較で確認した
- [x] EPUBの構造を確認した（mimetype・CRC・XML・lang・方向・章数・カポラーリ）
- [ ] Kindle Previewerで表示を三機種確認した（アクセント記号・カポラーリを特に）
- [ ] Descrizione を貼り付けた
- [ ] Parole chiave 7つを入れた
- [ ] Categorie を3つ選んだ
- [ ] シリーズ名が第一巻と一字一句同じか確認した（アポストロフィも）
- [ ] 価格を設定し、税抜額を確認した（伊4%）
- [ ] KDPセレクトの可否を決めた
