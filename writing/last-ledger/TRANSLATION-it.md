# イタリア語版の方針と対訳表

『最後の帳簿　三つに分けられた遺産』の伊訳。`manuscript/`（日本語）が原本、
`manuscript-it/` が訳文。**底本は日本語原文。** ほかの版（英・独・仏・西）は、
固有名詞と言い回しの決め方をそろえるための参照にだけ使う。

## 基本方針

1. **舞台は日本のまま。** 円は円（*yen*、イタリア語では複数形も yen）、法制度は日本の法制度。
2. **人名は名→姓**（Shuji Kamiya）。ほかの版と同じ。
3. **敬称。** 遠野家は台詞の中で「-san」を残す（Ryosuke-san, Chizuru-san）。
   姓で呼ぶ相手は signor／signora／avvocata（*signor Kamiya*, *avvocata Tachibana*, *signora Sagara*）。
4. **tu／lei。** 夫婦、兄妹、克巳から千鶴、宗一郎から子どもたちは tu。それ以外は敬称の lei（小文字で書く、現代の出版の慣例）。
5. **台詞は « »（caporali）で括る。** イタリアの小説で一般的な形。内側にスペースは入れない。
   « » の対応は `check_it.py` で検査する。
6. **法律用語に脚注をつけない。** 台詞の中で一度だけ説明する。
7. **文体。** 短い平叙文。感情の形容詞を使わない。段落は短く。`※` の区切りはそのまま。
8. **数字。** 台詞と地の文の金額は語で書く（*ventotto milioni di yen*）。
   帳票は `72.043.518`、`1.480 ¥`。日付は `10 febbraio 2026`、時刻は `18:40`。

## 数字の対比（ほかの版と同じ置き換え）

| | 日本語版 | イタリア語版 |
|---|---|---|
| 歴代の行 | 昭和十六年十二月 | *Showa 16, dodicesimo mese* |
| 〃 | 平成三年 | *Heisei 3* |
| 宗一郎の行 | 2026年2月10日 | **10 febbraio 2026** |

## 固有名詞

| 日本語 | Italiano |
|---|---|
| 遠野精工 | Tono Precisione |
| 遠野建装 | Costruzioni Tono |
| 上州あかぎ銀行 宇賀野支店 | Banca Joshu-Akagi, filiale di Ugano |
| 群馬中央信用金庫 | Cassa di credito cooperativo Gunma Chuo |
| 北関東証券 | Kita-Kanto Securities |
| 白鷺開発 | Shirasagi Development |
| 梶原FPオフィス | Kajiwara Consulenza Patrimoniale |
| 前田不動産 | Agenzia immobiliare Maeda |
| 宇賀野中央法律事務所 | Studio legale Ugano Chuo |
| 北関東データセンター構想 | il progetto del data center del Kanto Nord |
| ホームセンター栄和 | negozio di bricolage Eiwa |
| リョウ・クリエイト / 〈Arclight Capital〉 / 〈TAKA〉 | Ryo Create / Arclight Capital / TAKA |

人名・地名は英語版と同じ（`TRANSLATION.md`）。

## 法律・金融の語

| 日本語 | Italiano |
|---|---|
| 公正証書遺言 | testamento pubblico（公証人が作る遺言。イタリア法の同名の制度に近い） |
| 遺言執行者 | esecutore testamentario |
| 遺留分 | la legittima（イタリア民法にもある概念なので、そのまま通じる） |
| 付言事項 | la nota personale（「法的効力はない」と第26章で説明される） |
| 四十九日 | il quarantanovesimo giorno（第9章で「cerimonia buddhista」と一度添える） |
| 月命日 | la commemorazione mensile |
| 信託 / 受託者 / 受益権 | trust / banca fiduciaria / diritto del beneficiario |
| 連帯保証（人） | fideiussione solidale / fideiussore |
| 稟議（書） | pratica di fido |
| 試算表 / 粉飾 | situazione contabile provvisoria / bilancio truccato |
| 倍率地域 | zona a coefficiente（橘の台詞で一行説明） |
| 実印 / 印鑑証明 | sigillo registrato / certificato di registrazione del sigillo |
| 公証役場 | lo studio notarile |
| 任意同行 | presentarsi spontaneamente |
| 公訴の取り消し | ritiro dell'accusa |

## 繰り返される言い回し

| 日本語 | Italiano |
|---|---|
| すべてを一つに賭けた者には、一円も残すな | **A chi ha puntato tutto su una cosa sola, non lasciate nemmeno uno yen.** |
| 毎月、決まった額を、決まった日に／それだけ？／それだけです | **Ogni mese, la stessa somma, lo stesso giorno.** / *Tutto qui?* / *Tutto qui.* |
| 私は、何もしていません。／何もしなかっただけです。 | **Io non ho fatto niente.** / **Ho solo lasciato che succedesse.** |
| 2026年2月10日　三つに分けた　もう一つ　分けられなかったものがある | **10 febbraio 2026　l'ho diviso in tre　ne resta una　che non ho potuto dividere** |
| 階段から落ちて死んだのなら、それは事故ではありません | **Se sono morto cadendo dalle scale, non è stato un incidente.** |
| 片づける人のやり方です | **È così che fa chi mette via le cose.** |
| 金を失ったことのある人間にしか、金の見張りは頼めない | **Solo a chi ha già perso del denaro si può chiedere di sorvegliare il denaro.** |
| 間に合わなかったんですか | **Allora sono arrivata tardi?** |
| いちばん重いものを持とうとする | **Vuole sempre portare il peso più grande.** |
| もういいんです | **Non serve più.** |
| 三つの籠 | i tre cesti |

## 帳簿の七つの記号

漢字を出し、地の文で意味を添える。土 terra ／ 種 seme ／ 木 albero ／ 蜜 miele ／ 鍵 chiave ／ 手 mano ／ 水 acqua

## タイトル

- シリーズ: **L'ultimo libro dei conti**
- 第1巻: **L'ultimo libro dei conti: Un'eredità in tre parti**

## 章題

| 章 | 原題 | イタリア語 |
| --- | --- | --- |
| 序 | プロローグ | Prologo |
| 1 | 誘導灯 | Il bastone luminoso |
| 2 | 消印 | Il timbro postale |
| 3 | 11日 | Il giorno undici |
| 4 | 三つの籠 | I tre cesti |
| 5 | 1996年 | 1996 |
| 6 | 杭 | I picchetti |
| 7 | 番頭 | L'amministratore |
| 8 | 差額 | La differenza |
| 9 | 封をする紙 | La carta sigillata |
| 10 | 勝ち組の側 | Dalla parte dei vincenti |
| 11 | 三つの値段 | Tre prezzi |
| 12 | 四つの穴 | Quattro fori |
| 13 | 2月5日 | Il 5 febbraio |
| 14 | 三分の一 | Un terzo |
| 15 | 相良 | Sagara |
| 16 | 四回目 | La quarta volta |
| 17 | 任意 | Spontaneamente |
| 18 | 一回だけ | Una volta sola |
| 19 | 名簿 | La lista |
| 20 | もういいんです | Non serve più |
| 21 | 立てかけてあった | Appoggiato al muro |
| 22 | 三つ | Tre |
| 23 | 何もしなかった | Non ho fatto niente |
| 24 | 2月10日 | Il 10 febbraio |
| 25 | 連絡先 | Persona da contattare |
| 26 | 四通目 | La quarta busta |
| 27 | 定期 | Deposito vincolato |
| 終 | エピローグ | Epilogo |

章題はイタリア語の慣例どおり、最初の語と固有名詞だけを大文字にした。
第21章 *Appoggiato al muro* は「手すり（il corrimano、男性名詞）」を受けている。
第23章は千鶴の最後の台詞「私は、何もしていません」から *Non ho fatto niente* とし、
続く「何もしなかっただけです」は *Ho solo lasciato che succedesse.*（起きるのに任せただけ）と訳した。
第27章「定期」は *Deposito vincolato*（佳代子への嘘「定期に入れてある」と同じ語）。

訳しているあいだに、日本語原文の新しい傷は見つからなかった。
