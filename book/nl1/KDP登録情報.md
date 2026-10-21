# オランダ語版『Het Droombureau』KDP登録情報

第一巻のオランダ語版です。貼り付ける中身はオランダ語、説明は日本語で書いてあります。

主戦場は amazon.nl ですが、amazon.com.be（ベルギー）にも同時に出ます。
オランダ語の読者はオランダとフランデレン（ベルギー北部）に分かれていて、
人口では合わせて二千四百万人ほどです。

---

## 1. 本の詳細

| 項目 | 内容 |
|---|---|
| Titel | Het Droombureau |
| Ondertitel | Twaalf nachten |
| Serie | Het Droombureau（Deel 1） |
| 巻番号 | 1 |
| Auteur | Kazu A. Suzuki |
| 出版言語 | Nederlands |
| ISBN | 不要 |

---

## 2. Beschrijving（そのまま貼り付け可）

Dromen laten zich niet wissen. Zij laten zich alleen lichter maken.

Terwijl u slaapt, maakt het brein een herinnering zacht, bindt haar opnieuw en laat haar zich weer vastzetten. De droomredactie is het vak dat bij die paar seconden aanwezig is en de hand die bindt een heel klein beetje verzet.

Er is niets anders te doen dan het gewicht van een herinnering verlagen. In één nacht ten hoogste 0,05. In het vak heet dat de halftint.

De grens bestaat niet omdat de techniek tekortschiet. Maak je een herinnering te snel dunner, dan gaat het spoor van de herschrijving met haar mee. Zolang het spoor er is, kan iemand tegen zichzelf zeggen: dit is een geredigeerde droom. Wat de grens beschermt is niet de droom van wie slaapt. Het is de ruimte die daarna, bij het ontwaken, overblijft om aan je eigen geheugen te twijfelen.

Twaalf verbonden verhalen, in een land waar die techniek tot in de laatste hoek van het gewone leven is doorgedrongen.

- Een meisje van dertien dat vraagt haar eigen nachtmerrie te laten staan — Halftint
- Een vrouw die vier jaar en zeven maanden wacht en op de dag van haar beurt afziet — De wachtlijst van de vergetelheid
- Een weduwe die de verontschuldiging in handen krijgt die haar man nooit heeft kunnen uitspreken, gesynthetiseerd uit zijn dagboeken, en een dochter die dat namaak noemt — Het testament
- Een moeder aan wie elke maand een helder, troostend verhaal wordt voorgelezen, vertaald uit de dromen van een zoon zonder taal — De vertaler
- Een technicus die de wroeging van een doodslager in vijftien nachten van 0,07 naar 0,81 brengt — De boete
- Een werkplek waar de behandeling van verdriet binnen achtenveertig uur verplicht is, en een man die zich er niet bij neerlegt — Rouw bij volmacht

Er zijn geen slechteriken. Er zijn alleen mensen die hun werk correct doen, volgens de regeling, en een veld dat de regeling nooit heeft voorzien.

Elk verhaal staat op zichzelf. Hoe verder u komt, hoe duidelijker wordt wat dit land al die tijd geluk heeft genoemd.

INHOUD
I. Halftint
II. De wachtlijst van de vergetelheid
III. Het testament
IV. De vertaler
V. De droom in de tweede persoon
VI. Droombelasting
VII. Rouw bij volmacht
VIII. De boete
IX. Het recht niet te ontwaken
X. De erfopvolging
XI. Geluksindex 98
XII. De zwijgende proefpersoon

Ongeveer 25.500 woorden.

---

## 3. Trefwoorden（7つ）

1. `literaire sciencefiction`
2. `dystopie nabije toekomst`
3. `samenhangende verhalenbundel`
4. `geheugen en identiteit`
5. `beschouwende sciencefiction verhalen`
6. `bureaucratische dystopie roman`
7. `japanse sciencefiction in het nederlands`

**入れてはいけないもの**：他の作家名や既存作品名。他の言語版と同じ注意です。

---

## 4. Categorieën（最大3つ）

1. Literatuur en fictie → Sciencefiction en fantasy → Sciencefiction → Anthologieën en korte verhalen
2. Literatuur en fictie → Literaire fictie
3. Literatuur en fictie → Sciencefiction en fantasy → Sciencefiction → Dystopisch

---

## 5. 価格とロイヤリティ

| 項目 | 推奨 |
|---|---|
| ロイヤリティ | 70%プラン |
| 価格 | 3,99 €（オランダ） |
| KDPセレクト | 登録する |

70%プランが使えるのは **2,99 €〜9,99 €** の範囲です。独・西・仏・伊語版と
揃えてあります。

**付加価値税。** オランダの電子書籍は軽減税率（9%）です。六言語でいちばん
税率が高く、西・伊の4%より手取りが少なくなります。ベルギー（amazon.com.be）は
6%で、同じ値段でも手取りが変わります。ロイヤリティは税抜額に対してかかります。

**KDPセレクト。** 90日間の独占は**言語版ごと**に数えます。オランダ語版を
セレクトに入れても、他の五言語版の扱いには影響しません。

---

## 6. アップロードするファイル

| 用途 | ファイル |
|---|---|
| 原稿 | `book/dist/Het Droombureau.epub` |
| 表紙 | `book/dist/cover_nl1.jpg`（1600×2560px、1.6:1） |

```bash
python3 book/tools/build_epub.py nl1
python3 book/tools/build_cover.py nl1
```

（検証: 日本語版第一巻の表紙と画素比較して、差分は題字と著者名の矩形
`(168, 303)-(1286, 1055)` の内側だけ。英・独・西・仏・伊の第一巻とまったく
同じ矩形で、帯の地模様が一致していることを確認済み。EPUBは mimetype が
無圧縮で先頭、CRC・XML整形式・`dc:language` が nl、
`page-progression-direction` が ltr、章12・spine14。本文の引用符は
開き883・閉じ883で釣り合っており、ASCII引用符0個、約物前の空白0個）

---

## 7. 翻訳について

**日本語の原文から訳しています**（他の言語版からの重訳ではありません）。
原文51.718字 → 蘭文25.487 words（比0.493）。仏語の0.495とほぼ同じで、
伊語の0.438より13%ほど嵩みます。

### 会話は二重引用符（“ ”）で組んであります

これがオランダ語版でいちばん大きな判断です。オランダ文芸は「…」も“…”も‘…’も
使い、文芸書では**一重引用符のほうが普通**です。

それでも二重にしたのは、理由が一つあります。一重だと閉じ引用符が
アポストロフィ（`'s ochtends`、`z'n`、`foto's`）と同じ字になり、開きと閉じの
数が合っているかを機械で数えられません。二重なら数えられて、
`check_tr_terms.py` が話ごとに見ます。検査できない版は、このシリーズでは
一般的な代替案を選んだ版より価値が低いと判断しました。

アポストロフィは他の版と同じく ASCII の `'` です。

```
“Wis het niet, alstublieft.”
“Ik wis het niet,” zei Kaji. “Een techniek om te wissen bestaat niet.”
```

入れ子の引用符は、英・独・西・伊と同じく落としてあります。

### 約物の前に空白を入れません

`zo:` であって `zo :` ではありません。**仏語とは逆の規則**です。仏語版が
同じシリーズにあるので、検査を置いてあります。

### 数字

小数点は読点（`0,038`）、千の位は点（`114.206`）、百分率は `procent`。
独・西・伊と同じ体系で、仏語だけが不可分空白を使う例外です。

### 複合語はつなげて書きます

`droomredactie`、`wachtlijst`、`geluksindex`、`referentieapparaat`。
分けて書くのはオランダ語で「英語病」（Engelse ziekte）と呼ばれる誤りで、
この作品の造語はほとんどが複合語なので、いちばん起きやすい誤りです。
シリーズの用語について検査を置いてあります。

### 独語の混入検査を別に置いています

独語はオランダ語と近いので、`ist` や `und` が残っても**読んでいて気づき
にくい**。仏語や西語の単語なら目に飛び込んでくるのに、独語は飛び込んで
きません。そこでオランダ語に存在しない綴りだけを並べた検査を足しました
（`ist` / `und` / `nicht` / `auch` / `sich` / `wurde` / `zwischen` /
`über` / `nach` / `dem` / `eine` / `nur` / `schon` / `immer`）。
オランダ語にもある `den`（Den Haag）は入れていません。

### この版で難しかった語

| 日本語 | Nederlands | 理由 |
|---|---|---|
| 半色 | de halftint | 印刷の網点の語。原文の色と半歩の両方が残る。仏 demi-teinte・伊 mezzatinta と同じく、オランダ語には語が用意されていた。英語だけ half-shade を造語した |
| 夢裁判 | De boete | boete は罰金と「罪の償い」の両方を負う。仏 peine・伊 pena と同じ二重性で、十五晩かけて一人の男に据えつけられるのは、まさにその二つ |
| 涙の代筆 | Rouw bij volmacht | bij volmacht は法律の「委任による」。原文の事務的な語感をそのまま運ぶ |
| 混入率 | het contaminatiepercentage | 第十二話の指標。第二巻XIIが四十一年後にこれを開く |
| 共有者 | de deelgenoot | 共同所有者を指す法律語。同じ出来事を分け持つという意味を素直に負う |
| 引きずり | het meeslepen | 隣の素片へ力が漏れる現象 |

### 巻をまたぐ引用

第二巻第八話は、この巻の第二話・第四話・第十二話から文をそのまま引用します。
オランダ語の五件は、訳す**前**に `check_tr_quotes.py` の対応表へ登録しました。
表を記録ではなく仕様として置くことで、第四話を書くときに別の言い回しを
選べば検査が鳴ります。

---

## 8. 出版前チェックリスト

- [x] 全十二話の翻訳を終えた
- [x] `check_tr_structure.py` が0件で通ることを確認した
- [x] `check_tr_terms.py` が0件で通ることを確認した
- [x] `check_tr_quotes.py` で第一巻側の引用が通ることを確認した
- [x] `check_overlap.py` が0件で通ることを確認した（六言語）
- [x] 表紙の帯が日本語版第一巻と一致していることを画素比較で確認した
- [x] EPUBの構造を確認した（mimetype・CRC・XML・lang・方向・章数・引用符）
- [ ] Kindle Previewerで表示を三機種確認した（引用符の形を特に）
- [ ] Beschrijving を貼り付けた
- [ ] Trefwoorden 7つを入れた
- [ ] Categorieën を3つ選んだ
- [ ] 価格を設定し、税抜額を確認した（蘭9%・白6%）
- [ ] KDPセレクトの可否を決めた
