# Loop Engineering — このリポジトリの設計メモ

このリポジトリはもともと「RSSを毎朝取ってきて `docs/index.html` を作り直す」だけの
パイプラインだった。毎回ゼロから作り直すので、**昨日のランが何を知っていたかは残らない**。

Loop Engineering は、その状態をチャットでもスクリプトの変数でもなく、
ローカルのMarkdown Vault(`vault/`)に置く設計パターン。Vault自体が状態を持ち、
ループを回すたびに勝手に育っていく。

- Vaultの使い方(レイアウト・スキーマ・ルール): [`vault/README.md`](vault/README.md)
- ループを回すCLI: [`scripts/loop.py`](scripts/loop.py)
- Claude用の手順: [`.claude/skills/vault-loop/SKILL.md`](.claude/skills/vault-loop/SKILL.md)

## 核心

> ループの状態を持つのはVault。チャット画面じゃない。

Claudeが知っていることはすべて `.md` の中にある。会話が終わっても文脈は終わらない。
逆に言えば、**会話の中にしかない結論は、次のループでは存在しない**ものとして扱う。

## 基本ループ

```
capture → context → agent/draft → review → commit
```

| ステップ | 何をするか | このリポジトリでの実体 |
| --- | --- | --- |
| Capture | 思いついたこと・拾った記事を `00-inbox` に落とすだけ | `loop.py capture` (毎朝のワークフロー / 手動) |
| Context | リンク・タグ・近くのノートを集める | `loop.py context <id>` |
| Agent / Draft | worktreeの中で編集する。普段のVaultには直接書かない | `git worktree` + Claude |
| Review | 批評役のエージェントが差分をチェックする | `loop.py review` + `vault-critic` エージェント |
| Commit | 追記して(書き換えず、足すだけ)Vaultに戻す | 通常のcommit + `vault-review` ワークフロー |

人がやることは基本的に「思考をinboxに落とす」だけで、あとはこのループが回る。

## ノートスキーマ = グラフのエッジ

frontmatter の `supports` / `contradicts` / `supersedes` / `derived_from` は、
単なるメタデータではなく**ノート同士を結ぶエッジ**。だから `loop.py review` は
リンク切れをエラーとして落とす(壊れたエッジはグラフの破損であって、書式の乱れではない)。

## Vaultグラフ

5種類のノードと、その間のエッジでできている。

```
Source ──derived_from──▶ Capture ──derived_from──▶ Claim ──supports───▶ Claim
                                                     │  └─contradicts─▶ Claim
                                                     │  └─supersedes──▶ Claim(古い方)
Entity ◀──言及───────────────────────────────────────┘
Run ────記録────▶ そのランで作られたノート / Artifact
```

- **Source** — 情報源。`config/feeds.json` のフィード1本が1ノート
- **Capture** — 生の取り込み。まだ判断していない
- **Claim** — 1文の主張。ループの中心はここ
- **Entity** — 人・組織・製品
- **Artifact** — 外に出したもの(生成サイト、投稿文)
- **Run** — 1回の実行の記録

## 6つのプリミティブ

このリポジトリで今どこまで使っているか。増やすのは必要になってから。

| プリミティブ | 使用状況 |
| --- | --- |
| automations(スケジュール実行) | ✅ `.github/workflows/daily-update.yml` が毎朝 capture + サイト生成 |
| worktrees(実験用ブランチ) | ✅ Draft は worktree の中で行う(下記) |
| skills | ✅ `.claude/skills/vault-loop/` |
| connectors | ⛔ 未使用。RSSで足りているうちは足さない |
| sub-agents | ✅ `vault-critic` の1つだけ(ルール4) |
| memory | ✅ `vault/MEMORY.md` |

## 4つの形(Shape)

コストの目安は「Claudeを1回直接呼ぶ場合」を1とした相対値。

| 形 | 外部化するもの | コスト目安 | このリポジトリ |
| --- | --- | --- | --- |
| Loop | 時間(繰り返し) | 1〜2x | ← 今ここ |
| Chain | 手順 | 2〜3x | promote → review の2段 |
| Network | 役割(複数エージェント) | 3〜4x | critic 1つまで |
| Graph | 知識構造そのもの | 2〜4x | 会話をまたいでノートの状態を持ち越したくなったら |

全体としては、Claudeを1回直接呼ぶのに比べて **2〜4倍** のコストで回る設計。

## いつ次の形に移るか

安く始めて、必要になってからエスカレートする。

1. まずは **Loop** だけ。`capture` と `review` を回す
2. 毎回同じ手直しをしていると気づいたら **Chain**(手順をスクリプトかスキルに固定する)
3. 「作る側」と「批評する側」を分けたくなったら **Network**(ただしエージェントは2つまで)
4. 会話をまたいでノートの状態を持ち越したくなったら **Graph**(リンク構造を本格的に進める)

## 5つのルール

1. **安く始める** — capture と review から。エージェントを増やすのは最後
2. **追記する、書き換えない** — 更新は追記か、新ノート + `supersedes`
3. **トークンを数える** — `context` の出力が長くなったら、リンクではなくノートを分割する
4. **エージェントを増やしすぎない** — 1ループにつき、作る側1つと批評する側1つまで
5. **状態はVaultに置く** — 会話の中だけにある結論は存在しないものとして扱う

## worktreeでのDraft

普段のVaultに直接書かないための手順。

```bash
git worktree add ../x-auto-poster-draft -b draft/2026-09-04
cd ../x-auto-poster-draft
python scripts/loop.py context <id>       # 文脈を集める
# ノートを編集する
python scripts/loop.py review --strict    # 批評の前に機械チェック
git commit -am "notes: ..." && git push -u origin draft/2026-09-04
cd - && git worktree remove ../x-auto-poster-draft
```

## 出典

海外で共有されている Claude + Obsidian の Loop Engineering / LLM Wiki パターンを、
このリポジトリ(RSS集約サイト)向けに具体化したもの。
