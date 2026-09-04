---
name: vault-loop
description: このリポジトリのVault(vault/)でLoop Engineeringのループ(capture → context → agent/draft → review → commit)を回すときに使う。inboxのノートを整理する、キャプチャを主張ノートに昇格させる、ノート同士のエッジ(supports/contradicts/supersedes)を張る、Vaultの状態を確認する、MEMORY.mdを更新する、といった依頼のとき。ニュースの取り込みやサイト生成そのもの(scripts/generate_site.py)には使わない。
---

# Vault Loop

状態はチャットではなく `vault/` にある。**このループで得た結論は、必ずノートに書いてから終わる。**
会話の中にしかない結論は、次のループでは存在しない。

設計の背景は [`LOOP-ENGINEERING.md`](../../../LOOP-ENGINEERING.md)、
レイアウトとスキーマは [`vault/README.md`](../../../vault/README.md)。

## 始める前に

1. `cat vault/MEMORY.md` — 関心テーマ・運用ルール・未解決の問いを読む
2. `python scripts/loop.py status` — Vaultの現在地(滞留しているinboxの量)を見る

## 1. Capture

自動取り込みは毎朝のワークフローが回している。手で落とすときだけ:

```bash
python scripts/loop.py capture --note "思いついたこと" --tag design
```

このステップでは判断しない。落とすだけ。

## 2. Context

昇格させる候補を1つ選び、文脈を集める:

```bash
python scripts/loop.py context <id>
```

出力には対象ノート・出ていくエッジ・入ってくるエッジ・近いノート・MEMORY.mdが入る。
**この出力の外にある情報を前提にしない。** 足りなければ `context` の対象を変えるか、
必要なノートを `Read` で読む(推測で補わない)。

出力が打ち切られたら、それは文脈が多すぎるのではなくノートの粒度が粗いというサイン(ルール3)。

## 3. Agent / Draft

普段のVaultには直接書かない。worktreeを切る:

```bash
git worktree add ../x-auto-poster-draft -b draft/$(date +%Y-%m-%d)
```

その中で、キャプチャを主張ノートに昇格させる:

```bash
python scripts/loop.py promote <id> --title "1文で言える主張" --tag ai
```

生成された `10-notes/` のノートを埋める。守ること:

- **1ノート=1主張。** 2つ言いたくなったらノートを2つにする
- 「主張」は1文。長い説明は「根拠」に置く
- 「反証されうる点」を必ず書く。書けない主張は、まだ主張になっていない
- 関連するノートには `supports` / `contradicts` / `supersedes` でエッジを張る。
  IDは `python scripts/loop.py context <id>` の出力から取る(手で書かない)
- 既存ノートを更新するときは**本文を書き換えず**、`## 追記 YYYY-MM-DD` を足すか、
  新しいノートを作って `supersedes` で古い方を指す

## 4. Review

機械チェックを先に通す:

```bash
python scripts/loop.py review --strict
```

エラーが出たら直す。通ったら `vault-critic` サブエージェントに差分を渡して批評させる
(Agentツール、`subagent_type: "vault-critic"`)。渡すのは `git diff` と、
関係するノートのID。指摘は原則として取り込む。取り込まないときは理由をノートに追記する。

エージェントはこの1つだけ(ルール4)。批評役をさらに増やさない。

## 5. Commit

```bash
git commit -m "notes: <何を足したか>"
```

Vaultへの変更は**追加**か**追記**であること。既存ノートの行が消える差分になっていたら、
それはこのループのやり方を間違えている。

最後に `vault/MEMORY.md` を更新する:

- 新しく見えてきたテーマ → 「関心テーマ」に1行(目安5つまで)
- 解けた問い → 「未解決の問い」の行を消さずに `→ <id>` を追記する
- 新しく決めた運用ルール → 「運用ルール」に1行

`<!-- loop:last-run -->` ブロックは `loop.py` が管理しているので手で触らない。

## 掃除

`status` で滞留が目立ってきたら、扱わないと決めたものを畳む:

```bash
python scripts/loop.py archive --dry-run   # 対象を確認
python scripts/loop.py archive             # status を archived にして追記する
```

消さない。畳むだけ。扱う気になったら `status` を `inbox` に戻せばループに復帰する。
