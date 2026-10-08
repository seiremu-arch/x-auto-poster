# ポルトガル語（ブラジル）版の方針と対訳表

『最後の帳簿　三つに分けられた遺産』のポルトガル語訳。`manuscript/`（日本語）が原本、
`manuscript-pt/` が訳文。**底本は日本語原文。** ほかの版（英・独・仏・西・伊・蘭）は、
固有名詞と言い回しの決め方をそろえるための参照にだけ使う。

## 基本方針

1. **ブラジルのポルトガル語で訳す。** ポルトガル本国には Amazon のストアがなく、
   ポルトガル語の電子書籍の主な市場は Amazon.com.br。語彙・つづり・語順はブラジルの標準に合わせる。
2. **舞台は日本のまま。** 円は *iene*（複数形 *ienes*）、法制度は日本の法制度。
3. **人名は名→姓**（Shuji Kamiya）。ほかの版と同じ。
4. **敬称。** 遠野家は台詞の中で「-san」を残す（Ryosuke-san, Chizuru-san, Katsumi-san）。
   日本の作品の敬称はブラジルの読者になじみがある。姓で呼ぶ相手は *senhor*／*senhora*、
   弁護士の橘は *doutora Tachibana*（ブラジルで弁護士を呼ぶ慣例）。
5. **você／o senhor。** 夫婦、兄妹、克巳から千鶴、宗一郎から子どもたちは você。それ以外は o senhor／a senhora。
   亮介が神谷を「あんた」と呼ぶ場面だけ você に落として、無礼さを出す。
6. **台詞はダッシュ（—）で始める。** ブラジルの小説で一般的な形。地の文の受けは
   `— Só isso — disse ele.` の形。入れ子の引用は “ ”。
   神谷の頭の中で反復される帳簿や手紙の一行は、台詞と混ざらないよう斜体にする。
   ダッシュの後の空白と “ ” の対応は `check_pt.py` で検査する。
7. **法律用語に脚注をつけない。** 台詞の中で一度だけ説明する。
8. **文体。** 短い平叙文。感情の形容詞を使わない。段落は短く。`※` の区切りはそのまま。
9. **数字。** 台詞と地の文の金額は語で書く（*vinte e oito milhões de ienes*）。
   帳票は `72.043.518`、`¥ 1.480`、一覧は `21,4 mi`。日付は `10 de fevereiro de 2026`、
   短い日付は日／月（`8/2`）、時刻は `18h40`。
   階数はブラジル式（地上階が *térreo*。日本の2階 = *primeiro andar*、3階 = *segundo andar*）。

## 数字の対比（ほかの版と同じ置き換え）

| | 日本語版 | ポルトガル語版 |
|---|---|---|
| 歴代の行 | 昭和十六年十二月 | *Showa 16, décimo segundo mês* |
| 〃 | 平成三年 | *Heisei 3* |
| 宗一郎の行 | 2026年2月10日 | **10 de fevereiro de 2026** |

## 固有名詞

| 日本語 | Português |
|---|---|
| 本家 | a casa da família |
| 遠野精工（株式会社） | Tono Precisão (Ltda.) |
| 遠野建装 | Construtora Tono |
| 上州あかぎ銀行 宇賀野支店 | Banco Joshu Akagi, agência de Ugano |
| 群馬中央信用金庫 | Cooperativa de Crédito Gunma Chuo |
| 北関東証券 | Kita-Kanto Securities |
| 白鷺開発 | Shirasagi Development (S.A.) |
| 梶原FPオフィス | Kajiwara Planejamento Financeiro |
| 前田不動産 | Imobiliária Maeda |
| 宇賀野中央法律事務所 | Escritório de Advocacia Ugano Chuo |
| 北関東データセンター構想 | o projeto do data center do Norte de Kanto |
| ホームセンター栄和 | Home Center Eiwa（loja de material de construção） |
| リョウ・クリエイト / 〈Arclight Capital〉 / 〈TAKA〉 | Ryo Create Ltda. / Arclight Capital / TAKA |
| 東京 | Tóquio |

人名・地名は英語版と同じ（`TRANSLATION.md`）。

## 法律・金融の語

| 日本語 | Português |
|---|---|
| 公正証書遺言 | testamento público（ブラジル民法にも同名の方式がある。traslado = 正本） |
| 公証人 / 公証役場 | tabelião / cartório |
| 遺言執行者 | testamenteiro（ブラジル民法の語） |
| 遺留分 | a legítima（ブラジル民法にもある概念） |
| 付言事項 | a nota pessoal（「法的効力はない」と第26章で説明される） |
| 遺贈 | legado |
| 四十九日 | o quadragésimo nono dia |
| 月命日 | o dia de memória mensal |
| 信託 / 受託者 / 受益権 | trust / banco fiduciário / direito de beneficiário |
| 連帯保証（人） | fiança solidária / fiador(a) solidário(a) |
| 稟議（書） | proposta de crédito |
| 試算表 / 粉飾 | balancete / números maquiados |
| 固定資産評価証明書 | certidão de valor venal |
| 路線価 / 倍率地域 | valor de referência da via / zona de coeficiente（橘の台詞で一行説明） |
| 延納 | parcelamento, parcelas anuais |
| 実印 / 印鑑証明 | selo registrado / certificado de registro do selo |
| 登記事項証明書 | certidão de matrícula |
| 任意同行 | comparecer voluntariamente à delegacia |
| 公訴の取り消し | a denúncia foi retirada |
| 鍵の受け渡し簿 | o caderno das chaves（表紙は *Chaves*） |

## 繰り返される言い回し

| 日本語 | Português |
|---|---|
| すべてを一つに賭けた者には、一円も残すな | **A quem apostou tudo numa coisa só, não deixem nem um iene.** |
| 毎月、決まった額を、決まった日に／それだけ？／それだけです | **Todo mês, o mesmo valor, no mesmo dia.** / *Só isso?* / *Só isso.* |
| 私は、何もしていません。／何もしなかっただけです。 | **Eu não fiz nada.** / **Só deixei acontecer.** |
| 2026年2月10日　三つに分けた　もう一つ　分けられなかったものがある | **10 de fevereiro de 2026　dividi em três　resta uma　que não consegui dividir** |
| 階段から落ちて死んだのなら、それは事故ではありません | **Se morri caindo da escada, não foi um acidente.** |
| 片づける人のやり方です | **É assim que faz quem guarda as coisas.** |
| 金を失ったことのある人間にしか、金の見張りは頼めない | **Só a quem já perdeu dinheiro se pode pedir que vigie dinheiro.** |
| 金を守れた人間には…／守れなかった人間だけが、どこで手が滑るかを知っている | *A quem soube guardar o próprio dinheiro, não se pode pedir que vigie dinheiro.* / *Só quem não soube guardar sabe onde a mão escorrega.* |
| 間に合わなかったんですか | **Então eu cheguei tarde?** |
| いちばん重いものを持とうとする | **quer carregar o peso maior** |
| もういいんです | **Não precisa mais.** |
| 三つの籠 | os três cestos |
| 土地／事業／現金（封筒に書く三つ） | **Terreno / Empresa / Dinheiro** |

付言事項は、ブラジルの慣用句「すべての卵を一つの籠に入れる」（*pôr todos os ovos numa só cesta*）も考えたが、
第4章で亮介が「俺が博打打ちみたいに書いてある」と受けるので、賭けの語 *apostar* を残した。

## 帳簿の七つの記号

漢字を出し、地の文で意味を添える。土 terra ／ 種 semente ／ 木 árvore ／ 蜜 mel ／ 鍵 chave ／ 手 mão ／ 水 água

## タイトル

- シリーズ: **O último livro-caixa**
- 第1巻: **O último livro-caixa: Uma herança em três partes**

## 章題

| 章 | 原題 | ポルトガル語 |
| --- | --- | --- |
| 序 | プロローグ | Prólogo |
| 1 | 誘導灯 | O bastão luminoso |
| 2 | 消印 | O carimbo postal |
| 3 | 11日 | O dia onze |
| 4 | 三つの籠 | Os três cestos |
| 5 | 1996年 | 1996 |
| 6 | 杭 | As estacas |
| 7 | 番頭 | O braço direito |
| 8 | 差額 | A diferença |
| 9 | 封をする紙 | O papel lacrado |
| 10 | 勝ち組の側 | Do lado dos vencedores |
| 11 | 三つの値段 | Três preços |
| 12 | 四つの穴 | Quatro furos |
| 13 | 2月5日 | 5 de fevereiro |
| 14 | 三分の一 | Um terço |
| 15 | 相良 | Sagara |
| 16 | 四回目 | A quarta vez |
| 17 | 任意 | Voluntariamente |
| 18 | 一回だけ | Só uma vez |
| 19 | 名簿 | A lista |
| 20 | もういいんです | Não precisa mais |
| 21 | 立てかけてあった | Encostado na parede |
| 22 | 三つ | Três |
| 23 | 何もしなかった | Eu não fiz nada |
| 24 | 2月10日 | 10 de fevereiro |
| 25 | 連絡先 | Pessoa de contato |
| 26 | 四通目 | O quarto envelope |
| 27 | 定期 | Depósito a prazo |
| 終 | エピローグ | Epílogo |

章題はポルトガル語の慣例どおり、最初の語と固有名詞だけを大文字にした。
第7章「番頭」は、社長の右腕として帳場を預かる人という意味で *O braço direito*。
第21章 *Encostado na parede* は「手すり（o corrimão、男性名詞）」を受けている。
第23章は千鶴の最後の台詞から *Eu não fiz nada* とし、続く「何もしなかっただけです」は
*Só deixei acontecer.*（起きるのに任せただけ）と訳した（伊・蘭語版と同じ判断）。
第27章「定期」は *Depósito a prazo*（神谷の嘘「定期に入れてある」と同じ語）。

訳しているあいだに、日本語原文の新しい傷は見つからなかった。
