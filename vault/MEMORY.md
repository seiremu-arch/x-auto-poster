# MEMORY — ループをまたいで持ち越す状態

ここは短く保つ。詳細は各ノートに置き、ここにはIDと一行の要約だけを書く。
ループの最初にここを読み、最後にここへ追記する。

## 関心テーマ

<!-- 今このVaultが追いかけているテーマ。増やしすぎない(目安5つまで)。 -->

- (ニュース側は未設定) `loop.py capture` を数日回してから、繰り返し出てくるテーマをここに書く
- KDP出版 — 内省ワーク型の作品『いちばん小さい声』。芯は「内なる声は大きくならない。
  だから、こちらが静かになるしかない」(→ `0adde001a2`。基準は `6e9d28f8ea` / `100f1d5f68`)
- KDP出版(他言語版) — 翻訳ではなく書き直し(→ `899744d0ff`。`fcfb3b0ebf` を一般化したもの)。
  英語版 `The Quietest Voice` の芯は
  「Your quietest voice never gets louder. So the only way to hear it is to get quieter yourself」。
  ドイツ語版 `Die leiseste Stimme` の芯は
  「Deine leiseste Stimme wird nicht lauter. Also bleibt nur, selbst leiser zu werden」(du で書く → `7586251f89`)。
  フランス語版 `La voix la plus basse` の芯は
  「Votre voix la plus basse ne parlera jamais plus fort. Il ne reste donc qu'à faire silence de votre côté」
  (vous で書く → `e778004e3b`)。
  スペイン語版 `La voz más baja` の芯は
  「Tu voz más baja nunca hablará más fuerte. Solo queda bajar tu propio volumen」
  (中立スペイン語 → `cb294d65c0`。読者の性を決めない → `0045c354b1`、著者の性は著者が決める → `dba7c10f3f`)。
  イタリア語版 `La voce più bassa` の芯は
  「La tua voce più bassa non parlerà mai più forte. Non resta che abbassare il tuo volume」

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
- 2026-09-30 20:21 `capture(manual)` — 新規 1 / 重複 0 / 失敗 0 (`vault/40-runs/2026-09-30-run-5802c88646.md`)
<!-- /loop:last-run -->
