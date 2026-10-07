# MEMORY — ループをまたいで持ち越す状態

ここは短く保つ。詳細は各ノートに置き、ここにはIDと一行の要約だけを書く。
ループの最初にここを読み、最後にここへ追記する。

## 関心テーマ

<!-- 今このVaultが追いかけているテーマ。増やしすぎない(目安5つまで)。 -->

- (ニュース側は未設定) `loop.py capture` を数日回してから、繰り返し出てくるテーマをここに書く
  → 2026-10-06: 30日以上回したが、昇格したニュースは0件(59件を archived)。昇格させる先のテーマが無いので、
  ニュースのキャプチャは期限が来たら畳むのが今の運用。テーマを決めるのは人の判断として残す
- KDP出版 — 内省ワーク型の作品『いちばん小さい声』。芯は「内なる声は大きくならない。
  だから、こちらが静かになるしかない」(→ `0adde001a2`。基準は `6e9d28f8ea` / `100f1d5f68`)
- KDP出版(他言語版) — 翻訳ではなく書き直し(→ `899744d0ff`。`fcfb3b0ebf` を一般化したもの)。
  英語版 `The Quietest Voice` の芯は
  「Your quietest voice never gets louder. So the only way to hear it is to get quieter yourself」。
  (英語版の題は 2026-10-06 に `Your Quietest Voice` に変えた。同名のスリラーが Amazon.com にあるため → `15227c1bed`)
  ドイツ語版 `Die leiseste Stimme` の芯は
  「Deine leiseste Stimme wird nicht lauter. Also bleibt nur, selbst leiser zu werden」(du で書く → `7586251f89`)。
  フランス語版 `La voix la plus basse` の芯は
  「Votre voix la plus basse ne parlera jamais plus fort. Il ne reste donc qu'à faire silence de votre côté」
  (vous で書く → `e778004e3b`)。
  (フランス語版の著者の一人称は 2026-10-06 に中立と決まり、書き換えた → `dba7c10f3f`)
  (ただし性に絞った通しの読み返しは未完了。1回目の書き換えで3か所を取りこぼした → `dba7c10f3f` その2)
  (→ 同日に読み返しを実施。著者側1か所・読者側と総称の4か所を追加で直した → `dba7c10f3f` その3)
  (数の訂正と、複数の総称代名詞 certains / d'autres を残す判断 → `dba7c10f3f` その4)
  スペイン語版 `La voz más baja` の芯は
  「Tu voz más baja nunca hablará más fuerte. Solo queda bajar tu propio volumen」
  (中立スペイン語 → `cb294d65c0`。読者の性を決めない → `0045c354b1`、著者の性は著者が決める → `dba7c10f3f`)。
  イタリア語版 `La voce più bassa` の芯は
  「La tua voce più bassa non parlerà mai più forte. Non resta che abbassare il tuo volume」
  オランダ語版 `De zachtste stem` の芯は
  「Je zachtste stem wordt nooit luider. Er zit niets anders op dan zelf stiller te worden」
  ポルトガル語(ブラジル)版 `A voz mais baixa` の芯は
  「A sua voz mais baixa nunca vai falar mais alto. Só resta baixar o seu próprio volume」
  (ブラジルのポルトガル語で書く → `1a18342985`)

## 運用ルール

- 取り込みは1日1回、`Daily News Update` ワークフローから自動で行う
- `00-inbox/` に30日以上滞留したノートは、昇格するか `status: archived` にする
- 既存ノートの本文は書き換えない。追記するか、新しいノートを作って `supersedes` で指す
- ノートやエッジを足したら `python scripts/loop.py canvas` で `vault/graph.canvas` を作り直す
  (図は生成物。手で編集しない)
- Obsidianで開くときのvaultルートは `vault/`。見え方に状態を持たせない(→ `93c76df0c8`)
- `.canvas` / `.base` の構文は外部スキル `kepano/obsidian-skills` に従い、
  このリポジトリに写さない(→ `87803aefac`)。使うのは5つのうち3つだけ(→ `025bed47a9`)
- KDP作品の原稿は `books/<slug>/` に置き、判断だけをVaultに置く(→ `3f64e5ecd8`)。
  章を書いたら `python scripts/build_book.py <slug>` で字数を見る

## 未解決の問い

<!-- 次のループで扱いたい問い。解けたら claim ノートにして、ここから消さずに「→ <id>」を追記する。 -->

- 「事実」と「意見」のフィード単位の分類を、記事単位の claim に落とせるか

## 直近のラン

<!-- loop:last-run -->
- 2026-10-08 08:21 `capture(manual)` — 新規 1 / 重複 0 / 失敗 0 (`vault/40-runs/2026-10-08-run-475055b4c2.md`)
<!-- /loop:last-run -->
