# フランス語版『Le Bureau des Rêves』KDP登録情報

第一巻のフランス語版です。貼り付ける中身はフランス語、説明は日本語で書いてあります。

主戦場は amazon.fr ですが、amazon.ca（ケベック）と amazon.be にも同時に出ます。

---

## 1. 本の詳細

| 項目 | 内容 |
|---|---|
| Titre | Le Bureau des Rêves |
| Sous-titre | Douze nuits |
| Série | Le Bureau des Rêves（Livre 1） |
| 巻番号 | 1 |
| Auteur | Kazu A. Suzuki |
| 出版言語 | Français |
| ISBN | 不要 |

---

## 2. Description（そのまま貼り付け可）

Les rêves ne s'effacent pas. Ils ne peuvent qu'être allégés.

Pendant que vous dormez, le cerveau ramollit un souvenir, le relie à nouveau et le laisse se fixer de nouveau. L'édition des rêves est le métier qui assiste à ces quelques secondes et modifie, très peu, la main qui relie.

On ne peut rien faire d'autre que baisser le poids d'un souvenir. En une nuit, 0,05 au maximum. Dans le métier, on appelle cela la demi-teinte.

La limite n'existe pas par insuffisance de la technique. Si l'on amincit un souvenir trop vite, la trace de la réécriture s'en va avec lui. Tant que la trace demeure, on peut se dire : ceci est un rêve édité. Ce que la limite protège, ce n'est pas le rêve de qui dort. C'est la marge qui reste ensuite, au réveil, pour douter de sa propre mémoire.

Douze nouvelles liées, dans un pays où cette technique est entrée jusqu'au dernier recoin de la vie ordinaire.

- Une jeune fille de treize ans qui demande qu'on laisse son cauchemar tranquille — « Demi-teinte »
- Une femme qui attend quatre ans et sept mois et renonce le jour de son tour — « La file d'attente de l'oubli »
- Une veuve à qui l'on remet les excuses que son mari n'a jamais su dire, synthétisées d'après ses journaux, et une fille qui appelle cela une contrefaçon — « Le testament »
- Une mère à qui l'on lit chaque mois une histoire claire et consolante, traduite des rêves d'un fils sans langage — « Le traducteur »
- Un technicien qui élève le remords d'un meurtrier de 0,07 à 0,81 au long de quinze nuits — « La peine »
- Un lieu de travail où la tramitation du deuil est obligatoire en quarante-huit heures, et un homme qui ne l'accepte pas — « Le deuil par procuration »

Il n'y a pas de méchants. Il n'y a que des gens qui font leur travail correctement, conformément à la norme, et un champ que la norme n'a jamais prévu.

Chaque nouvelle se tient seule. Plus on avance, plus il devient clair ce que ce pays appelle depuis toujours le bonheur.

SOMMAIRE
I. Demi-teinte
II. La file d'attente de l'oubli
III. Le testament
IV. Le traducteur
V. Le rêve à la deuxième personne
VI. L'impôt sur les rêves
VII. Le deuil par procuration
VIII. La peine
IX. Le droit de ne pas se réveiller
X. La succession
XI. Indice de Bonheur 98
XII. Le sujet silencieux

Environ 25 600 mots.

---

## 3. Mots-clés（7つ）

1. `science-fiction littéraire`
2. `dystopie futur proche`
3. `nouvelles liées`
4. `mémoire et identité`
5. `science-fiction contemplative nouvelles`
6. `dystopie bureaucratique roman`
7. `science-fiction japonaise en français`

**入れてはいけないもの**：他の作家名や既存作品名。他の言語版と同じ注意です。

---

## 4. Catégories（最大3つ）

1. Romans et littérature → Science-fiction → Anthologies et nouvelles
2. Romans et littérature → Littérature générale
3. Romans et littérature → Science-fiction → Dystopies

---

## 5. 価格とロイヤリティ

| 項目 | 推奨 |
|---|---|
| ロイヤリティ | 70%プラン |
| 価格 | 3,99 €（フランス） |
| KDPセレクト | 登録する |

70%プランが使えるのは **2,99 €〜9,99 €** の範囲です。独語版・西語版と揃えてあります。

**付加価値税。** フランスの電子書籍は軽減税率（5,5%）です。ロイヤリティは税抜額に
対してかかるので、同じ 3,99 € でも手取りはドイツ（7%）より少し多く、
スペイン（4%）より少し少なくなります。カナダ（amazon.ca）は税率も通貨も別なので、
登録画面で自動換算させたうえで税抜額を確認してください。

**KDPセレクト。** 90日間の独占は**言語版ごと**に数えます。フランス語版を
セレクトに入れても、他の四言語版の扱いには影響しません。

---

## 6. アップロードするファイル

| 用途 | ファイル |
|---|---|
| 原稿 | `book/dist/Le Bureau des Rêves.epub` |
| 表紙 | `book/dist/cover_fr1.jpg`（1600×2560px、1.6:1） |

```bash
python3 book/tools/build_epub.py fr1
python3 book/tools/build_cover.py fr1
```

（検証: 日本語版第一巻の表紙と、字のない下半分を画素比較して差分ゼロを確認済み。
EPUBは mimetype が無圧縮で先頭、CRC・XML整形式・`dc:language` が fr、
`page-progression-direction` が ltr、章12・spine14。約物前の不可分空白が
EPUB本文に生き残っていることも確認済み）

---

## 7. 翻訳について

**日本語の原文から訳しています**（英語版・ドイツ語版・スペイン語版からの重訳では
ありません）。原文51,718字 → 仏文25,600 words（比0.495）。四言語でいちばん
語数が多く、英語の0.463より7%ほど嵩みます。

### 会話は長ダッシュ（—）で組んであります

フランス語は会話をギュメ（« »）で囲む組み方と、返答ごとに長ダッシュを置く
組み方の両方を許します。後者のほうが現代の文芸書の標準で、しかも原文と段落が
一対一で対応するので、欠落検出の検査がそのまま使えます。

```
— Ne l'effacez pas, je vous en prie.
— Je ne vais pas l'effacer, dit Kaji. Il n'existe pas de technique pour effacer.
```

### 約物の前の不可分空白

`:` `;` `?` `!` の前と « » の内側に不可分空白（U+00A0）が要ります。これは
フランス語の規則で、入れないとリーダーで行が変なところで折れます。二十四話ぶんを
手で打つと必ずどこかで落ちるので、`fix_fr_spacing.py` で機械的に入れ、
`check_tr_terms.py` で検査しています。U+202F（細い空白）ではなく U+00A0 を
使うのは、U+202F がKindleの全フォントで出ないためです。

### 数字

小数点は読点（0,05）。**千の位は点ではなく不可分空白**（51 718）。ここが
西語・独語との分かれ目で、言語をまたいで作業していて最も入りやすい誤りなので、
検査に入れてあります。

### 主な用語

| 日本語 | Français | 理由 |
|---|---|---|
| 夢編集局 | Le Bureau des Rêves | 「Bureau d'édition des rêves」は題として長い。本文では初出のみ正式名、以降は le Bureau |
| 半色 | la demi-teinte | **四言語でいちばん幸運な訳。** 印刷の網点の語でありながら「半分の色」をそのまま言う。英語は half-shade を造り、独語は Halbton、西語は media tinta を借りたが、仏語には既製の正解があった |
| 校正官 | le Correcteur | 原文の編集／校正という出版の比喩を残す |
| 素片 | le fragment | |
| 情動荷重 | la charge affective | |
| 残差 | le résidu | 仏語の統計用語 |
| 夢裁判 | La peine | peine は刑と悲しみの両方を負う。この話が一人の男に据えつけるのはまさにその両方で、英 The Sentence / 独 Das Strafmaß / 西 La condena のどれも刑の側しか運べない |
| 涙の代筆 | Le deuil par procuration | 「par procuration」は代理投票の語で、行政の語感が残る |
| 夢の相続 | La succession | 仏語の相続法の語 |

### 第一巻の原文を一字直しました

第三話の第三節、謝ろうとした三度の一度目が「桐山が転勤の話を断った夜」に
なっていました。桐山は技師で、転勤を断ったのは宮田恒男です。英・独・西の
三版はいずれも代名詞で訳していて字面としては通っていましたが、原文の誤りは
残ったままでした。主語を落とす形に直し、四言語の第一巻EPUBを再生成しています。

---

## 8. 出版前チェックリスト

- [x] 全十二話の翻訳を終えた
- [x] `fix_fr_spacing.py` を通した
- [x] `check_tr_structure.py` が0件で通ることを確認した（字下げ・三字下げの塊も）
- [x] `check_tr_terms.py` が0件で通ることを確認した（小数・桁区切り・約物の空白も）
- [x] `check_tr_quotes.py` の定型句が0件で通ることを確認した
- [x] `check_overlap.py` が0件で通ることを確認した（英・独・西・仏の四言語）
- [x] 表紙の帯が日本語版第一巻と一致していることを画素比較で確認した
- [x] EPUBの構造を確認した（mimetype・CRC・XML・lang・方向・章数・不可分空白）
- [ ] Kindle Previewerで表示を三機種確認した（アクセント記号・ギュメ・約物前の空白を特に）
- [ ] Description を貼り付けた
- [ ] Mots-clés 7つを入れた
- [ ] Catégories を3つ選んだ
- [ ] 価格を設定し、税抜額を確認した（仏5,5%・加は別税率）
- [ ] KDPセレクトの可否を決めた
