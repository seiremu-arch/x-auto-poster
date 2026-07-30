# KDP出版・SNS運用 サブエージェントチーム

Kazu A. Suzuki（Boundary Japan）の個人開発チーム基盤。Claude Codeのサブエージェント機能を使い、
KDP出版パイプラインとSNS運用を7ロールで自律的に回す。

## 体制図

```
人間（著者 / EM）
│
└── /run-project（メインセッション = オーケストレーター）
     │
     ├── product-manager (Opus)         … 企画統括・振り分け
     │
     ├── KDP出版ライン
     │    ├── story-editor (Opus)        … プロット・引き設計
     │    ├── localization-lead (Opus)   … 多言語ローカライズ統括
     │    ├── kdp-production (Sonnet)    … docx整形・メタデータ
     │    └── proofreader-qa (Sonnet)    … 独立校正・検証
     │
     └── SNS運用ライン
          ├── content-planner (Opus)     … 投稿企画・スケジュール
          └── copywriter (Sonnet)        … 媒体別原稿作成
```

判断・設計系はOpus、実行系（Production / QA / Copywriter）はSonnetでコスト効率を取る。

サブエージェントは互いに直接対話できない。**Product Managerが「頭脳」**（どのロールを・どの順で・
何を入力に動かすかの計画を出力）、**メインセッションが「手足」**（Taskツールで各ロールを順次起動）、
**受け渡しはすべてファイルベース**という設計は元記事の構成を踏襲している。

## ワークスペース構造

```
.claude/documents/projects/{yyyy-mm-dd}_{slug}/
├── 00_request.md          # 人間の依頼（原文）
├── 10_product_brief.md    # Product Manager
├── 20_story_plan.md       # Story Editor（KDPラインのみ）
├── 30_localization_plan.md# Localization Lead（KDPライン・多言語対応時のみ）
├── 50_kdp_package.md      # KDP Production（KDPラインのみ）
├── 60_qa_report.md        # Proofreader/QA（KDPラインのみ）
├── 70_content_calendar.md # Content Planner（SNSラインのみ）
├── 80_content_drafts.md   # Copywriter（SNSラインのみ）
└── 90_completion.md       # Product Manager（完了報告）
```

番号はパイプライン順序。KDP出版のみなら 00→10→20→30→50→60→90、SNS運用のみなら
00→10→70→80→90、両方を連携させる場合（新刊リリース連動のSNS施策など）は10を共有し、
20〜60と70〜80を並行して走らせ90で合流する。

小規模な修正（誤字修正など）は 00→50→60→90 のように短縮可能。

## 人間ゲートとエスカレーション

| タイミング       | 内容                                   |
| ----------- | -------------------------------------- |
| ゲート1（計画承認） | スコープ・見積り・リスクの承認後に着手     |
| ゲート2（完了承認） | 完了報告の確認。git commit/push・SNS投稿の実行は人間 |
| 随時         | `STATUS: NEEDS_HUMAN_INPUT` で即停止      |

全ロール共通のエスカレーション基準:
- プロダクト戦略・ブランドイメージの判断
- 不可逆な操作（削除・課金・公開・投稿実行）
- 新規有償サービス・クレデンシャルの追加
- 見積り150%超過
- QA/校正の差し戻し2回超過
- ロール間の成果物矛盾

## 既存ガードレールとの関係

既存の `CLAUDE.md`（KDP docxパイプライン規約・執筆のクセチェックリスト等）はそのまま活かし、
このエージェント定義群はその上に載る形にしている。エージェント定義側でgit書き込み禁止や
投稿実行禁止などの制約を緩めることはしない。

## 導入手順

1. このディレクトリの `.claude/agents/` を対象プロジェクトの `.claude/agents/` にコピーする
2. 対象プロジェクトの `CLAUDE.md` に以下のようなエージェント表を追記する:

   ```markdown
   ## サブエージェント構成
   - product-manager: 企画統括（KDP/SNS振り分け）
   - story-editor: プロット・引き設計（KDP）
   - localization-lead: 多言語ローカライズ統括（KDP）
   - kdp-production: docx整形・メタデータ生成（KDP）
   - proofreader-qa: 独立校正・検証（KDP）
   - content-planner: SNS投稿企画・スケジュール（SNS）
   - copywriter: 媒体別原稿作成（SNS）
   ```

3. KDP docxパイプラインの規約（Heading1/TOC/行間/メタデータテンプレート）と、執筆のクセ
   チェックリストは既存の `CLAUDE.md` に定義済みのものをそのまま参照させる（エージェント定義
   内には重複記載していないため、既存ファイルを削除・移動しないこと）

## 今後の調整ポイント

- KDP出版とSNS運用を同時並行させる際、Content Plannerがどのタイミングでproduct_briefを
  参照するかは実運用しながら調整する
- 多言語版のSNS展開（Boundary Japan Radioの対象言語拡大）が進んだ場合、localization-lead
  との連携ルールを追加する余地がある
