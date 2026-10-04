# Claude Code の道具箱

このリポジトリで使う Claude Code の拡張7つと、その入れ方・使い方。

**先に知っておくこと:どこで効くかは入れ方で決まる。**

| 入れ方 | ローカルの `claude` | クラウド(claude.ai/code・スマホアプリ) |
| --- | --- | --- |
| `.claude/skills/` にコミットしたスキル | 効く | 効く |
| `.mcp.json` のMCPサーバー | 効く | 効く |
| `.claude/settings.json` の `enabledPlugins` | 効く(初回に確認が出る) | **効かない** |

なので、クラウドでも使いたいもの(Remotion / Playwright)はスキル・MCPとしてリポジトリに入れ、
プラグインでしか配られていないもの(Superpowers など)はローカル用として扱う。

| # | 道具 | 用途 | 入れ方 | 状態 |
| --- | --- | --- | --- | --- |
| 1 | Remotion | Reactで動画を自動生成 | `.claude/skills/remotion-best-practices/` | 導入済み |
| 2 | Superpowers | 計画 → サブエージェント実行 → レビューのループ | プラグイン | 要承認(下記) |
| 3 | Playwright | ブラウザ操作・スクショ | `.mcp.json` + `scripts/playwright-mcp.sh` | ラッパー導入済み・`.mcp.json` 要承認 |
| 4 | claude-code-setup | このリポジトリに合う自動化を提案 | プラグイン | 要承認 |
| 5 | frontend-design | 見た目の良いUIを作る | プラグイン | 要承認 |
| 6 | Discord | スマホのDiscordからClaude Codeを操作 | プラグイン(Channels) | 手動セットアップ |
| 7 | skill-creator | スキルを作る・評価する | プラグイン | 要承認 |

2〜7 はすべて公式マーケットプレイス `claude-plugins-official`(最初から登録済み)にある。

---

## 要承認:設定ファイル2つ

Claude Code の自動モードは、自分の設定(`.claude/settings.json` / `.mcp.json`)を
書き換える操作を止める。内容を確認して、問題なければ自分で作るか、Claudeに書き込みを許可する。

`.claude/settings.json`(ローカルでプラグインを有効化):

```json
{
  "enabledPlugins": {
    "superpowers@claude-plugins-official": true,
    "frontend-design@claude-plugins-official": true,
    "skill-creator@claude-plugins-official": true,
    "claude-code-setup@claude-plugins-official": true
  }
}
```

`.mcp.json`(Playwright MCP。ローカルでもクラウドでも読まれる):

```json
{
  "mcpServers": {
    "playwright": {
      "command": "bash",
      "args": ["scripts/playwright-mcp.sh"]
    }
  }
}
```

設定ファイルを使わずに手で入れる場合は、`claude` の中で:

```
/plugin install superpowers@claude-plugins-official
/plugin install frontend-design@claude-plugins-official
/plugin install skill-creator@claude-plugins-official
/plugin install claude-code-setup@claude-plugins-official
```

---

## 1. Remotion — 自動で動画

`npx skills add remotion-dev/skills -a claude-code -s remotion-best-practices --copy` で入れたもの。
`remotion-best-practices` がルーターで、作成・字幕・レンダリングなどの個別スキルを中に持っている。
出どころとハッシュは `skills-lock.json` に記録してある。

```
/remotion-best-practices 今日の docs/index.html の見出しから30秒の縦動画を作って
```

- Remotionのプロジェクト本体(`package.json` など)はまだ無い。最初の依頼でスキルが `npx create-video` から作る。
- 更新:`npx skills update -p`

## 2. Superpowers — 計画・サブエージェント・改善のループ

`brainstorming → writing-plans → subagent-driven-development → requesting-code-review` の順に
スキルが自動で発動する。計画を立て、タスクごとにサブエージェントを走らせ、レビューして直す。

```
/superpowers:brainstorming 毎朝のニュースを動画にしてXに投稿する仕組みを考えたい
```

**このリポジトリでの注意**:CLAUDE.md の「批評は `vault-critic` 1つだけ。エージェントを増やさない」は
Vault(`vault/`)の作業に対するルール。Superpowers のサブエージェントはコード変更に使い、
Vaultのノート整理は従来どおり `.claude/skills/vault-loop/` の手順で回す。

## 3. Playwright — ブラウザ

`scripts/playwright-mcp.sh` が `@playwright/mcp` を起動する。クラウドでは同梱の Chromium
(`/opt/pw-browsers/chromium`)を headless・no-sandbox で使う。そうしないと
`@playwright/mcp` が別バージョンのブラウザを探して起動に失敗する。

生成したサイトを見せる例:

```bash
python scripts/generate_site.py
python -m http.server 8000 -d docs   # 別ターミナル
```

```
http://localhost:8000 を開いて、スマホ幅でスクショを撮って崩れを探して
```

クラウドではネットワーク制限で外部サイトに出られないことがある。ローカルの `docs/` 確認なら問題ない。

## 4. claude-code-setup — 使い方・自動化の提案

コードベースを読んで、合うフック・スキル・MCP・サブエージェントを1〜2個ずつ提案する(読むだけで書き換えない)。

```
このリポジトリに合う Claude Code の自動化を提案して
```

## 5. frontend-design — デザイン

ありがちな「AIっぽい」UIを避け、タイポグラフィ・配色・余白に方針を持たせるスキル。
`docs/index.html` の見た目を変えるときに使う(テンプレートは `scripts/generate_site.py` の中)。

```
frontend-design で docs/index.html を新聞の一面風に作り直して
```

## 6. Discord — スマホで操作

Claude Code Channels の Discord プラグイン。**手元のPCで `claude` が動いている間だけ**、
DiscordのDMがそのセッションに届く。クラウドセッションでは使えない。

1. [Bun](https://bun.sh) を入れる:`curl -fsSL https://bun.sh/install | bash`
2. [Discord Developer Portal](https://discord.com/developers/applications) でアプリとBotを作り、
   **Message Content Intent** を有効にしてトークンを発行する
3. OAuth2 → URL Generator(scope: `bot`)でBotを自分のサーバーに招待する
4. `claude` の中で:
   ```
   /plugin install discord@claude-plugins-official
   /discord:configure <BOTトークン>
   ```
5. チャンネル付きで起動し直す:`claude --channels plugin:discord@claude-plugins-official`
6. BotにDMするとペアリングコードが返る → `/discord:access pair <コード>`
7. 最後に `/discord:access policy allowlist` で他人を締め出す

トークンは `~/.claude/channels/discord/.env` に入る。**リポジトリにコミットしない。**

スマホから操作したいだけなら、Discordを使わずに Claude アプリの Claude Code(クラウドセッション)や
Remote Control でも同じことができる。

## 7. skill-creator — スキル

スキルの作成・改善と、評価(eval)でのトリガー精度の測定までやる。

```
/skill-creator:skill-creator 毎朝のニュースから動画台本を作るスキルを作って
```

作ったスキルは `.claude/skills/<名前>/SKILL.md` に置けば、ローカルでもクラウドでも読まれる。
