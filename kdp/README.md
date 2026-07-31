# KDP 既刊の棚卸し

既刊の一覧を `bookshelf.csv` に集約し、`scripts/kdp_inventory.py` で `INVENTORY.md`
（シリーズ別一覧＋要確認リスト）を生成する。

```bash
python scripts/kdp_inventory.py
```

- `bookshelf.csv` … 手で記入する台帳。**ここだけを編集する**
- `INVENTORY.md` … 生成物。直接編集しない

## 記入方法

KDP管理画面の**本棚（Bookshelf）**を開き、1タイトル1行で記入する。同じ作品でも
**言語ごと・形態ごと（Kindle / ペーパーバック）に別行**にする。KDPが別ASINを振るため、
棚卸しの単位もそれに合わせる。

| 列 | 内容 | 記入例 |
| --- | --- | --- |
| `series` | シリーズ名。KDP登録時のシリーズ名をそのまま | 境界の物語 |
| `volume` | 巻数。数字のみ | 3 |
| `title` | タイトル | はじまりの街 |
| `subtitle` | サブタイトル。無ければ空欄 | 霧の向こうへ |
| `language` | 言語コード | ja / en / de / fr / es / it / nl / pt-BR |
| `format` | 形態 | kindle / paperback |
| `asin` | ASIN。本棚の各タイトル下に表示される | B0AAA11111 |
| `status` | 状態 | live / in_review / draft / unpublished |
| `publish_date` | リリース日。`YYYY-MM-DD` | 2025-04-01 |
| `price` | 価格。通貨記号なしの数値 | 500 |
| `kdp_select` | KDPセレクト登録の有無 | yes / no |
| `notes` | 備考。自由記述 | |

先頭の `EXAMPLE_` で始まる行は記入例なので、実データを入れたら行ごと削除してよい
（残っていても集計からは除外される）。

### ASINをまとめて拾う場合

タイトル数が多い場合は、KDP管理画面の **レポート → ロイヤリティレポートをダウンロード**
で xlsx が取得できる。ASIN・タイトル・マーケットプレイスが並んでいるので、そこから
`asin` / `title` / `language` を転記すると手入力が減る。ただし未公開（draft / in_review）の
タイトルはレポートに出てこないため、本棚を見て手で足す必要がある。

## 生成される「要確認」

`INVENTORY.md` の末尾に、機械的に検出できる不整合が並ぶ。

- **重複** … シリーズ・巻・言語・形態がすべて同じ行が2つ以上ある（転記ミス）
- **公開中なのにリリース日／ASINが空** … 記入漏れ
- **巻数の抜け** … 同一シリーズ・同一言語で第2巻だけ無い、など。多言語展開の未着手分が
  ここに出る

## 補足

このディレクトリは KDP 出版の管理データ用で、`x-auto-poster`（分岐点ニュース）の
サイト生成とは無関係。`docs/` 配下ではないため GitHub Pages では公開されない。
