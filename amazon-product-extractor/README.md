# Amazon Product Extractor

Amazonの商品ページを開いた状態でツールバーのアイコンを押すと、その商品のタイトル・価格・ASINなどをポップアップに表示し、テキスト / JSON / CSV でコピーできるChrome拡張機能(Manifest V3)です。

## 取得する項目

| 項目 | キー | 主な取得元 |
| --- | --- | --- |
| ASIN | `asin` | URL(`/dp/`・`/gp/product/`)、なければ `input[name="ASIN"]` や `[data-asin]` |
| 商品名 | `title` | `#productTitle` |
| 価格 | `price` | `.a-price .a-offscreen` ほか |
| 評価 | `rating` | `#acrPopover .a-icon-alt` |
| レビュー数 | `reviewCount` | `#acrCustomerReviewText` |
| ブランド | `brand` | `#bylineInfo` |
| 画像URL | `image` | `#landingImage` |
| 在庫状況 | `availability` | `#availability` |
| ページURL | `url` | `location.href` |
| 取得日時 | `extractedAt` | ISO 8601形式 |

取得できなかった項目は `null` になり、ポップアップ上では「取得できませんでした」と表示されます。

## インストール(未署名の拡張機能として読み込む)

1. Chromeで `chrome://extensions/` を開く
2. 右上の **デベロッパーモード** をオンにする
3. **パッケージ化されていない拡張機能を読み込む** をクリック
4. このリポジトリの `amazon-product-extractor/` フォルダを選択する

## 使い方

1. `amazon.co.jp` または `amazon.com` の商品ページを開く
2. ツールバーの拡張機能アイコンをクリックする
3. 表示された内容をボタンでコピーする
   - **テキストをコピー**: `商品名: …` の形式で1行ずつ
   - **JSON**: 整形済みJSON
   - **CSV**: ヘッダー行＋データ1行(スプレッドシートに貼り付けやすい形式)
   - **再取得**: 価格の切り替わりなどのあとに取り直す

直近の取得結果は `chrome.storage.local` の `lastProduct` に保存されます。

## 構成

```
amazon-product-extractor/
├── manifest.json  … 権限・content script・ポップアップの定義
├── popup.html     … ポップアップのUI
├── popup.js       … 取得の実行、表示、コピー処理
├── content.js     … 商品ページ上でDOMから情報を抽出
└── icons/
    ├── icon16.png / icon48.png / icon128.png
    └── generate_icons.py  … アイコンを生成し直すスクリプト
```

`content.js` は宣言的に注入されますが、拡張機能を入れた直後などで注入されていない場合は、`popup.js` が `chrome.scripting.executeScript` で読み込んでから再試行します。

## 注意点

- Amazonのページ構造(セレクタ)は予告なく変更されます。取得できない項目が出た場合は `content.js` のセレクタを更新してください。
- Kindle本・定期おトク便・バリエーション商品など、ページによっては価格の表示要素が異なり取得できないことがあります。
- 取得したデータは外部に送信しません。処理はすべてブラウザ内で完結します。

## アイコンの再生成

```bash
python3 amazon-product-extractor/icons/generate_icons.py
```
