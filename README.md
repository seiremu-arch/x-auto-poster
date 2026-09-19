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

## 日経225(`scripts/n225.py`)

日経225を対象にした、シグナル生成とバックテストのCLIです。個別株の流動性を避けて
指数そのものを売買する前提で、レバレッジは**証拠金で建玉を持つ形(先物)**を
想定しています。依存は標準ライブラリだけです。

```bash
python scripts/n225.py selftest                          # 計算式の自己検証(ネット不要)
python scripts/n225.py fetch --out n225.csv              # 日経平均の日足を取得
python scripts/n225.py backtest --csv n225.csv --compare # 戦略比較 + 減価の比較
python scripts/n225.py signal --csv n225.csv --equity 3000000
```

### 減価はレバレッジではなくリバランスから出る

このスクリプトの中心にある事実です。指数が **+10% → −9.0909%** と往復して
元の水準に戻ったとき:

| 持ち方 | 結果 |
| --- | --- |
| 建玉を固定したまま(先物) | **ちょうど元に戻る(減価ゼロ)** |
| 毎日2倍に戻す(レバETF 1570など) | **0.9818 倍**(減価) |

減価を生むのは「レバレッジをかけたこと」ではなく「**毎日レバレッジ比率を一定に
戻したこと**」です。この往復を100回繰り返しても、建玉固定は 1.000 のまま、
日次リバランスだけが 0.16 倍まで削れます(`selftest` が検証します)。

だからエンジンは建玉(想定元本)を状態として持ち、リバランスを
`--rebalance-band` 1つで連続的に扱います。

- `--rebalance-band 0` … 毎日きっちり戻す → レバETFと同じ減価が出る
- `--rebalance-band 大` … ほぼ建て替えない → 先物の建玉固定、減価は出ない

**代わりに別のリスクが立ちます。** 建玉を固定すると含み損で証拠金維持率が下がり、
`--maintenance-margin` を割ればロスカットされます。また利益が出ると実効レバレッジが
下がり、損が出ると上がります(損失時に勝手にレバがかかる)。
**減価が消えるのではなく、リスクの形がボラティリティ減価から強制決済に置き換わります。**

### 商品プリセット(`--instrument`)

| | レバレッジ | 保有コスト | リバランス幅 | 維持率 |
| --- | --- | --- | --- | --- |
| `index` | 1.0 | 0.19%/年 | 0.20 | なし |
| `futures`(既定) | 2.0 | 0% | 0.20 | 10% |
| `etf2x`(比較用) | 2.0 | 0.80%/年 | 0(毎日) | なし |

いずれも `--leverage` `--carry` `--rebalance-band` `--maintenance-margin` で上書きできます。

### 戦略

| 名前 | 中身 |
| --- | --- |
| `buyhold` | 常にフルポジション。基準線 |
| `flat` | 常にノーポジション。コスト計算の対照 |
| `sma` | 指数が移動平均(既定200日)より上のときだけ持つ |
| `voltarget` | 指数の実現ボラが目標(既定18%)を超えたら建玉を落とす |
| `sma_vol` | トレンドで方向を、ボラで大きさを決める |

### バックテストが嘘をつかないための約束

- **未来を見ない**: 戦略は「i日目の終値まで」の情報だけで決め、効くのは i+1 日目から
- **独立実装と突き合わせる**: `--rebalance-band 0` のエンジンが、レバETF基準価額の
  閉じた式と小数9桁まで一致することを `selftest` が確認します
- **約定の遅れを試せる**: `--exec-lag 1` で終値に建てられない場合の感度を見る
- **コストを引く**: `--cost-bps`(往復、既定5bps)と保有コストを毎日引く
- **期間を分ける**: `--split 0.6` で前半/後半に分割。**後半で崩れる戦略は
  過去に合わせ込んだだけ**なので捨ててください

### 限界

- 再現していないもの: 先物のロールコストと限月間スプレッド、金利、配当、
  SPAN証拠金の日々の変動、約定の滑り、板の厚み
- `fetch` は stooq から取得しますが、**開発時に外部接続が塞がれていたため未検証**です
- **このスクリプトは発注しません。** `signal` が出す目標建玉が発注系との境界です
- `signal` の「現在の建玉」は「初日からこの戦略を回していたら」の理論値です。
  実際の残高とは別に管理してください
- 必要証拠金は SPAN により日々変わります。`--maintenance-margin` は概算です

## ローカルでの実行

```bash
pip install -r requirements.txt
python scripts/generate_site.py
```

`docs/index.html` が生成されます。Vault側だけを検証したいときは `python scripts/loop.py review` を実行してください。
