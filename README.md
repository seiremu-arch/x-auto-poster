# x-auto-poster

このリポジトリには、独立した2つの自動化があります。

| | 内容 | 詳細 |
| --- | --- | --- |
| **分岐点ニュース** | RSSから毎朝ニュースを集めて静的サイトを自動更新する | この下 |
| **KDP制作パイプライン** | Markdown原稿からKDP入稿用の docx / EPUB を生成する | [`scripts/kdp/README.md`](scripts/kdp/README.md) |

---

# 分岐点ニュース

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

---

# KDP制作パイプライン

Markdownで書いた原稿と `book.yaml` から、KDP(Kindle Direct Publishing)にそのまま入稿できる
docx(電子書籍用・ペーパーバック用)と EPUB3 を生成します。目次の自動生成、改ページ、奥付、
入稿前チェックまでをスクリプトが受け持つので、原稿を直したらビルドし直すだけで入稿ファイルが揃います。

```bash
pip install -r requirements.txt

# 生成(docx 2種 + EPUB + KDP登録用メタデータ)
python scripts/build_book.py manuscripts/sample-book

# 入稿前チェックだけ
python scripts/build_book.py manuscripts/sample-book --check-only --strict
```

出力は `build/<slug>/` に入ります。

| ファイル | 用途 |
| --- | --- |
| `<slug>-ebook.docx` | 電子書籍用(リンク付き目次) |
| `<slug>-print.docx` | ペーパーバック用(判型・見開き余白・ノンブル・目次フィールド) |
| `<slug>.epub` | KDP推奨形式のEPUB3 |
| `<slug>-kdp-metadata.md` | KDPの登録画面にコピペするメタデータ |
| `build-manifest.json` | ビルド結果のサマリ(統計・概算ページ数・警告) |

原稿は `manuscripts/<本の名前>/` に置きます。サンプルとして
[`manuscripts/sample-book/`](manuscripts/sample-book/) が入っており、これ自体が
パイプラインの使い方を説明した1冊の本になっています。

設定項目・原稿の記法・目次の仕組み・入稿手順は
**[`scripts/kdp/README.md`](scripts/kdp/README.md)** にまとめています。

## テスト

```bash
python -m unittest discover -s tests -v
```
