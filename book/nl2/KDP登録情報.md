# オランダ語版『De Nivellering』KDP登録情報

第二巻のオランダ語版です。貼り付ける中身はオランダ語、説明は日本語で書いてあります。

主戦場は amazon.nl ですが、amazon.com.be（ベルギー）にも同時に出ます。

---

## 1. 本の詳細

| 項目 | 内容 |
|---|---|
| Titel | De Nivellering |
| Ondertitel | Het Droombureau, Deel Twee |
| Serie | Het Droombureau（Deel 2） |
| 巻番号 | 2 |
| Auteur | Kazu A. Suzuki |
| 出版言語 | Nederlands |
| ISBN | 不要 |

シリーズ名はオランダ語版第一巻と**一字一句同じ**（`Het Droombureau`）に
してください。違うとシリーズページが別々に作られます。

---

## 2. Beschrijving（そのまま貼り付け可）

De Nivellering. Zo heet een staatsplan dat het gewicht van de herinneringen van een miljoen mensen, nacht na nacht, naar het gemiddelde brengt.

Terwijl u slaapt, maakt het brein een herinnering zacht, bindt haar opnieuw en laat haar zich weer vastzetten. De droomredactie grijpt in die paar seconden in en verlaagt het gewicht; in één nacht kan er ten hoogste 0,05 worden verplaatst. In het vak heet dat de halftint.

Ging Deel I, Het Droombureau, over een technicus en een aanvrager die tegenover elkaar zitten, dan komen deze twaalf verhalen daarna: wanneer de techniek eerst een bedrijfstak is geworden, toen een stelsel, en ten slotte iets van de omvang van een land.

- Een samenleving waarin drie uur slaap genoeg is, en een bedrijf dat in de veertig minuten die overblijven de gevoelens van anderen verkoopt — De stad die niet slaapt
- Een ingreep voor de geboorte die bij een ongeboren kind geborgenheid, vertrouwen en nieuwsgierigheid vormt. Waar zij op werkte, waren niet de kinderen — Fundamenten
- Het verdriet dat naar een dader wordt overgebracht, is de nabestaanden op het ogenblik van de afname al afgenomen — De empathie-injectie
- Percentage automatische verwerking 98,4, en de laatste ambachtsman die de resterende 1,6 draagt — De laatste ambachtsman
- Een man bij wie zeven nachten zonder zijn instemming de dingen zwaarder zijn gemaakt, en die weigert ze te laten terugzetten — Mishandeling
- Een brand met negentien doden die niemand zich herinnert en die nergens is opgeschreven — Het register

Er zijn geen slechteriken. Er zijn alleen mensen die op hun afdeling hun werk correct doen. De Verdeling verandert iets om het bezettingspercentage; de Storingsanalyse om de omvang van de correctiekosten; Technisch Beheer uit tekort aan personeel. Er is geen spoor dat zij met elkaar hebben gesproken.

Wat zich voordeed toen de drie redeneringen in hetzelfde kwartaal bij elkaar kwamen, komt in het laatste verhaal aan het licht, Het eindrapport.

Elk verhaal staat op zichzelf. Deel I is niet nodig.

INHOUD
I. De stad die niet slaapt
II. Fundamenten
III. De empathie-injectie
IV. De laatste ambachtsman
V. Droomt de machine?
VI. Mishandeling
VII. Het register
VIII. De zee van dromen
IX. De droom van morgen
X. De laatste bug
XI. Residu
XII. Het eindrapport

Ongeveer 24.000 woorden.

---

## 3. Trefwoorden（7つ）

1. `literaire sciencefiction`
2. `dystopie nabije toekomst`
3. `samenhangende verhalenbundel`
4. `bureaucratische dystopie roman`
5. `geheugen en identiteit`
6. `beschouwende sciencefiction verhalen`
7. `japanse sciencefiction in het nederlands`

第一巻と同じ七語です。順番だけ、この巻の中身（官僚機構の側に寄っている）に
合わせて四番目を上げました。他の五言語の第二巻と同じ入れ替えです。

---

## 4. Categorieën（最大3つ）

1. Literatuur en fictie → Sciencefiction en fantasy → Sciencefiction → Anthologieën en korte verhalen
2. Literatuur en fictie → Sciencefiction en fantasy → Sciencefiction → Dystopisch
3. Literatuur en fictie → Literaire fictie

第一巻は2番と3番が逆です。この巻はディストピアの比重が高いので入れ替えました。

---

## 5. 価格とロイヤリティ

| 項目 | 推奨 |
|---|---|
| ロイヤリティ | 70%プラン |
| 価格 | 3,99 €（オランダ） |
| KDPセレクト | 登録する |

70%プランが使えるのは **2,99 €〜9,99 €** の範囲です。第一巻・独・西・仏・伊語版と
揃えてあります。

**付加価値税。** オランダの電子書籍は軽減税率（9%）です。六言語でいちばん
税率が高く、西・伊の4%より手取りが少なくなります。ベルギー（amazon.com.be）は
6%です。ロイヤリティは税抜額に対してかかります。

**KDPセレクト。** 90日間の独占は**言語版ごと**に数えます。オランダ語版を
セレクトに入れても、他の五言語版の扱いには影響しません。

---

## 6. アップロードするファイル

| 用途 | ファイル |
|---|---|
| 原稿 | `book/dist/De Nivellering.epub` |
| 表紙 | `book/dist/cover_nl2.jpg`（1600×2560px、1.6:1） |

```bash
python3 book/tools/build_epub.py nl2
python3 book/tools/build_cover.py nl2
```

（検証: 日本語版第二巻の表紙と画素比較して、差分は題字と著者名の矩形
`(168, 307)-(1297, 947)` の内側だけ。英・独・西・仏・伊の第二巻とまったく
同じ矩形で、帯の地模様が一致していることを確認済み。EPUBは mimetype が
無圧縮で先頭、CRC・XML整形式・`dc:language` が nl、
`page-progression-direction` が ltr、章12・spine14。本文の引用符は
開き764・閉じ764で釣り合っており、ASCII引用符0個、約物前の空白0個、
ピリオドは千の位だけ）

---

## 7. 翻訳について

**日本語の原文から訳しています**（他の言語版からの重訳ではありません）。
原文48.719字 → 蘭文24.065 words（比0.494）。仏語の0.507に次いで嵩み、
伊語の0.449より10%ほど多くなります。

会話は二重引用符（“ ”）で組んでいます。一重にしなかった理由は第一巻の
登録情報に書いたとおりです。約物の前に空白は入れません（仏語と逆）。
小数点は読点（0,038）、千の位は点（1.027.400）。

### この巻で新しく出た用語

| 日本語 | Nederlands | 理由 |
|---|---|---|
| 均し計画 | het Nivelleringsplan | 表題の `De Nivellering` は本文の計画名と同語源 |
| 第二次同期 | de Tweede Synchronisatie | 第一巻XIIの `synchronisatie` を受ける |
| 共有者数 | het aantal deelgenoten | XIで研究者が論文で名づける造語。deelgenoot は共同所有者を指す法律語で、同じ出来事を分け持つという意味を素直に負う |
| 窪み | de holte | Xの「同じ形の窪み」 |
| 保持記録 | de bewaarde registers | V・VIII・X・XI・XIIを貫く |
| 混入率 | het contaminatiepercentage | XIIが第一巻XIIの読み手報告を四十一年後に開く。第一巻の訳語をそのまま使う |
| 分散 | de variantie | 統計の用語。XIIの完了要件はこの一語で書かれている |
| 間 | de speling | IVの「余りじゃなくて、間だ」。speling は機械の遊び（公差）と「余地」の両方を負うので、上限と実際に押す量のあいだという原文の意味がそのまま入る |
| 先行確定 | de voorafgaande vaststelling | IXの配分用語 |
| 余剰成分 | de overtollige component | V・Xに共通 |
| 最後のバグ | de laatste bug | 原文は 不具合（公式語）と バグ（現場の通称）を書き分けている。蘭語も同じ対が使えるので、公式分類は bekende lichte storing、通称は bug |
| 混線 | overspraak | 第一巻VIから継承。電話・電気の用語で、無料枠の素片が隣に漏れる現象にそのまま当たる |

### 巻をまたぐ引用

第八話は、第一巻の第二話・第四話・第十二話と、この巻の第六話に出た文を、
保管庫に残った記録としてそのまま引用します。五件すべてが一字一句一致することを
`check_tr_quotes.py` で確認済みです（六言語を同時に見ます）。

蘭語の五件は、訳す**前**に対応表へ登録しました。表を記録ではなく仕様として
置くことで、第四話を書くときに別の言い回しを選べば検査が鳴ります。

### 蘭語版で足した検査

オランダ語は独語と近く、読んでいて混入に気づきにくいので、機械で拾える分を
検査に足しました。

- **独語の機能語**：`ist` / `und` / `nicht` / `auch` / `sich` / `wurde` /
  `zwischen` / `über` / `nach` / `dem` / `eine` / `nur` / `schon` / `immer`。
  オランダ語に存在しない綴りだけを並べています。オランダ語にもある `den`
  （Den Haag）は入れていません
- **複合語の分かち書き**：`droom redactie` のように分けて書く誤り。オランダ語で
  「英語病」（Engelse ziekte）と呼ばれるもので、この作品の造語は
  ほとんどが複合語なのでいちばん起きやすい
- **比較の als**：`groter als` は話し言葉では広く使われますが、文章では誤りです。
  `zonder meer als` は比較ではないので除いてあります
- **冠詞**：`de fragment` のように het 語に de を付ける誤り。シリーズの造語は
  ほとんどが het 語で、冠詞だけ違っていても通読では気づきません

いずれも、誤った入力を食わせて実際に鳴ることを確かめてから入れています。

---

## 8. 出版前チェックリスト

- [x] 全十二話の翻訳を終えた
- [x] `check_tr_structure.py` が0件で通ることを確認した
- [x] `check_tr_terms.py` が0件で通ることを確認した
- [x] `check_tr_quotes.py` が0件で通ることを確認した（引用5件・定型句3件）
- [x] `check_overlap.py` が0件で通ることを確認した（六言語）
- [x] 表紙の帯が日本語版第二巻と一致していることを画素比較で確認した
- [x] EPUBの構造を確認した（mimetype・CRC・XML・lang・方向・章数・引用符）
- [ ] Kindle Previewerで表示を三機種確認した（引用符の形を特に）
- [ ] Beschrijving を貼り付けた
- [ ] Trefwoorden 7つを入れた
- [ ] Categorieën を3つ選んだ
- [ ] シリーズ名が第一巻と一字一句同じか確認した
- [ ] 価格を設定し、税抜額を確認した（蘭9%・白6%）
- [ ] KDPセレクトの可否を決めた
