---
type: ナレッジ
created: 2026-08-10
updated: 2026-08-10
tags:
  - RSS
  - Python
---

# feedparser

## 要点

RSS 2.0 / RDF / Atom を同じインターフェースで読めるPythonライブラリ。`feedparser.parse(url)` にURLを渡せば取得とパースを両方やる。ピン留めして使っているバージョンは `feedparser==6.0.11`。

## 詳細

### 基本

```python
import feedparser

parsed = feedparser.parse(
    url,
    agent=USER_AGENT,
    request_headers={"User-Agent": USER_AGENT},
)
for entry in parsed.entries:
    entry.get("title")
    entry.get("link")
    entry.get("summary")
    entry.get("published_parsed")   # UTC の time.struct_time or 無い
```

`entry` は辞書としても属性としても引ける。**取れないキーがあるのが普通**なので、`entry.title` ではなく `entry.get("title", "")` を使う。

### bozo

パースで問題が起きると例外を投げず、`parsed.bozo` が真になり `parsed.bozo_exception` に理由が入る。ここが重要で、bozoでも `entries` が取れていることは多い(軽微な整形式違反など)。

```python
if parsed.bozo and not parsed.entries:
    raise parsed.bozo_exception or RuntimeError("failed to parse feed")
```

**「bozoなら失敗」ではなく「bozoかつ記事0件なら失敗」** と判定する。前者にすると読めるフィードまで捨てる。

### ネットワークエラーも例外にならない

DNS失敗や404も `parse()` は投げずに返してくる。結果は「bozo + entries空」になるので、上の判定でまとめて拾える。呼び出し側は `try/except` に加えてこの判定が要る。

## ハマったこと

- タイムアウトの引数が無い。`parse()` は `timeout` を受け取らないので、厳密に制御したいなら `requests` などで自分で取ってきた文字列を `parse()` に渡す形にする。
- `summary` はHTMLタグを含むことがある。そのまま出すならサニタイズが要る。

## 使っている案件

- [[分岐点ニュース]]

## 関連

- [[RSSフィード収集]]
- [[静的HTML生成スクリプト]]

---

親: [[ホーム]] / 書き方: [[運用ルール]]
