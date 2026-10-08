# オランダ語版の方針と対訳表

『最後の帳簿　三つに分けられた遺産』の蘭訳。`manuscript/`（日本語）が原本、
`manuscript-nl/` が訳文。**底本は日本語原文。** ほかの版（英・独・仏・西・伊）は、
固有名詞と言い回しの決め方をそろえるための参照にだけ使う。

## 基本方針

1. **舞台は日本のまま。** 円は円（*yen*、複数形も yen）、法制度は日本の法制度。
2. **人名は名→姓**（Shuji Kamiya）。ほかの版と同じ。
3. **敬称。** 台詞では meneer／mevrouw＋姓（*meneer Kamiya*, *mevrouw Tachibana*, *mevrouw Sagara*）。
   遠野家の3人も *meneer Tono*／*mevrouw Tono* で呼ぶ（「-san」は残さない。
   誰のことかは場面で分かる）。第三者に言及するときは名で呼ぶ（Ryosuke, Chizuru）。
4. **u／jij。** 夫婦、兄妹、克巳から千鶴、宗一郎から子どもたちは jij。それ以外は u。
   亮介が神谷を「あんた」と呼ぶ場面だけ jij に落として、無礼さを出す。
5. **台詞は ‘ ’（一重引用符）で括る。** オランダの小説で一般的な形。入れ子は “ ”。
   アポストロフィは半角の `'`（'s, z'n, foto's）。台詞の閉じと混ざらないようにするため。
   ‘ ’ の対応とアポストロフィの書き方は `check_nl.py` で検査する。
6. **法律用語に脚注をつけない。** 台詞の中で一度だけ説明する。
7. **文体。** 短い平叙文。感情の形容詞を使わない。段落は短く。`※` の区切りはそのまま。
8. **数字。** 台詞と地の文の金額は語で書く（*achtentwintig miljoen yen*）。
   帳票は `72.043.518`、`¥ 1.480`、一覧は `21,4 mln`。日付は `10 februari 2026`、時刻は `18.40 uur`。
   階数はヨーロッパ式（日本の3階 = *tweede verdieping*）。

## 数字の対比（ほかの版と同じ置き換え）

| | 日本語版 | オランダ語版 |
|---|---|---|
| 歴代の行 | 昭和十六年十二月 | *Showa 16, twaalfde maand* |
| 〃 | 平成三年 | *Heisei 3* |
| 宗一郎の行 | 2026年2月10日 | **10 februari 2026** |

## 固有名詞

| 日本語 | Nederlands |
|---|---|
| 本家 | het stamhuis |
| 遠野精工（株式会社） | Tono Precisie (bv) |
| 遠野建装 | Bouwbedrijf Tono |
| 上州あかぎ銀行 宇賀野支店 | Joshu Akagi Bank, filiaal Ugano |
| 群馬中央信用金庫 | Coöperatieve Kredietbank Gunma Chuo |
| 北関東証券 | Kita-Kanto Securities |
| 白鷺開発 | Shirasagi Development (nv) |
| 梶原FPオフィス | Kajiwara Financiële Planning |
| 前田不動産 | Makelaardij Maeda |
| 宇賀野中央法律事務所 | Advocatenkantoor Ugano Chuo |
| 北関東データセンター構想 | het datacenterproject Noord-Kanto |
| ホームセンター栄和 | Eiwa Bouwmarkt |
| リョウ・クリエイト / 〈Arclight Capital〉 / 〈TAKA〉 | Ryo Create (bv) / Arclight Capital / TAKA |
| 東京 | Tokio（オランダ語の綴り） |

人名・地名は英語版と同じ（`TRANSLATION.md`）。

## 法律・金融の語

| 日本語 | Nederlands |
|---|---|
| 公正証書遺言 | notarieel testament（afschrift van de grosse） |
| 遺言執行者 | executeur |
| 遺留分 | de legitieme portie（オランダ法にもある語なので、そのまま通じる） |
| 付言事項 | de persoonlijke toelichting（「法的効力はない」と第26章で説明される） |
| 四十九日 | de negenenveertigste dag |
| 月命日 | de maandelijkse gedenkdag |
| 信託 / 受託者 / 受益権 | trust / trustbank als trustee / recht als begunstigde |
| 遺贈 | legaat |
| 連帯保証（人） | hoofdelijke borgstelling / hoofdelijk borg |
| 稟議（書） | kredietvoorstel |
| 試算表 / 粉飾 | proefbalans / vervalste cijfers |
| 固定資産評価証明書 | uittreksel van de WOZ-waarde |
| 路線価 / 倍率地域 | wegwaarde / zone met een vermenigvuldigingsfactor（橘の台詞で一行説明） |
| 延納 | uitstel van betaling, jaarlijkse termijnen |
| 実印 / 印鑑証明 | geregistreerd zegel / zegelregistratiebewijs |
| 公証役場 | notaris |
| 任意同行 | vrijwillig naar het bureau komen |
| 公訴の取り消し | de aanklacht is ingetrokken |
| 鍵の受け渡し簿 | het sleutelschrift（表紙は *Sleutels*） |

## 繰り返される言い回し

| 日本語 | Nederlands |
|---|---|
| すべてを一つに賭けた者には、一円も残すな | **Laat wie alles op één kaart heeft gezet geen enkele yen na.** |
| 毎月、決まった額を、決まった日に／それだけ？／それだけです | **Elke maand hetzelfde bedrag, op dezelfde dag.** / *Meer niet?* / *Meer niet.* |
| 私は、何もしていません。／何もしなかっただけです。 | **Ik heb niets gedaan.** / **Ik heb het alleen laten gebeuren.** |
| 2026年2月10日　三つに分けた　もう一つ　分けられなかったものがある | **10 februari 2026　in drieën gedeeld　er is er nog één　die ik niet kon delen** |
| 階段から落ちて死んだのなら、それは事故ではありません | **Als ik door een val van de trap ben gestorven, dan was het geen ongeluk.** |
| 片づける人のやり方です | **Zo doet iemand die dingen opbergt.** |
| 金を失ったことのある人間にしか、金の見張りは頼めない | **Alleen iemand die zelf geld heeft verloren kun je vragen op geld te passen.** |
| 金を守れた人間には…／守れなかった人間だけが、どこで手が滑るかを知っている | *Wie zijn geld heeft kunnen houden, kun je niet vragen op geld te passen.* / *Alleen wie het niet heeft kunnen houden, weet waar je hand wegglijdt.* |
| 間に合わなかったんですか | **Dus ik was te laat?** |
| いちばん重いものを持とうとする | **wil het zwaarste dragen** |
| もういいんです | **Het hoeft niet meer.** |
| 三つの籠 | de drie manden |
| 土地／事業／現金（封筒に書く三つ） | **Grond / Bedrijf / Geld** |

「すべてを一つに賭けた」には、分散の話にそのまま重なる慣用句 *alles op één kaart zetten* を使った。

## 帳簿の七つの記号

漢字を出し、地の文で意味を添える。土 aarde ／ 種 zaad ／ 木 boom ／ 蜜 honing ／ 鍵 sleutel ／ 手 hand ／ 水 water

## タイトル

- シリーズ: **Het laatste kasboek**
- 第1巻: **Het laatste kasboek: Een erfenis in drie delen**

## 章題

| 章 | 原題 | オランダ語 |
| --- | --- | --- |
| 序 | プロローグ | Proloog |
| 1 | 誘導灯 | De lichtstaaf |
| 2 | 消印 | Het poststempel |
| 3 | 11日 | De elfde |
| 4 | 三つの籠 | De drie manden |
| 5 | 1996年 | 1996 |
| 6 | 杭 | De piketpaaltjes |
| 7 | 番頭 | De rentmeester |
| 8 | 差額 | Het verschil |
| 9 | 封をする紙 | Het verzegelde papier |
| 10 | 勝ち組の側 | Aan de kant van de winnaars |
| 11 | 三つの値段 | Drie prijzen |
| 12 | 四つの穴 | Vier gaten |
| 13 | 2月5日 | 5 februari |
| 14 | 三分の一 | Een derde |
| 15 | 相良 | Sagara |
| 16 | 四回目 | De vierde keer |
| 17 | 任意 | Vrijwillig |
| 18 | 一回だけ | Maar één keer |
| 19 | 名簿 | De lijst |
| 20 | もういいんです | Het hoeft niet meer |
| 21 | 立てかけてあった | Tegen de muur |
| 22 | 三つ | Drie |
| 23 | 何もしなかった | Ik heb niets gedaan |
| 24 | 2月10日 | 10 februari |
| 25 | 連絡先 | Contactpersoon |
| 26 | 四通目 | De vierde envelop |
| 27 | 定期 | Termijndeposito |
| 終 | エピローグ | Epiloog |

章題はオランダ語の慣例どおり、最初の語と固有名詞だけを大文字にした。
第7章「番頭」は、会社の帳場を預かる人という意味で *De rentmeester*（英語版の *The Steward* に近い）。
第21章 *Tegen de muur* は「立てかけてあった」手すりのこと。
第23章は千鶴の最後の台詞から *Ik heb niets gedaan* とし、
続く「何もしなかっただけです」は *Ik heb het alleen laten gebeuren.*（起きるのに任せただけ）と訳した（伊語版と同じ判断）。
第27章「定期」は *Termijndeposito*（神谷の嘘「定期に入れてある」と同じ語）。

訳しているあいだに、日本語原文の新しい傷は見つからなかった。
