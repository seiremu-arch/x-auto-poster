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

## ローカルでの実行

```bash
pip install -r requirements.txt
python scripts/generate_site.py
```

`docs/index.html` が生成されます。

## Obsidian vault(`vault/`)

`vault/` ディレクトリがそのままObsidianのvaultです。案件ごと・ナレッジごとにノートを分け、`[[ウィキリンク]]` で相互に繋いで貯めていきます。

### 開き方

Obsidianで **「フォルダをvaultとして開く」** から、このリポジトリの `vault/` を選びます。リポジトリごとgit管理されているので、`git pull` すれば他の端末やGitHub Actionsからの更新もそのまま反映されます。

`vault/.obsidian/` の設定(ウィキリンク・テンプレート・有効化するコアプラグイン)は共有していますが、端末ごとに変わる `workspace.json` などは `.gitignore` で除外しています。

### 構成

```
vault/
├── ホーム.md            入口。ここから全ノートをたどる
├── 運用ルール.md         ノートの分け方・リンクの張り方
├── ノート作成スクリプト.md
├── 案件/                案件ごとに1フォルダ + 同名のハブノート
│   └── 分岐点ニュース/
├── ナレッジ/             分野ごとの再利用可能な知識
│   ├── RSS/ GitHub/ 情報設計/ Python/
└── テンプレート/
```

### ノートを作る

```bash
# 案件: vault/案件/<案件名>/<案件名>.md を作り、ホーム.md にリンクを追記
python scripts/new_note.py 案件 "新しい案件名"

# ナレッジ: vault/ナレッジ/<分野>/<トピック名>.md を作る
python scripts/new_note.py ナレッジ "トピック名" --分野 GitHub
```

作成後、関連ノートへのリンクを最低1本張ってください。書き方の詳細は `vault/運用ルール.md` にあります。

### リンクの検査

```bash
python scripts/check_vault_links.py
```

未解決のウィキリンクと、どこからもリンクされていない孤立ノートを報告します(未解決リンクがあれば終了コード1)。
