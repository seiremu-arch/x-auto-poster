# フランス語版『Le Nivellement』KDP登録情報

第二巻のフランス語版です。貼り付ける中身はフランス語、説明は日本語で書いてあります。

主戦場は amazon.fr ですが、amazon.ca（ケベック）と amazon.be にも同時に出ます。

---

## 1. 本の詳細

| 項目 | 内容 |
|---|---|
| Titre | Le Nivellement |
| Sous-titre | Le Bureau des Rêves, Livre Deux |
| Série | Le Bureau des Rêves（Livre 2） |
| 巻番号 | 2 |
| Auteur | Kazu A. Suzuki |
| 出版言語 | Français |
| ISBN | 不要 |

シリーズ名はフランス語版第一巻と**一字一句同じ**（`Le Bureau des Rêves`）に
してください。違うとシリーズページが別々に作られます。

---

## 2. Description（そのまま貼り付け可）

Le Nivellement. C'est le nom d'un projet d'État qui rapproche de la moyenne, nuit après nuit, le poids des souvenirs d'un million de personnes.

Pendant que vous dormez, le cerveau ramollit un souvenir, le relie à nouveau et le laisse se fixer de nouveau. L'édition des rêves intervient dans ces quelques secondes pour baisser le poids, et en une nuit 0,05 au maximum peuvent être déplacés. Dans le métier, on appelle cela la demi-teinte.

Si le Livre I, Le Bureau des Rêves, traitait d'un technicien et d'un demandeur assis face à face, ces douze nouvelles se passent après : quand la technique est devenue d'abord une industrie, puis un système, et enfin quelque chose de la taille d'un pays.

- Une société où trois heures de sommeil suffisent, et une entreprise qui vend, dans les quarante minutes restantes, les sentiments des autres — « La ville qui ne dort pas »
- Une intervention prénatale qui forme sécurité, confiance et curiosité chez un fœtus. Ce sur quoi elle agissait, ce n'était pas les enfants — « Fondations »
- Le chagrin transféré à un auteur a déjà été retiré aux proches à l'instant du prélèvement — « L'injection d'empathie »
- Taux d'automatisation, 98,4 pour cent, et le dernier artisan qui porte les 1,6 restants — « Le dernier artisan »
- Un homme à qui l'on a rendu les choses plus lourdes pendant sept nuits sans son consentement, et qui refuse qu'on les lui remette — « Violences »
- Un incendie avec dix-neuf morts dont personne ne se souvient et qui n'est écrit nulle part — « Le registre »

Il n'y a pas de méchants. Il n'y a que des gens qui, dans leurs services, font leur travail correctement. La Répartition change quelque chose pour le taux d'utilisation ; l'Analyse des anomalies, pour le coût de la correction ; la Gestion technique, par manque d'effectifs. Il n'y a aucun indice qu'ils se soient parlé.

Ce qui s'est produit quand les trois raisonnements sont tombés dans le même trimestre s'éclaire dans la dernière nouvelle, « Le rapport de clôture ».

Chaque nouvelle se tient seule. Le Livre I n'est pas nécessaire.

SOMMAIRE
I. La ville qui ne dort pas
II. Fondations
III. L'injection d'empathie
IV. Le dernier artisan
V. La machine rêve-t-elle ?
VI. Violences
VII. Le registre
VIII. La mer des rêves
IX. Le rêve de demain
X. Le dernier bug
XI. Résidu
XII. Le rapport de clôture

Environ 24 700 mots.

---

## 3. Mots-clés（7つ）

1. `science-fiction littéraire`
2. `dystopie futur proche`
3. `nouvelles liées`
4. `dystopie bureaucratique roman`
5. `mémoire et identité`
6. `science-fiction contemplative nouvelles`
7. `science-fiction japonaise en français`

第一巻と同じ七語です。順番だけ、この巻の中身（官僚機構の側に寄っている）に
合わせて四番目を上げました。

---

## 4. Catégories（最大3つ）

1. Romans et littérature → Science-fiction → Anthologies et nouvelles
2. Romans et littérature → Science-fiction → Dystopies
3. Romans et littérature → Littérature générale

第一巻は2番と3番が逆です。この巻はディストピアの比重が高いので入れ替えました。

---

## 5. 価格とロイヤリティ

| 項目 | 推奨 |
|---|---|
| ロイヤリティ | 70%プラン |
| 価格 | 3,99 €（フランス） |
| KDPセレクト | 登録する |

70%プランが使えるのは **2,99 €〜9,99 €** の範囲です。第一巻・独語版・西語版と
揃えてあります。

**付加価値税。** フランスの電子書籍は軽減税率（5,5%）です。ロイヤリティは
税抜額に対してかかります。カナダ（amazon.ca）は税率も通貨も別なので、登録画面で
自動換算させたうえで税抜額を確認してください。

**KDPセレクト。** 90日間の独占は**言語版ごと**に数えます。フランス語版を
セレクトに入れても、他の四言語版の扱いには影響しません。

---

## 6. アップロードするファイル

| 用途 | ファイル |
|---|---|
| 原稿 | `book/dist/Le Nivellement.epub` |
| 表紙 | `book/dist/cover_fr2.jpg`（1600×2560px、1.6:1） |

```bash
python3 book/tools/build_epub.py fr2
python3 book/tools/build_cover.py fr2
```

（検証: 日本語版第二巻の表紙と、字のない下半分を画素比較して差分ゼロ。英・独・西の
第二巻とも一致し、第一巻族とは違うことも確認済み。EPUBは mimetype が無圧縮で先頭、
CRC・XML整形式・`dc:language` が fr、`page-progression-direction` が ltr、
章12・spine14。本文中の不可分空白384個がEPUBに生き残っていることも確認済み）

---

## 7. 翻訳について

**日本語の原文から訳しています**（他の言語版からの重訳ではありません）。
原文48,719字 → 仏文24,709 words（比0.507）。五言語でいちばん嵩みます。

会話は長ダッシュ（—）で組んでいます。約物前の不可分空白と組み方の理由は
第一巻の登録情報に書いたとおりです。小数点は読点（0,038）、**千の位は不可分空白**
（1 027 400）。

### この巻で新しく出た用語

| 日本語 | Français | 理由 |
|---|---|---|
| 均し計画 | le Plan de Nivellement | 表題の `Le Nivellement` は本文の計画名と同語源 |
| 第二次同期 | la Deuxième Synchronisation | 第一巻XIIの `synchronisation` を受ける |
| 共有者数 | le nombre de codétenteurs | XIで研究者が論文で名づける造語。codétenteur は民法の共同所持の語で、同じ出来事を分け持つ者という意味を素直に負う |
| 窪み | le creux | Xの「同じ形の窪み」 |
| 保持記録 | les registres conservés | V・VIII・X・XI・XIIを貫く |
| 下方編集 | l'édition à la baisse | |
| 引きずり | l'entraînement | 第一巻Iから継承 |
| 先行確定 | la fixation anticipée | IXの配分用語 |
| 余剰成分 | le composant excédentaire | V・Xに共通 |
| 最後のバグ | le dernier bug | 原文は 不具合（公式語）と バグ（現場の通称）を書き分けている。仏語も同じ対が使えるので、公式分類は anomalie légère connue、通称は bug。bogue にすると語感の差が消える |

### 巻をまたぐ引用

第八話は、第一巻の第二話・第四話・第十二話と、この巻の第六話に出た文を、
保管庫に残った記録としてそのまま引用します。五件すべてが一字一句一致することを
`check_tr_quotes.py` で確認済みです（英・独・西・仏の四言語を同時に見ます）。

仏語の五件は、訳す**前**に対応表へ登録しました。表を記録ではなく仕様として
置くことで、第四話を書くときに別の言い回しを選べば検査が鳴ります。

---

## 8. 出版前チェックリスト

- [x] 全十二話の翻訳を終えた
- [x] `fix_fr_spacing.py` を通した
- [x] `check_tr_structure.py` が0件で通ることを確認した
- [x] `check_tr_terms.py` が0件で通ることを確認した
- [x] `check_tr_quotes.py` が0件で通ることを確認した（引用5件・定型句3件）
- [x] `check_overlap.py` が0件で通ることを確認した（英・独・西・仏の四言語）
- [x] 表紙の帯が日本語版第二巻と一致していることを画素比較で確認した
- [x] EPUBの構造を確認した（mimetype・CRC・XML・lang・方向・章数・不可分空白）
- [ ] Kindle Previewerで表示を三機種確認した（アクセント記号・約物前の空白を特に）
- [ ] Description を貼り付けた
- [ ] Mots-clés 7つを入れた
- [ ] Catégories を3つ選んだ
- [ ] シリーズ名が第一巻と一字一句同じか確認した
- [ ] 価格を設定し、税抜額を確認した（仏5,5%・加は別税率）
- [ ] KDPセレクトの可否を決めた
