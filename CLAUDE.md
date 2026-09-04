# x-auto-poster

RSSフィードから記事を集め、事実/意見に分けて `docs/index.html` を毎朝生成する静的サイト。
それに加えて、取り込んだものを `vault/` にMarkdownノートとして蓄積する
Loop Engineering の構成になっている。

- サイト生成: `scripts/generate_site.py`(`config/feeds.json` → `docs/index.html`)
- Vaultのループ: `scripts/loop.py`(capture / context / promote / archive / review / status)
- Vaultの読み書き: `scripts/vault.py`
- 設計: [`LOOP-ENGINEERING.md`](LOOP-ENGINEERING.md) / [`vault/README.md`](vault/README.md)

## Vaultを触るときの不変条件

1. **状態はVaultにある。** 会話の中にしかない結論は、次のループでは存在しない。
   結論はノートに書いてから終わる。
2. **追記する、書き換えない。** 既存ノートの本文の行が消える差分は、原則として誤り。
   更新は `## 追記 YYYY-MM-DD` を足すか、新しいノートを作って `supersedes` で古い方を指す。
3. **frontmatterのエッジはグラフの辺。** `supports` / `contradicts` / `supersedes` /
   `derived_from` のリンク切れは `loop.py review` がエラーにする。
4. **IDは手で書かない。** `loop.py` が作る。参照するIDは `loop.py context <id>` の出力から取る。

ノートを整理・昇格する作業は `.claude/skills/vault-loop/` の手順に従う。
批評は `vault-critic` サブエージェント1つだけに任せる(エージェントを増やさない)。

## 変更したら

```bash
python scripts/loop.py review        # Vaultの検証(CIと同じ)
python scripts/generate_site.py      # サイト生成(docs/index.html が変わる)
```
