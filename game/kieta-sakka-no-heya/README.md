# 消えた作家の部屋 — HTML5 推理アドベンチャー

『消えた作家の部屋』を、そのままブラウザで遊べる推理ゲームにしたもの。
外部ライブラリ・外部通信ゼロの**単一HTMLファイル**なので、itch.io のHTML5枠にZIPを投げるだけで動きます。

- 設計（登場人物・トリック・動機・証拠15点・エンディング3種）: [DESIGN.md](DESIGN.md)
- 本体: `index.html`
- 想定プレイ時間: 25〜40分

## 遊び方（ローカル確認）

`index.html` をブラウザにドラッグ&ドロップするだけ。サーバは要りません。

## ZIPを作る

```bash
./build.sh
# => dist/kieta-sakka-no-heya.zip
```

ZIP の**直下に index.html がある**状態でなければ itch.io は動かしてくれません。`build.sh` はその形で固めます。

## itch.io へのアップロード手順

1. https://itch.io/game/new を開く
2. **Title** に「消えた作家の部屋」
3. **Kind of project** を `HTML` にする
4. **Uploads** → `dist/kieta-sakka-no-heya.zip` をアップロードし、`This file will be played in the browser` にチェック
5. **Embed options**
   - Viewport dimensions: `1280 × 800`
   - `Mobile friendly` にチェック（縦画面でも遊べます）
   - `Fullscreen button` を有効に
6. **Genre** は `Visual Novel`、**Tags** に `mystery` `detective` `text-based` `japanese` `story-rich` あたり
7. 右下 **Save & view page** → 実際に遊べるか確認 → **Visibility & access** を `Public` にして公開

### butler（CLI）で更新する場合

```bash
butler push dist/kieta-sakka-no-heya.zip <ユーザー名>/kieta-sakka-no-heya:html5
```

## 中身を差し替えるとき

物語のテキストは `index.html` 内の `EV`（証拠15点）、`PLACES`（場所10と調べる対象）、
`TALK`（会話と証拠の突きつけ）、`DEDUCE`（推理の3問）、`ENDINGS`（結末3種）に
すべてデータとして分離してあります。演出コードに触らずに文章だけ書き換えられます。
