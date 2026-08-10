---
type: ナレッジ
created: 2026-08-10
updated: 2026-08-10
tags:
  - Python
---

# 静的HTML生成スクリプト

## 要点

テンプレートエンジンを入れず、Pythonのf-stringだけでHTMLを組み立てるときの型。依存を減らせる代わりに、**波括弧のエスケープ**と**HTMLエスケープ**の2つを自分で面倒みる必要がある。

## 詳細

### 波括弧のエスケープ

f-string内のCSSは `{` `}` をすべて2重にする。ここを1つでも忘れると `KeyError` か構文エラーで落ちる。

```python
return f"""<style>
  body {{
    margin: 0;
    color: {fg_color};
  }}
</style>"""
```

CSSが長くなるほど事故りやすい。CSSだけ別の通常文字列にして `+` で連結するか、`.format()` を使わない素の文字列に逃がすほうが安全な場面も多い。

### 外部由来の文字列は必ずエスケープ

RSSのタイトルやURLはそのまま埋めない。

```python
title = html.escape(article["title"])
link = html.escape(article["link"])
```

`html` は標準ライブラリなので依存は増えない。逆に、エスケープできない/したくないHTML片(フィードの `summary` など)は、サニタイズの手当てをするまで**出さない**という判断もある。

### 関数を階層で分ける

`render_article()` → `render_section()` → `render_html()` と、小さい単位から組み上げる。各関数が文字列を返すだけなので、単体で呼んで目視確認できる。

### 出力先を先に作る

```python
OUTPUT_HTML.parent.mkdir(parents=True, exist_ok=True)
OUTPUT_HTML.write_text(html_content, encoding="utf-8")
```

`encoding="utf-8"` は明示する。CIのロケール次第で書き出しが壊れる。

### パスはスクリプト位置から解決する

```python
ROOT = Path(__file__).resolve().parent.parent
```

カレントディレクトリに依存させない。CIとローカルで実行位置が違っても同じ場所に出る。

### 結果を標準出力に出す

件数を stdout、失敗を stderr に出しておくと、Actionsのログだけで成否が判断できる。

## ハマったこと

- ライト/ダーク両対応のCSSを書くとき、`prefers-color-scheme` のメディアクエリと `[data-theme]` の両方を定義しないと、明示的なテーマ切り替えが効かない。
- 生成物をリポジトリにコミットする構成では、毎日全文が差分になる。更新時刻を埋め込むと**内容が同じでも必ず差分が出る**ので、無変更でコミットを止めたいなら時刻の扱いを考える必要がある。

## 使っている案件

- [[分岐点ニュース]] — [[構成とデータフロー]]

## 関連

- [[feedparser]]
- [[GitHub Pages]]

---

親: [[ホーム]] / 書き方: [[運用ルール]]
