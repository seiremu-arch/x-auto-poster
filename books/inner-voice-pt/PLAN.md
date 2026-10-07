# 企画書 — ポルトガル語(ブラジル)版『A voz mais baixa』

日本語版 `books/inner-voice/` の**書き直し**であって、翻訳ではない
(方針と反証条件は Vault `899744d0ff`)。芯・章構成・実践の番号は揃え、場面と例を決め直す。

## 書誌

| 項目 | 内容 |
| --- | --- |
| Título | A voz mais baixa |
| Subtítulo | Sete exercícios para distinguir a sua própria voz do barulho na sua cabeça |
| Autor | Kazu A. Suzuki(他の七言語と同一表記) |
| 言語 | ポルトガル語(ブラジル)。Amazon.com.br |
| 分量 | 14,700 words 前後(日本語版 33,075字 ÷ 実測 2.25字/word。→ Vault `4fc805514a` の追記) |
| 想定価格 | R$ 19,90 前後(登録時に70%の範囲を画面で確かめる) |

## 芯にする一文

> A sua voz mais baixa nunca vai falar mais alto. Só resta baixar o seu próprio volume.

スペイン語・イタリア語版と同じく、`voz mais baixa`(いちばん低い声)と `baixar`(下げる)が響き合う。
八言語のどれかを直すときは八つとも直す(`--check` が一致を見る)。

## 決め直すもの

- **地域: ブラジルのポルトガル語で書く。中立にしない**(→ Vault `1a18342985`)。
  スペイン語版は中立にしたが、ポルトガル語の Kindle ストアは Amazon.com.br だけなので理由が当たらない。
  ポルトガルの語と形(`telemóvel`、`ecrã`、`estar a + 不定詞` など)は `check_style.py` が拾う
- **人称は `você`。** ブラジルの標準。命令形は接続法の形(`Escreva`、`Anote`)になり、直説法(`escreve`)と形が違うので、
  検査で見分けやすい
- **性の一致**は既存の判断に従う。読者側 `0045c354b1`、著者側 `dba7c10f3f`(新しく書く原稿なので、著者の一人称も最初から中立)。
  ポルトガル語はスペイン語・イタリア語と同じく、`estou cansado/a`、`fiquei surpreso/a`、`sozinho/a` で性が出る。
  イタリア語版で、方針だけでは書いている途中に男性形が漏れたので、**検査を第1章から回し、全章のあとで性に絞った読み返しをする**

## 検証すること

claim `dd52672aca` の予測(第5章がプラス、第7章がマイナス)を、イタリア語・オランダ語に続けて三度目に試す。
全章を書いたら結果をあのノートに追記する。

## 日本語版から差し替えるもの

| 章 | 日本語版の場面 | ポルトガル語版の場面 |
| --- | --- | --- |
| 序章 | 眠れない夜に二十行書く | 同じ |
| 1 | 金曜の飲みの誘い「その仕事、辞めたら?」 | jantar de sexta com uma amiga: “Pede demissão, ué.” |
| 2 | 誘いに即答した三日後 | “Tô dentro!” em três segundos no grupo do WhatsApp |
| 3 | 内見した部屋の玄関で肩が上がる | a terceira visita a um apartamento, com o corretor |
| 4 | レンジの二分・信号待ち | o micro-ondas, o semáforo, o elevador |
| 5 | 会議で部長に数字を指摘される | uma reunião de sete pessoas, um número errado |
| 6 | 三年ぶりの分岐点は金曜の夜、誘いを断った | o happy hour de sexta recusado |
| 7 | 三週間目に何も来なくなった | 同じ。止まるのは地下鉄(metrô) |

## 出す前に確かめること

- **タイトルの重複。** Amazon.com.br で “A voz mais baixa” を検索する
- `check_style.py` が0件(命令形・禁止語・地域語・性の一致・引用符・書きかけの言い直し)

## 現在地

- [x] 企画・構成
- [x] Prólogo
- [x] Capítulo 1 Quantas vozes estão falando
- [x] Capítulo 2 Distinguir pela velocidade
- [x] Capítulo 3 Distinguir no corpo
- [x] Capítulo 4 Fazer espaço
- [x] Capítulo 5 Escrever para ouvir
- [x] Capítulo 6 Decidir pequeno
- [x] Capítulo 7 Os dias em que você não ouve nada
- [x] Encerramento / Apêndice(全10章 14,875 words、目安の101%)
- [x] 検査 `check_style.py` 0件 / EPUB / 表紙 / 登録シート(`LISTING.md`)
- [x] 性に絞った読み返し(性の出うる語の型を抜き出して一件ずつ見た。範囲と見ていないものは Vault `81fc698ea9` の追記)
- [ ] 章をまたいだ通しの推敲(文章全体の読み返し)
- [ ] KDP登録(手作業。DRM と KDP Select は要判断)
