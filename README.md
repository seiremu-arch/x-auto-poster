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
python scripts/loop.py canvas                # エッジから vault/graph.canvas を作り直す
python scripts/loop.py review                # スキーマとエッジを検証(CIと同じ)
python scripts/loop.py status                # Vaultの現在地
```

`vault/` はそのまま Obsidian の vault として開けます(`vault/graph.canvas` がノートのつながり、
`vault/vault.base` が受信箱・主張・情報源のビュー)。詳細は
[`LOOP-ENGINEERING.md`](LOOP-ENGINEERING.md#obsidianで開く) を参照してください。

`Daily News Update` ワークフローが毎朝 `capture` → `canvas` → `review` → サイト生成の順に実行し、
`docs/index.html` と `vault/` の変更をまとめてコミットします。Vaultへの変更は
`Vault Review` ワークフローが検証します(スキーマ違反とエッジのリンク切れはCIで落ちます)。

## 日経225レバレッジ(`scripts/lev225.py`)

日経平均の2倍レバレッジ商品(1570 など)だけを対象にした、シグナル生成と
バックテストのCLIです。個別株の流動性を避けて指数レバレッジに寄せる、という前提で
作ってあります。依存は標準ライブラリだけです。

```bash
python scripts/lev225.py selftest                 # 計算式の自己検証(ネット不要)
python scripts/lev225.py fetch --out n225.csv     # 日経平均の日足を取得
python scripts/lev225.py backtest --csv n225.csv  # 全戦略を比較
python scripts/lev225.py signal --csv n225.csv    # 今日の目標ポジション
```

### 何を計算しているか

入力は**日経平均そのもの**の日足CSVです。レバレッジETFの値動きは、その指数から
日次リバランスを再現して合成します(`ETF_t = ETF_{t-1} × (1 + 2×r_t − 信託報酬/245)`)。
ETFの実際の価格ではなく指数から合成するのは、**減価がどこから来ているかを分離して
見るため**です。

この減価が、この商品を扱ううえでの中心的な事実です。指数が +10% → −9.0909% と
往復すると指数は元の水準に戻りますが、2倍側は 0.9818 倍にしかなりません。
同じ往復を100回繰り返すと、指数は横ばいのまま2倍側は 0.16 倍まで削れます
(→ `vault/10-notes/` の主張 `e0d65fcdb7`)。

### 戦略

| 名前 | 中身 |
| --- | --- |
| `buyhold` | 常にフルポジション。比較の基準線 |
| `flat` | 常にノーポジション。コスト計算の対照 |
| `sma` | 指数が移動平均(既定200日)より上のときだけ持つ |
| `voltarget` | 実現ボラが目標(既定25%)を超えたらポジションを落とす |
| `sma_vol` | トレンドで方向を、ボラで大きさを決める |

### バックテストが嘘をつかないための約束

- **未来を見ない**: 戦略は「i日目の終値まで」の情報だけでポジションを決め、それが
  効くのは i+1 日目から。`selftest` がこの整合を検証します
- **約定の遅れを試せる**: `--exec-lag 1` で、終値で建てられず翌日になる場合の感度を見る
- **コストを引く**: `--cost-bps`(往復、既定10bps)と信託報酬を毎日引く
- **建て替えすぎない**: `--rebalance-band`(既定0.10)未満の変更は発注しない。
  幅を入れないとボラターゲットは毎日わずかに建て替え、実際には執行できません
- **期間を分ける**: `--split 0.6` で前半/後半を分けて出す。**後半で崩れる戦略は
  過去に合わせ込んだだけ**なので捨ててください

### 限界

- 再現していないもの: 先物のロールコスト、金利、信託財産留保額、ETFの市場価格と
  基準価額の乖離(プレミアム/ディスカウント)、約定の滑り
- `fetch` は stooq から取得しますが、**開発時に外部接続が塞がれていたため未検証**です。
  落ちた場合は URL を直接開いてCSVが返るか確かめてください
- **このスクリプトは発注しません。** `signal` が出す目標ポジションが発注系との境界です。
  実際に自動売買につなぐ場合は、証券会社のAPI側で建玉・資金・二重発注を管理してください
- `signal` の「現在の建玉」は「初日からこの戦略を回していたら」の理論値です。
  実際の残高とは別に管理してください

## ローカルでの実行

```bash
pip install -r requirements.txt
python scripts/generate_site.py
```

`docs/index.html` が生成されます。Vault側だけを検証したいときは `python scripts/loop.py review` を実行してください。
