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

## 現在の作品

- `inner-voice/` — 『いちばん小さい声』(内省ワーク型 / 4万字前後 / 執筆中)
