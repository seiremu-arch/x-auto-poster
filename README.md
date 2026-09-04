# x-auto-poster / 分岐点ニュース

RSSフィードから直近のニュースを集め、「事実」と「意見」に分けて毎朝自動更新する静的サイトです。GitHub Actions が毎日決まった時刻にニュースを取得し、`docs/index.html` を再生成して GitHub Pages で公開します。

## 仕組み

1. `.github/workflows/daily-update.yml` が毎日 06:00 JST(21:00 UTC)に実行される
2. `scripts/generate_site.py` が `config/feeds.json` に登録されたRSSフィードを取得
3. フィードごとに設定された `category`(`fact`=事実 / `opinion`=意見)に振り分けて `docs/index.html` を生成
4. 変更があれば自動でコミット・プッシュ
5. GitHub Pages(`main` ブランチの `/docs`)が更新後のページを配信

手動で今すぐ更新したい場合は、GitHub の Actions タブから `Daily News Update` ワークフローを `Run workflow` で実行できます。

## 初回セットアップ(手動で1回だけ必要)

GitHub Pages の公開設定は git push だけでは有効化されないため、リポジトリの管理者が以下を一度だけ行ってください。

1. GitHub のリポジトリ → **Settings** → **Pages**
2. **Source** を `Deploy from a branch` に設定
3. Branch を `main` / フォルダを `/docs` に設定して **Save**

これで `https://<owner>.github.io/x-auto-poster/` でサイトが公開されます。

> 補足: GitHub の `schedule` トリガーは既定ブランチ(通常 `main`)にマージされたワークフローのみ実行されます。このブランチが `main` にマージされるまで、自動実行はされません(`workflow_dispatch` による手動実行は可能)。

## フィードの追加・変更

`config/feeds.json` を編集してください。

```json
{
  "name": "表示名",
  "url": "https://example.com/rss.xml",
  "category": "fact"  // または "opinion"
}
```

- `fact`: 速報・事実報道系のフィード
- `opinion`: コラム・論評・分析系のフィード

分類はフィード単位の簡易的なヒューリスティックであり、記事単位で厳密に事実/意見を判定しているわけではありません。ニュースサイトはRSS配信を予告なく変更・終了することがあるため、フィードが取得できなくなった場合はこのファイルを更新してください(取得に失敗したフィードはページ下部の「取得できなかったフィード」に表示されます)。

## Vault(Loop Engineering)

ニュースの取り込みは、`docs/index.html` を作り直すだけでなく `vault/` にも落ちます。
Vault自体が状態を持ち、ループを回すたびに育っていく設計です。詳細は
[`LOOP-ENGINEERING.md`](LOOP-ENGINEERING.md) と [`vault/README.md`](vault/README.md) を参照してください。

```bash
python scripts/loop.py capture               # RSSから vault/00-inbox へ(重複は自動でスキップ)
python scripts/loop.py capture --note "..."  # 思いつきを vault/00-inbox へ
python scripts/loop.py context <id>          # リンク・タグ・近くのノートを集める
python scripts/loop.py promote <id>          # vault/10-notes に原子ノートを作る
python scripts/loop.py archive               # 30日以上滞留したinboxノートを畳む
python scripts/loop.py review                # スキーマとエッジを検証(CIと同じ)
python scripts/loop.py status                # Vaultの現在地
```

`Daily News Update` ワークフローが毎朝 `capture` → `review` → サイト生成の順に実行し、
`docs/index.html` と `vault/` の変更をまとめてコミットします。Vaultへの変更は
`Vault Review` ワークフローが検証します(スキーマ違反とエッジのリンク切れはCIで落ちます)。

## ローカルでの実行

```bash
pip install -r requirements.txt
python scripts/generate_site.py
```

`docs/index.html` が生成されます。Vault側だけを検証したいときは `python scripts/loop.py review` を実行してください。
