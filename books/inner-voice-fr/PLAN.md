# 企画書 — フランス語版『La voix la plus basse』

日本語版 `books/inner-voice/` の**書き直し**であって、翻訳ではない
(方針と反証条件は Vault `899744d0ff`)。芯・章構成・実践の番号は揃え、
場面と例、そして**読者との距離**を決め直す。

## 書誌

| 項目 | 内容 |
| --- | --- |
| Titre | La voix la plus basse |
| Sous-titre | Sept exercices pour distinguer votre propre voix du bruit dans votre tête |
| Auteur | Kazu A. Suzuki(日本語版・英語版・ドイツ語版と同一表記) |
| 言語 | フランス語(Amazon.fr を主戦場にする。.be / .ca / .ch も同じ本で届く) |
| 分量 | 15,700 words 前後(日本語版 33,075字 ÷ 実測 2.10字/word。→ Vault `899744d0ff` の追記) |
| 想定価格 | 4,99 €(70%ロイヤリティの範囲は 2,99〜9,99 €) |

## 芯にする一文

> Votre voix la plus basse ne parlera jamais plus fort. Il ne reste donc qu'à faire silence de votre côté.

四言語のどれかを直すときは四つとも直す(`--check` が一致を見る)。

## 読者との距離

**`vous` で書く**(→ Vault `e778004e3b`)。ドイツ語版の `du` とは逆だが、守っている距離は同じ。
フランス語の développement personnel では `tu` がコーチング寄りの語り口と結びついていて、
この本が避けている調子になる。

`vous` でも命令形の連続は起きうるので、手順の節の外では裸の指示を使わない。
`check_style.py` で検査する。

## 日本語版から動かさないもの

- 四つの声 — la voix anxieuse / la voix du « il faut » / la voix empruntée / la voix la plus basse
- 二つの基準 — **la vitesse**(l'ordre d'arrivée)と **le corps**(ça se relâche / ça se serre)
- 七つの実践の中身と番号。所要時間も変えない
- 章の順番と、各章が担う主張
- 約束しないこと(効果の断定をしない / 医療の代替にしない / 検証できない語を使わない)

## 日本語版から差し替えるもの

| 章 | 日本語版の場面 | フランス語版の場面 |
| --- | --- | --- |
| 序章 | 眠れない夜に二十行書く | 同じ(文化に依存しない) |
| 1 | 金曜の飲みの誘い「その仕事、辞めたら?」 | un dîner le vendredi : « Démissionne, tout simplement. » |
| 2 | 誘いに即答した三日後 | « Je viens ! » tapé en trois secondes dans un groupe |
| 3 | 内見した部屋の玄関で肩が上がる | la troisième visite d'appartement(そのまま使う) |
| 4 | レンジの二分・信号待ち | le micro-ondes, l'ascenseur, la file à la caisse |
| 5 | 会議で部長に数字を指摘される | une réunion à sept, un chiffre faux dans la présentation |
| 6 | 三年ぶりの分岐点は金曜の夜、誘いを断った | 同じ形(une invitation déclinée) |
| 7 | 三週間目に何も来なくなった | 同じ(文化に依存しない) |

第1章の友人の台詞だけは `tu` のまま。登場人物どうしの会話であって、読者への語りかけではない。

## 出す前に確かめること

- **タイトルの重複。** Amazon.fr で « La voix la plus basse » を検索する
- 命令形が手順の節の外に出ていないか(`check_style.py`)
- 本文が硬すぎないか(`vous` が距離を作りすぎていないか。claim `e778004e3b` の反証条件)
- 免責の文が、医療行為の否定と読まれない書き方になっているか

## 現在地

- [x] 企画・構成(日本語版からの対応表)/ 読者との距離の判断
- [x] Avant-propos
- [x] Chapitre 1 Combien de voix parlent en ce moment
- [x] Chapitre 2 Distinguer par la vitesse
- [x] Chapitre 3 Distinguer dans le corps
- [x] Chapitre 4 Faire de la place
- [x] Chapitre 5 Écrire pour entendre
- [x] Chapitre 6 Décider petit
- [x] Chapitre 7 Les jours où vous n'entendez rien
- [x] Conclusion / Annexe
- [x] 通しの推敲(命令形・禁止語・約物の空白・章ごとの語数比)/ EPUB / KDP登録シート(`LISTING.md`)
- [x] 表紙(四言語で同じデザイン、文字だけフランス語に)(`python scripts/build_cover.py inner-voice-fr`)
- [ ] **著者の一人称の性**(→ Vault `dba7c10f3f`)。目視で約21か所が男性形のまま(`check_style.py` が拾えるのはそのうち16か所)。
      著者の答え(男性形 / 女性形 / 性が出ない言い方)を待っている。
      `check_style.py` が件数を「確認待ち」として出す
- [ ] タイトルの重複確認(Amazon.fr)/ KDP登録
