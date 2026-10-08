# book/ — 入稿用の生成物

ここにあるファイルは**すべて生成物**。本文を直すときは `../manuscript/*.md` を編集し、
下のコマンドで作り直す。

```bash
python3 ../to_kanji.py                 # manuscript/（算用数字）→ ../build/vertical/（漢数字）
python3 ../build_epub.py               # 縦書きEPUB + 統合md
python3 ../build_epub.py --horizontal  # 横書きEPUB + 統合md
python3 ../build_epub.py --english     # 英語版EPUB + 統合md（../manuscript-en/）
python3 ../build_epub.py --german      # ドイツ語版EPUB + 統合md（../manuscript-de/）
python3 ../fr_typo.py && python3 ../build_epub.py --french   # フランス語版EPUB + 統合md（../manuscript-fr/）
python3 ../check_es.py && python3 ../build_epub.py --spanish # スペイン語版EPUB + 統合md（../manuscript-es/）
python3 ../check_it.py && python3 ../build_epub.py --italian # イタリア語版EPUB + 統合md（../manuscript-it/）
python3 ../check_nl.py && python3 ../build_epub.py --dutch   # オランダ語版EPUB + 統合md（../manuscript-nl/）
python3 ../check_pt.py && python3 ../build_epub.py --portuguese # ポルトガル語版EPUB + 統合md（../manuscript-pt/）
```

| ファイル | 中身 |
| --- | --- |
| `KDP-出版情報.md` | タイトル・内容紹介・キーワード・カテゴリ・表紙仕様・チェックリスト |
| `最後の帳簿1_三つに分けられた遺産.epub` | **KDP入稿用**（縦書き・漢数字） |
| `最後の帳簿1_三つに分けられた遺産_横書き.epub` | 横書き・算用数字 |
| `最後の帳簿1_三つに分けられた遺産.md` | 統合原稿（縦書き版） |
| `最後の帳簿1_三つに分けられた遺産_横書き.md` | 統合原稿（横書き版） |
| `KDP-English.md` | 英語版のKDP入力内容（英語の内容紹介・キーワード・カテゴリ・AI開示） |
| `The_Last_Ledger_1_An_Estate_in_Three_Parts.epub` | **英語版のKDP入稿用**（横書き・左開き） |
| `The_Last_Ledger_1_An_Estate_in_Three_Parts.md` | 英語版の統合原稿 |
| `KDP-Deutsch.md` | ドイツ語版のKDP入力内容（内容紹介・キーワード・カテゴリ・AI開示・価格拘束の注意） |
| `Das_letzte_Kassenbuch_1_Ein_Erbe_in_drei_Teilen.epub` | **ドイツ語版のKDP入稿用**（横書き・左開き） |
| `Das_letzte_Kassenbuch_1_Ein_Erbe_in_drei_Teilen.md` | ドイツ語版の統合原稿 |
| `KDP-Francais.md` | フランス語版のKDP入力内容（内容紹介・キーワード・カテゴリ・AI開示・定価制度の注意） |
| `Le_Dernier_Livre_de_comptes_1_Un_heritage_en_trois_parts.epub` | **フランス語版のKDP入稿用**（横書き・左開き） |
| `Le_Dernier_Livre_de_comptes_1_Un_heritage_en_trois_parts.md` | フランス語版の統合原稿 |
| `KDP-Espanol.md` | スペイン語版のKDP入力内容（内容紹介・キーワード・カテゴリ・AI開示・定価制度の注意） |
| `El_ultimo_libro_de_cuentas_1_Una_herencia_en_tres_partes.epub` | **スペイン語版のKDP入稿用**（横書き・左開き） |
| `El_ultimo_libro_de_cuentas_1_Una_herencia_en_tres_partes.md` | スペイン語版の統合原稿 |
| `KDP-Italiano.md` | イタリア語版のKDP入力内容（内容紹介・キーワード・カテゴリ・AI開示・値引き規制の注意） |
| `L_ultimo_libro_dei_conti_1_Un_eredita_in_tre_parti.epub` | **イタリア語版のKDP入稿用**（横書き・左開き） |
| `L_ultimo_libro_dei_conti_1_Un_eredita_in_tre_parti.md` | イタリア語版の統合原稿 |
| `KDP-Nederlands.md` | オランダ語版のKDP入力内容（内容紹介・キーワード・カテゴリ・AI開示・定価制度の注意） |
| `Het_laatste_kasboek_1_Een_erfenis_in_drie_delen.epub` | **オランダ語版のKDP入稿用**（横書き・左開き） |
| `Het_laatste_kasboek_1_Een_erfenis_in_drie_delen.md` | オランダ語版の統合原稿 |
| `KDP-Portugues.md` | ポルトガル語（ブラジル）版のKDP入力内容（内容紹介・キーワード・カテゴリ・AI開示・KDPセレクトの注意） |
| `O_ultimo_livro-caixa_1_Uma_heranca_em_tres_partes.epub` | **ポルトガル語版のKDP入稿用**（横書き・左開き） |
| `O_ultimo_livro-caixa_1_Uma_heranca_em_tres_partes.md` | ポルトガル語版の統合原稿 |

## 数字の扱い

`manuscript/` は**算用数字を正**とする。縦書きでは算用数字が寝てしまうので、
`to_kanji.py` が漢数字に変換したものを `build/vertical/` に書き出し、EPUBはそれを使う。

変換しないもの（意図的に算用数字のまま残すもの）。

- 帳簿の最新の一行 `2026年2月10日　三つに分けた　もう一つ　分けられなかったものがある`
- 測量杭の刻印 `T-4　2026.1.20`
- 紙のサイズ `A4` `B5`、`LED`、`PDF`、`NISA`、`ATM`、`Arclight Capital`

帳票類（通帳、残高明細、財産目録、見積書）は、縦書きでも帳票に見えるよう
`to_kanji.py` の `DOCUMENT_FORMS` で個別に指定している
（例：`72,043,518` → `七二、〇四三、五一八`）。
