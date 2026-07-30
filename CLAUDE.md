# CLAUDE.md

## このリポジトリについて

`x-auto-poster` / 分岐点ニュース。RSSフィードからニュースを集め、「事実」と「意見」に分けて
毎朝自動更新する静的サイト。詳細は `README.md` を参照。

- `scripts/generate_site.py` … サイト生成スクリプト（`docs/index.html` を出力）
- `config/feeds.json` … 取得対象フィード定義（`category` は `fact` / `opinion`）
- `.github/workflows/daily-update.yml` … 毎日 06:00 JST の自動更新
- `docs/` … GitHub Pages の公開ディレクトリ。**生成物のため直接編集しない**

## サブエージェント構成

KDP出版・SNS運用のサブエージェントチーム（定義は `.claude/agents/`、全体設計は
`.claude/agents-team-README.md`）。

- product-manager: 企画統括（KDP/SNS振り分け）
- story-editor: プロット・引き設計（KDP）
- localization-lead: 多言語ローカライズ統括（KDP）
- kdp-production: docx整形・メタデータ生成（KDP）
- proofreader-qa: 独立校正・検証（KDP）
- content-planner: SNS投稿企画・スケジュール（SNS）
- copywriter: 媒体別原稿作成（SNS）

判断・設計系はOpus、実行系（kdp-production / proofreader-qa / copywriter）はSonnet。

### オーケストレーション

サブエージェント同士は直接対話できない。product-manager が「頭脳」（どのロールを・どの順で・
何を入力に動かすかの計画を出力）、メインセッションが「手足」（Taskツールで各ロールを順次起動）、
受け渡しはすべてファイルベース。

ワークスペース: `.claude/documents/projects/{yyyy-mm-dd}_{slug}/`

| ファイル                   | 担当              |
| ---------------------- | --------------- |
| `00_request.md`        | 人間の依頼（原文）       |
| `10_product_brief.md`  | product-manager |
| `20_story_plan.md`     | story-editor    |
| `30_localization_plan.md` | localization-lead |
| `50_kdp_package.md`    | kdp-production  |
| `60_qa_report.md`      | proofreader-qa  |
| `70_content_calendar.md` | content-planner |
| `80_content_drafts.md` | copywriter      |
| `90_completion.md`     | product-manager（完了報告） |

番号はパイプライン順序。KDP出版のみなら 00→10→20→30→50→60→90、SNS運用のみなら
00→10→70→80→90。両方を連携させる場合は 10 を共有し、20〜60 と 70〜80 を並行させて 90 で合流する。
小規模な修正（誤字修正など）は 00→50→60→90 に短縮可能。

### 人間ゲート

| タイミング       | 内容                                        |
| ----------- | ----------------------------------------- |
| ゲート1（計画承認） | スコープ・見積り・リスクの承認後に着手                       |
| ゲート2（完了承認） | 完了報告の確認。git commit/push・SNS投稿の実行は人間        |
| 随時          | `STATUS: NEEDS_HUMAN_INPUT` で即停止           |

全ロール共通のエスカレーション基準:

- プロダクト戦略・ブランドイメージの判断
- 不可逆な操作（削除・課金・公開・投稿実行）
- 新規有償サービス・クレデンシャルの追加
- 見積り150%超過
- QA/校正の差し戻し2回超過
- ロール間の成果物矛盾

### 共通の表記規約

- 出版社名: Boundary Japan
- 著者名: Kazu A. Suzuki
- シリーズ名は意図的に広義の名称にする（狭義だと多言語展開が複雑になるため）

KDP docxパイプラインの規約（Heading1 / TOC / 行間1.8倍 / メタデータテンプレート）と文章の
クセチェックリストは、各エージェント定義（`kdp-production.md` / `story-editor.md` /
`proofreader-qa.md`）に記載されている。
