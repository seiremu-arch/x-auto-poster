# Vault — ループの状態を持つ場所

このディレクトリが **このリポジトリの状態機械** です。チャットの履歴ではなく、ここにある `.md`
ファイルだけが「Claudeが知っていること」の全てになります。会話が終わっても文脈は消えません。

前提: [Loop Engineering](../LOOP-ENGINEERING.md) の設計メモを先に読んでください。

## レイアウト

| ディレクトリ | 役割 | 誰が書くか |
| --- | --- | --- |
| `00-inbox/` | 生のキャプチャ。RSSの記事1件、思いつきのメモ1件がそれぞれ1ノート | `loop.py capture`(自動) / 人 |
| `10-notes/` | 原子ノート。1ノート=1つの主張(claim)か1つの概念 | Claude(昇格時) / 人 |
| `20-sources/` | 情報源ノート。RSSフィード1本につき1ノート | `loop.py capture`(自動) |
| `30-artifacts/` | ループが外に出した成果物の記録(生成サイト、投稿文など) | Claude / 人 |
| `40-runs/` | ラン(実行)のログ。いつ何件取り込み、何を昇格したか | `loop.py`(自動) |
| `MEMORY.md` | ループをまたいで持ち越す短い状態。関心テーマ・運用ルール・未解決の問い | Claude / 人 |

`.claude/skills/vault-loop/` にループの回し方、`.claude/agents/vault-critic.md` に批評役の
定義があります。

## ノートスキーマ = グラフのエッジ

frontmatter はメタデータではなく **グラフの辺** です。`supports` / `contradicts` /
`supersedes` / `derived_from` に書いたIDが、そのままノート間のエッジになります。
リンク切れは `loop.py review` がエラーにします(書式の乱れではなく、グラフの破損として扱う)。

```markdown
---
id: 3f9a1c04b2
type: capture          # capture | claim | entity | source | artifact | run
title: 記事や主張のタイトル
status: inbox          # inbox | promoted | active | archived
source: NHKニュース(主要)
url: https://example.com/article
published: 2026-09-04T06:12:00+09:00
captured_at: 2026-09-04T06:30:11+09:00
tags: [ai, policy]
supports: [a1b2c3d4e5]      # このノートが補強するノートのID
contradicts: [f6e5d4c3b2]   # 矛盾するノートのID
supersedes: [0011223344]    # 置き換える(古くなった)ノートのID
derived_from: [9988776655]  # 出自(claim ← capture ← source)
---

本文。追記のみで育てる。
```

必須キー: `id` / `type` / `title` / `status`。エッジ4種と `tags` は省略可(空リスト扱い)。
`id` は URL の SHA-1 先頭10桁(手動ノートは本文+時刻のハッシュ)で、ファイル名にも含めます。

### ノードの種類

- **source** — 情報源(RSSフィード、サイト、人)
- **capture** — 生の取り込み。まだ判断していないもの
- **claim** — 「何が言えるか」を1文にした主張。ループの中心
- **entity** — 人・組織・製品などの固有名詞
- **artifact** — 外に出したもの(生成サイト、投稿文)
- **run** — 1回の実行の記録

## 基本ループ

```
capture → context → agent/draft → review → commit
```

1. **Capture** — `python scripts/loop.py capture` で `00-inbox/` にノートが落ちる。
   手で思いつきを落とすなら `python scripts/loop.py capture --note "思いついたこと"`。
2. **Context** — `python scripts/loop.py context <id>` が、リンク・タグ・同じ情報源・
   近いノートを集めて1つの文脈バンドルとして出力する。
3. **Agent / Draft** — Claudeは `git worktree` の中で編集する。普段のVaultには直接書かない。
   `python scripts/loop.py promote <id>` が `10-notes/` に原子ノートの骨組みを作る。
4. **Review** — `python scripts/loop.py review --strict` がスキーマとエッジを機械的に検証し、
   `vault-critic` エージェントが差分を批評する。
5. **Commit** — 追記(書き換えず、足すだけ)でVaultに戻す。

掃除は `python scripts/loop.py archive`(30日以上昇格されなかったinboxノートを `archived` にする)。
現在地は `python scripts/loop.py status`。

## 5つのルール

1. **安く始める** — まずは capture と review だけ。エージェントを増やすのは最後。
2. **追記する、書き換えない** — 既存ノートの本文は消さない。更新は `## 追記 YYYY-MM-DD` を足すか、
   新しいノートを作って `supersedes` で古い方を指す。
3. **トークンを数える** — `context` の出力が長くなったら、リンクを削るのではなく原子ノートを分割する。
4. **エージェントを増やしすぎない** — 1ループにつき、作る側1つと批評する側1つまで。
5. **状態はVaultに置く** — 会話の中だけにある結論は、次のループでは存在しないものとして扱う。
