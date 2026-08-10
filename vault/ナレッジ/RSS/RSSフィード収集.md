---
type: ナレッジ
created: 2026-08-10
updated: 2026-08-10
tags:
  - RSS
---

# RSSフィード収集

## 要点

複数媒体のRSSをまとめて取りに行くときは、**1本の失敗で全体を落とさない**のが最優先。フォーマットの揺れ(RSS 2.0 / RDF / Atom)は [[feedparser]] が吸収してくれるので、自前パースはしない。

## 詳細

### フィードの種類は混在する

同じ「RSS」でも中身は違う。実例:

- `https://www3.nhk.or.jp/rss/news/cat0.xml` — RSS 2.0
- `https://www.47news.jp/rss/47news.rdf` — RDF(RSS 1.0)
- 媒体によってはAtom

パーサを統一しておけば呼び出し側は同じコードで扱える。

### 日時フィールドは統一されていない

`published` があるフィードと `updated` しかないフィードがある。両方見て、どちらも無ければ「不明」として扱えるようにしておく。

```python
for key in ("published_parsed", "updated_parsed"):
    value = entry.get(key)
    if value:
        return datetime(*value[:6], tzinfo=timezone.utc)
return None
```

`*_parsed` はUTCの `time.struct_time` なので、`tzinfo=timezone.utc` を付けてawareにしてから表示タイムゾーンへ変換する。naiveのまま比較するとソートで落ちる。

### User-Agent を付ける

デフォルトのUAだと弾く媒体がある。識別可能なUAを名乗る。

### 取得件数を絞る

フィードは数十件返してくることがある。媒体ごとに上限(例: 8件)を掛けてから全体をマージすると、1媒体がページを占有しない。

## ハマったこと

- **公開日時が無い記事のソート**: `None` を含むリストをそのまま `sort()` すると `TypeError`。`a["published"] or datetime.min.replace(tzinfo=timezone.utc)` のようにフォールバックを噛ませる。
- **エラーを握りつぶしすぎない**: 例外は捕まえるが、どのフィードがなぜ落ちたかは必ず出力に残す。黙って空になるのが一番気付けない。

## 使っている案件

- [[分岐点ニュース]] — [[フィード運用メモ]] に実際の運用手順

## 関連

- [[feedparser]]
- [[事実と意見の分類]]

---

親: [[ホーム]] / 書き方: [[運用ルール]]
