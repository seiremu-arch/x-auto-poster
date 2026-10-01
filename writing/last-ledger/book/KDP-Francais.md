# Fiche KDP — *Le Dernier Livre de comptes : Un héritage en trois parts*（フランス語版）

フランス語版は、日本語版・英語版・ドイツ語版とは別の KDP タイトル（別ASIN）として登録する。
以下はそのまま KDP の入力欄に貼れる。**残るのは表紙と価格の2つ。**

---

## 1. 入稿ファイル

| ファイル | 用途 |
| --- | --- |
| `Le_Dernier_Livre_de_comptes_1_Un_heritage_en_trois_parts.epub` | **KDPにアップロードするのはこれ**（横書き・左開き） |
| `Le_Dernier_Livre_de_comptes_1_Un_heritage_en_trois_parts.md` | 統合原稿（読み返し用） |

EPUB3・リフロー、`dc:language` は `fr`、`page-progression-direction="ltr"`。
本文は `../manuscript-fr/*.md`、方針と対訳表は `../TRANSLATION-fr.md`。
フランス語の組版（« » の内側と `: ? ! ;` の前の改行なしスペース）は `../fr_typo.py` で当ててある。

```bash
python3 writing/last-ledger/fr_typo.py              # 本文を直したら先にこれ
python3 writing/last-ledger/build_epub.py --french
```

---

## 2. Détails du livre

**Langue**

```
Français
```

**Titre / Sous-titre**

```
Le Dernier Livre de comptes
Un héritage en trois parts
```

**Série / Numéro**

```
Le Dernier Livre de comptes / 1
```

**Auteur**

```
Prénom : Kazu A.
Nom : Suzuki
```

**Description**（約230語。KDPの上限は4,000字）

```
Il a laissé trois cents millions de yens. Chaque héritier ne pourra en prendre qu'un tiers.

Pendant trente ans, Shuji Kamiya a examiné des dossiers de crédit dans une banque
japonaise — et pendant un an, il a caché à sa femme qu'il avait perdu l'essentiel de
son indemnité de départ dans une escroquerie au placement étranger. Puis arrive par la
poste un vieux livre de comptes. L'expéditeur est un homme qu'il n'a croisé qu'une fois,
il y a trente ans : Soichiro Tono, dont la banque de Kamiya a lâché l'entreprise en 1996.

La lettre jointe dit : « Si je suis mort en tombant dans l'escalier, ce n'était pas un
accident. »

Elle a été postée la veille du jour où Soichiro est tombé dans l'escalier de la maison
familiale, vide.

Son testament divise la succession en terrains, entreprise et liquidités, et oblige
trois héritiers à en choisir chacun une part dans une enveloppe scellée. Si deux
choisissent la même, elle va à une fondation. En note personnelle, il n'a laissé
qu'une ligne : « À qui a tout misé sur une seule chose, ne laissez pas un seul yen. »

Désigné exécuteur testamentaire, Kamiya se met à compter. Du jour au lendemain, le
terrain tombe de cent à vingt millions. De l'argent a disparu à l'étranger. Et dans le
mur de l'escalier, il reste quatre trous de vis, là où se trouvait une rampe.

Un polar financier, sobre et précis, sur l'héritage, l'escroquerie et un crime qui
consiste à ne rien faire. Tome 1 de la série « Le Dernier Livre de comptes ».
```

**Mots-clés**（7つまで）

```
polar japonais
roman policier financier
héritage testament mystère
secret de famille japon
escroquerie placement roman
traduit du japonais
roman noir littéraire
```

**Catégories**（KDPで3つまで。表示名はストアの言語で変わるので、ピッカーで最も近いものを選ぶ）

```
Boutique Kindle › Ebooks Kindle › Policier et suspense › Policier › International
Boutique Kindle › Ebooks Kindle › Policier et suspense › Thriller › Financier
Boutique Kindle › Ebooks Kindle › Littérature › Littérature étrangère › Asie › Japon
```

**Contenu pour adultes** Non
**Territoires** Monde entier

---

## 3. ★ AI開示（必須）

KDP は、本文・画像・**翻訳**にAIを使ったかを申告させる。このフランス語版は
**AIの支援で翻訳した**ので、*Traductions*（Translations）は **Oui／Yes** と答える。
誤って申告すると販売停止になることがある。

---

## 4. ★ 表紙（未着手）

- 1600 × 2560 px、JPEG または TIFF、RGB、72dpi以上、50MB未満
- 文字：**LE DERNIER LIVRE DE COMPTES** ／ *Un héritage en trois parts* ／ **Kazu A. Suzuki**
- ほかの版と同じ絵に文字だけ載せ替えると、シリーズとしてそろう

---

## 5. 価格

- 約40,000語。紙換算でおよそ170〜190ページ
- 70%ロイヤリティの価格帯は Amazon.fr で 2,99〜9,99 €（**税込で設定する**。フランスの電子書籍はVAT 5,5%）
- 新人作家の第1巻なら **2,99〜3,99 €** が置きやすい
- フランスには書籍の定価制度（loi Lang、電子書籍は2011年法）がある。Amazon.fr で決めた価格を
  フランスの他ストアでも同じにしなければならない（KDPセレクトで Amazon 独占にするなら気にしなくてよい）

---

## 6. 出版前チェックリスト

- [x] 著者名 `Kazu A. Suzuki`（`dc:creator`、扉、Mentions légales）
- [x] EPUB の XML 検証済み、`mimetype` 非圧縮で先頭
- [x] フランス語の組版（« » と `: ? ! ;` の前の改行なしスペース）
- [ ] 表紙画像（1600 × 2560 px）
- [ ] KDP プレビューアで確認：左開き、段落の字下げ、`※` の区切り、行末で « や ? が孤立していないか
- [ ] 目次（Table des matières）から全章に飛べるか
- [ ] 帳簿の最新の一行が *10 février 2026…* になっているか（和暦の中で唯一の西暦）
- [ ] AI開示（3.）
- [ ] 内容紹介の末尾に第2巻の予告を入れるか
