# books — KDPに出す作品

このディレクトリは**原稿と体裁**を持つ。Vaultとの分担、`books/` に書いてよい「なぜ」の
範囲、破れたと判断する条件は、Vaultのclaimノート `3f64e5ecd8` にある。ここには写さない。

    python scripts/loop.py context 3f64e5ecd8

## レイアウト

```
books/<slug>/
  book.json            メタデータと章の順序(ビルドの入力)
  PLAN.md              企画書(誰に / 何を約束するか / やらないこと / KDP設定)
  OUTLINE.md           全章のアウトライン(章ごとの主張・実践・字数の目安)
  STYLE.md             文体ルール(使う語・使わない語・表記)
  manuscript/*.md      原稿。1ファイル=1章。ファイル名の数字が並び順
  build/               生成物(gitignore)
```

## 作業の順番

```bash
python scripts/build_book.py inner-voice            # 字数を数える(章ごと / 合計)
python scripts/build_book.py inner-voice --markdown # build/<slug>.md に1本化
python scripts/build_book.py inner-voice --epub     # build/<slug>.epub(KDPにアップロードする形)
python scripts/build_book.py inner-voice --check    # 芯の一文が3か所で一致しているか
```

章を1つ書き終えるたびに字数を見る。`book.json` の `target_chars` に対して各章が
どれだけ膨らんだ / 痩せたかが分かる。

`--check` は、`book.json` の `core_sentence`(その本の芯の一文)が `PLAN.md` ・
`core_claim` が指すVaultのclaimノート・ `vault/MEMORY.md` の3か所に同じ文で現れるかを見る。
片方だけ書き換えると落ちる。`Vault Review` ワークフローが同じチェックを実行する。

## 表紙

文字だけで組む(画像生成はしない)。五言語で同じデザインにして、文字だけ差し替える。

```bash
pip install pillow                                  # 初回だけ
python scripts/build_cover.py --fetch-fonts         # 初回だけ。npm から Noto Serif / Noto Serif JP(OFL-1.1)
python scripts/build_cover.py --all --sheet /tmp/sheet.png   # 全言語 + 縦200pxの縮小版を並べた確認用
```

フォントはリポジトリに入れず `books/.fonts/`(gitignore)に置く。タイトルの改行が不自然なときは
`book.json` の `cover.title_lines` で固定する(フランス語版は「La voix / la plus basse」に固定している)。

## 同じ本の他言語版

言語ごとに別のディレクトリを持つ(KDPも言語ごとに別のタイトルとして登録する)。
翻訳ではなく**書き直し**で、芯の一文・章構成・実践の番号だけを揃える
(→ Vault `899744d0ff`)。

```bash
python scripts/build_book.py inner-voice-en --check   # 英語以外は語数で数える
python books/inner-voice-de/check_style.py            # ドイツ語版の文体検査
python books/inner-voice-fr/check_style.py --fix      # フランス語版の文体検査と不可分空白
python books/inner-voice-es/check_style.py            # スペイン語版の文体検査(地域語・性の一致・¿¡ も)
```

## 現在の作品

- `inner-voice/` — 『いちばん小さい声』(内省ワーク型 / 33,075字 / 原稿完成・表紙待ち)
- `inner-voice-en/` — 『The Quietest Voice』(`inner-voice` の英語での書き直し / 執筆済み)
- `inner-voice-de/` — 『Die leiseste Stimme』(`inner-voice` のドイツ語での書き直し / 執筆済み)
- `inner-voice-fr/` — 『La voix la plus basse』(`inner-voice` のフランス語での書き直し / 執筆済み)
- `inner-voice-es/` — 『La voz más baja』(`inner-voice` のスペイン語での書き直し / 執筆済み)
