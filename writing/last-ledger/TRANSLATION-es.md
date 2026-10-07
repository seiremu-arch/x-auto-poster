# スペイン語版の方針と対訳表

『最後の帳簿　三つに分けられた遺産』の西訳。`manuscript/`（日本語）が原本、
`manuscript-es/` が訳文。**底本は日本語原文。** 英語版・ドイツ語版・フランス語版は、
固有名詞と言い回しの決め方をそろえるための参照にだけ使う。

## 基本方針

1. **舞台は日本のまま。** 円は円（*yenes*）、法制度は日本の法制度。
2. **人名は名→姓**（Shuji Kamiya）。ほかの版と同じ。
3. **スペインと中南米の両方で読めるスペイン語にする。** *vosotros* は使わない
   （複数への命令は *ustedes*、または命令形を避ける）。語彙も地域色の強いものを避ける。
4. **敬称。** 遠野家は台詞の中で「-san」を残す（Ryosuke-san, Chizuru-san）。
   姓で呼ぶ相手は señor／señora（*señor Kamiya*, *señora Tachibana*, *señora Sagara*）。
5. **tú／usted。** 夫婦、兄妹、克巳から千鶴、宗一郎から子どもたちは tú。それ以外は usted。
6. **台詞は « » で括る。** スペイン語の小説はダッシュ（raya）で台詞を始めることが多いが、
   ほかの版と同じく « » にそろえた（スペイン語の出版物でも使われる形）。
   疑問文・感嘆文は必ず ¿ ¡ で始める（`check_es.py` で漏れを検査する）。
7. **法律用語に脚注をつけない。** 台詞の中で一度だけ説明する。
8. **文体。** 短い平叙文。感情の形容詞を使わない。段落は短く。`※` の区切りはそのまま。
9. **数字。** 台詞と地の文の金額は語で書く（*veintiocho millones de yenes*）。
   帳票は `72.043.518`、`1.480 ¥`。日付は `10 de febrero de 2026`、時刻は `18:40`。

## 数字の対比（ほかの版と同じ置き換え）

| | 日本語版 | スペイン語版 |
|---|---|---|
| 歴代の行 | 昭和十六年十二月 | *Showa 16, duodécimo mes* |
| 〃 | 平成三年 | *Heisei 3* |
| 宗一郎の行 | 2026年2月10日 | **10 de febrero de 2026** |

## 固有名詞

| 日本語 | Español |
|---|---|
| 遠野精工 | Tono Precisión |
| 遠野建装 | Construcciones Tono |
| 上州あかぎ銀行 宇賀野支店 | Banco Joshu-Akagi, sucursal de Ugano |
| 群馬中央信用金庫 | Cooperativa de Crédito Gunma Chuo |
| 北関東証券 | Kita-Kanto Securities |
| 白鷺開発 | Shirasagi Development |
| 梶原FPオフィス | Kajiwara Asesoría Patrimonial |
| 前田不動産 | Inmobiliaria Maeda |
| 宇賀野中央法律事務所 | Bufete Ugano Chuo |
| 北関東データセンター構想 | el proyecto del centro de datos de Kanto Norte |
| ホームセンター栄和 | tienda de bricolaje Eiwa |
| リョウ・クリエイト / 〈Arclight Capital〉 / 〈TAKA〉 | Ryo Create / Arclight Capital / TAKA |

人名・地名は英語版と同じ（`TRANSLATION.md`）。

## 法律・金融の語

| 日本語 | Español |
|---|---|
| 公正証書遺言 | testamento notarial |
| 遺言執行者 | albacea |
| 遺留分 | la legítima（スペイン・中南米の民法にもある概念なので、そのまま通じる） |
| 付言事項 | la nota personal（「法的効力はない」と第26章で説明される） |
| 四十九日 | el cuadragésimo noveno día（第9章で「ceremonia budista」と一度添える） |
| 月命日 | el día de conmemoración mensual |
| 信託 / 受託者 / 受益権 | fideicomiso / fiduciario / derecho de beneficiario |
| 連帯保証（人） | aval solidario / avalista solidario(a) |
| 稟議（書） | expediente de crédito |
| 試算表 / 粉飾 | balance provisional / contabilidad maquillada |
| 倍率地域 | zona de coeficiente（橘の台詞で一行説明） |
| 実印 / 印鑑証明 | sello registrado / certificado de registro del sello |
| 公証役場 | la notaría |
| 任意同行 | declarar de forma voluntaria |
| 公訴の取り消し | retirada de la acusación |

## 繰り返される言い回し

| 日本語 | Español |
|---|---|
| すべてを一つに賭けた者には、一円も残すな | **A quien lo haya apostado todo a una sola cosa, que no le quede ni un yen.** |
| 毎月、決まった額を、決まった日に／それだけ？／それだけです | **Cada mes, la misma cantidad, el mismo día.** / *¿Nada más?* / *Nada más.* |
| 私は、何もしていません。／何もしなかっただけです。 | **Yo no hice nada.** / **Solo dejé que pasara.** |
| 2026年2月10日　三つに分けた　もう一つ　分けられなかったものがある | **10 de febrero de 2026　lo dividí en tres　queda una　que no pude dividir** |
| 階段から落ちて死んだのなら、それは事故ではありません | **Si he muerto al caer por la escalera, no fue un accidente.** |
| 片づける人のやり方です | **Así es como lo hace alguien que guarda las cosas.** |
| 金を失ったことのある人間にしか、金の見張りは頼めない | **Solo a quien ya ha perdido dinero se le puede encargar que vigile el dinero.** |
| 間に合わなかったんですか | **Entonces, ¿llegué tarde?** |
| いちばん重いものを持とうとする | **Siempre quiere cargar con lo más pesado.** |
| もういいんです | **Ya no hace falta.** |
| 三つの籠 | las tres cestas |

## 帳簿の七つの記号

漢字を出し、地の文で意味を添える。土 tierra ／ 種 semilla ／ 木 árbol ／ 蜜 miel ／ 鍵 llave ／ 手 mano ／ 水 agua

## タイトル

- シリーズ: **El último libro de cuentas**
- 第1巻: **El último libro de cuentas: Una herencia en tres partes**

## 章題（スペイン語版）

| | 日本語 | Español |
|---|---|---|
| 序 | プロローグ | Prólogo |
| 1 | 誘導灯 | El bastón luminoso |
| 2 | 消印 | El matasellos |
| 3 | 11日 | El día once |
| 4 | 三つの籠 | Las tres cestas |
| 5 | 1996年 | 1996 |
| 6 | 杭 | Las estacas |
| 7 | 番頭 | El administrador |
| 8 | 差額 | La diferencia |
| 9 | 封をする紙 | El papel sellado |
| 10 | 勝ち組の側 | Del lado de los ganadores |
| 11 | 三つの値段 | Tres precios |
| 12 | 四つの穴 | Cuatro agujeros |
| 13 | 2月5日 | El 5 de febrero |
| 14 | 三分の一 | Un tercio |
| 15 | 相良 | Sagara |
| 16 | 四回目 | La cuarta vez |
| 17 | 任意 | Declaración voluntaria |
| 18 | 一回だけ | Una sola vez |
| 19 | 名簿 | La lista |
| 20 | もういいんです | Ya no hace falta |
| 21 | 立てかけてあった | Apoyada contra la pared |
| 22 | 三つ | Tres |
| 23 | 何もしなかった | Yo no hice nada |
| 24 | 2月10日 | El 10 de febrero |
| 25 | 連絡先 | Persona de contacto |
| 26 | 四通目 | El cuarto sobre |
| 27 | 定期 | Depósito a plazo |
| 終 | エピローグ | Epílogo |

章題はスペイン語の慣例どおり、最初の語と固有名詞だけを大文字にした。
第21章 *Apoyada contra la pared* は「手すり（la barandilla、女性名詞）」を受けている。
第27章「定期」は *Depósito a plazo*（ほかの版と同じ判断）。

訳しているあいだに、日本語原文の新しい傷は見つからなかった。

