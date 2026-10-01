# フランス語版の方針と対訳表

『最後の帳簿　三つに分けられた遺産』の仏訳。`manuscript/`（日本語）が原本、
`manuscript-fr/` が訳文。**底本は日本語原文。** 英語版・ドイツ語版は、
固有名詞と言い回しの決め方をそろえるための参照にだけ使う。

## 基本方針

1. **舞台は日本のまま。** 円は円（*yens*）、法制度は日本の法制度。
2. **人名は名→姓**（Shuji Kamiya）。ほかの版と同じ。
3. **敬称。** 遠野家は4人とも姓が同じなので、家族は台詞の中で「-san」を残す
   （Ryosuke-san, Chizuru-san）。姓で呼ぶ相手は monsieur／madame
   （*monsieur Kamiya*, *madame Tachibana*, *madame Sagara*）。
4. **tu／vous。** 夫婦（神谷と佳代子）、兄妹（亮介と千鶴）、克巳から千鶴、宗一郎から子どもたちは tu。
   それ以外はすべて vous。
5. **法律用語に脚注をつけない。** 台詞の中で一度だけ説明する。
6. **文体。** 短い平叙文。感情の形容詞を使わない。段落は短く。`※` の区切りはそのまま。
7. **フランス語の組版規則。** 台詞は « … »。`? ! ;` の前は細い改行なしスペース（U+202F）、
   `:` と « » の内側は改行なしスペース（U+00A0）。書くときは普通のスペースで書き、
   `fr_typo.py` で一括変換する（何度かけても同じ結果になる）。
8. **数字。** 台詞と地の文の金額は語で書く（*vingt-huit millions de yens*）。
   帳票はフランス式（`72 043 518`、`1 480 ¥`）。日付は `10 février 2026`、時刻は `18 h 40`。

## 数字の対比（英語版・ドイツ語版と同じ置き換え）

| | 日本語版 | フランス語版 |
|---|---|---|
| 歴代の行 | 昭和十六年十二月 | *Showa 16, douzième mois* |
| 〃 | 平成三年 | *Heisei 3* |
| 宗一郎の行 | 2026年2月10日 | **10 février 2026** |

## 固有名詞

| 日本語 | Français |
|---|---|
| 遠野精工 | Tono Précision |
| 遠野建装 | Tono Construction |
| 上州あかぎ銀行 宇賀野支店 | Banque Joshu-Akagi, agence d'Ugano |
| 群馬中央信用金庫 | Crédit coopératif Gunma Chuo |
| 北関東証券 | Kita-Kanto Securities |
| 白鷺開発 | Shirasagi Development |
| 梶原FPオフィス | Kajiwara Conseil patrimonial |
| 前田不動産 | Agence immobilière Maeda |
| 宇賀野中央法律事務所 | Cabinet Ugano Chuo |
| 北関東データセンター構想 | le projet de centre de données du Nord-Kanto |
| ホームセンター栄和 | magasin de bricolage Eiwa |
| リョウ・クリエイト / 〈Arclight Capital〉 / 〈TAKA〉 | Ryo Create / Arclight Capital / TAKA |

人名・地名は英語版と同じ（`TRANSLATION.md`）。

## 法律・金融の語

| 日本語 | Français |
|---|---|
| 公正証書遺言 | testament authentique（公証人が作る遺言。フランス法の同名の制度に近い） |
| 遺言執行者 | exécuteur testamentaire |
| 遺留分 | réserve héréditaire（フランス法にもある概念なので、そのまま通じる） |
| 付言事項 | la note personnelle（「法的効力はない」と第26章で説明される） |
| 四十九日 | le quarante-neuvième jour（第9章で「cérémonie bouddhique」と一度添える） |
| 月命日 | le jour de commémoration mensuelle |
| 信託 / 受託者 / 受益権 | fiducie / fiduciaire / droit de bénéficiaire |
| 連帯保証（人） | caution solidaire |
| 稟議（書） | dossier de crédit |
| 試算表 / 粉飾 | situation intermédiaire / comptes maquillés |
| 倍率地域 | zone à coefficient（橘の台詞で一行説明） |
| 実印 / 印鑑証明 | sceau officiel / certificat d'enregistrement du sceau |
| 公証役場 | l'office notarial |
| 任意同行 | audition libre（フランスの制度名がちょうど合う） |
| 公訴の取り消し | abandon des poursuites |

## 繰り返される言い回し

| 日本語 | Français |
|---|---|
| すべてを一つに賭けた者には、一円も残すな | **À qui a tout misé sur une seule chose, ne laissez pas un seul yen.** |
| 毎月、決まった額を、決まった日に／それだけ？／それだけです | **Chaque mois, la même somme, le même jour.** / *C'est tout ?* / *C'est tout.* |
| 私は、何もしていません。／何もしなかっただけです。 | **Je n'ai rien fait.** / **J'ai seulement laissé faire.** |
| 2026年2月10日　三つに分けた　もう一つ　分けられなかったものがある | **10 février 2026　j'ai divisé en trois　il en reste une　que je n'ai pas pu diviser** |
| 階段から落ちて死んだのなら、それは事故ではありません | **Si je suis mort en tombant dans l'escalier, ce n'était pas un accident.** |
| 片づける人のやり方です | **C'est ainsi que fait quelqu'un qui range.** |
| 金を失ったことのある人間にしか、金の見張りは頼めない | **On ne peut confier la garde de l'argent qu'à quelqu'un qui en a déjà perdu.** |
| 間に合わなかったんですか | **Alors je suis arrivée trop tard ?** |
| いちばん重いものを持とうとする | **Elle veut toujours porter le plus lourd.** |
| もういいんです | **Ce n'est plus la peine.** |
| 三つの籠 | les trois paniers |

## 帳簿の七つの記号

漢字を出し、地の文で意味を添える。土 terre ／ 種 graine ／ 木 arbre ／ 蜜 miel ／ 鍵 clé ／ 手 main ／ 水 eau

## タイトル

- シリーズ: **Le Dernier Livre de comptes**
- 第1巻: **Le Dernier Livre de comptes : Un héritage en trois parts**

## 章題（フランス語版）

| | 日本語 | Français |
|---|---|---|
| 序 | プロローグ | Prologue |
| 1 | 誘導灯 | Le bâton lumineux |
| 2 | 消印 | Le cachet de la poste |
| 3 | 11日 | Le onze |
| 4 | 三つの籠 | Les trois paniers |
| 5 | 1996年 | 1996 |
| 6 | 杭 | Les piquets |
| 7 | 番頭 | L'intendant |
| 8 | 差額 | L'écart |
| 9 | 封をする紙 | Le papier scellé |
| 10 | 勝ち組の側 | Du côté des gagnants |
| 11 | 三つの値段 | Trois prix |
| 12 | 四つの穴 | Quatre trous |
| 13 | 2月5日 | Le 5 février |
| 14 | 三分の一 | Un tiers |
| 15 | 相良 | Sagara |
| 16 | 四回目 | La quatrième fois |
| 17 | 任意 | Audition libre |
| 18 | 一回だけ | Une seule fois |
| 19 | 名簿 | La liste |
| 20 | もういいんです | Ce n'est plus la peine |
| 21 | 立てかけてあった | Appuyée contre le mur |
| 22 | 三つ | Trois |
| 23 | 何もしなかった | Je n'ai rien fait |
| 24 | 2月10日 | Le 10 février |
| 25 | 連絡先 | Personne à prévenir |
| 26 | 四通目 | La quatrième enveloppe |
| 27 | 定期 | Dépôt à terme |
| 終 | エピローグ | Épilogue |

章題はフランス語の慣例どおり、最初の語と固有名詞だけを大文字にした。
第27章「定期」は *Dépôt à terme*（神谷の嘘の定期預金）。「毎月、決まった額を、決まった日に」の
意味は本文の決め台詞に任せた（英語版・ドイツ語版と同じ判断）。

訳しているあいだに、日本語原文の新しい傷は見つからなかった
（ドイツ語版のときに直した4か所は、直したあとの原文から訳している）。

