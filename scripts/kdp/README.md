# KDP制作パイプライン

Markdownの原稿と `book.yaml` から、KDP(Kindle Direct Publishing)にそのまま入稿できる
**docx(電子書籍用・ペーパーバック用)** と **EPUB3** を生成する。目次・改ページ・奥付・
入稿前チェックはすべてスクリプトが受け持つので、原稿を直したらビルドし直すだけでよい。

```bash
pip install -r requirements.txt
python scripts/build_book.py manuscripts/sample-book
```

## 目次

- [ディレクトリ構成](#ディレクトリ構成)
- [コマンド](#コマンド)
- [book.yaml の書き方](#bookyaml-の書き方)
- [原稿の書き方](#原稿の書き方)
- [目次の作られ方](#目次の作られ方)
- [入稿前チェック](#入稿前チェック)
- [出力物とKDPへの入稿](#出力物とkdpへの入稿)
- [自動ビルド(GitHub Actions)](#自動ビルドgithub-actions)
- [モジュール構成](#モジュール構成)

## ディレクトリ構成

```
manuscripts/
  sample-book/
    book.yaml            # メタデータと組版設定
    manuscript/
      00-まえがき.md      # ファイル名順に並ぶ = 章順
      01-第1章.md
      ...
    assets/              # 図版・表紙画像
scripts/
  build_book.py          # ビルドCLI
  kdp/                   # パイプライン本体
build/
  <slug>/                # 出力先(gitignore 済み)
```

本を増やしたいときは `manuscripts/` の下にディレクトリを1つ足すだけでよい。

## コマンド

```bash
# 既定: docx(ebook + print)と EPUB をまとめて生成
python scripts/build_book.py manuscripts/sample-book

# ペーパーバック用の docx だけ
python scripts/build_book.py manuscripts/sample-book --target docx --profile print

# EPUB だけ
python scripts/build_book.py manuscripts/sample-book --target epub

# 入稿前チェックだけ(警告もエラー扱いにする)
python scripts/build_book.py manuscripts/sample-book --check-only --strict

# 出力先を変える
python scripts/build_book.py manuscripts/sample-book --out /tmp/out
```

`manuscripts/` 直下に本が1つしかない場合は、引数を省略できる。

| 終了コード | 意味 |
| --- | --- |
| `0` | 成功 |
| `1` | 入稿前チェックでエラー(`--strict` なら警告)が出た |
| `2` | 設定ファイルまたは原稿ファイルの指定に問題がある |

## book.yaml の書き方

1冊分のメタデータと組版設定をここにまとめる。

```yaml
slug: kdp-pipeline-guide     # 出力ファイル名(省略可)
title: 本のタイトル           # 必須
subtitle: サブタイトル
author: 著者名                # 必須
publisher: 個人出版
language: ja
published: 2026-08-25
isbn: ""                     # KDPの無料ISBNを使うなら空でよい

description: |               # KDPの「内容紹介」。4000文字まで
  本の紹介文。
keywords: [Kindle出版, KDP]   # 7個まで
categories: [コンピュータ・IT]
cover: assets/cover.jpg      # 1600×2560px以上のJPEG推奨

manuscript:
  - manuscript/*.md          # globはファイル名順。明示列挙なら書いた順

frontmatter:
  title_page: true           # 扉ページ
  copyright_page: false      # 前付の権利表記
  colophon: true             # 巻末の奥付
  colophon_note: 補足文

ebook:                       # 電子書籍プロファイル
  base_font_pt: 11
  line_spacing: 1.8
  toc: {title: 目次, depth: 2, style: link}

print:                       # ペーパーバックプロファイル
  trim: 6x9
  base_font_pt: 10.5
  line_spacing: 1.7
  margins: {top: 20, bottom: 20, inside: 19, outside: 13, gutter: 0}
  mirror_margins: true       # 見開きで内外の余白を入れ替える
  page_numbers: true         # フッターにノンブル
  toc: {title: 目次, depth: 2, style: field}
```

### 判型(`print.trim`)

`5x8` `5.06x7.81` `5.25x8` `5.5x8.5` `6x9` `6.14x9.21` `7x10` `8x10` `8.5x11`
(KDPの規格サイズ)のほか、日本語書籍向けに `a5` `b6` `shinsho`(新書) `shiroku`(四六判)
`bunko`(文庫)が使える。`四六判` `新書` `文庫` のような日本語表記や `128x182mm` も解釈される。
`{width_mm: 128, height_mm: 182}` のように直接指定してもよい。

### プロファイルの違い

|  | `ebook` | `print` |
| --- | --- | --- |
| 判型 | 持たない(既定 6×9相当) | `trim` で固定 |
| 余白 | 一律15mm | ノド/小口を分けて指定、`mirror_margins` |
| ノンブル | なし | フッター中央 |
| 目次 | リンク付き目次 | Wordの目次フィールド(ページ番号付き) |

## 原稿の書き方

Markdownのうち、書籍で必要な記法だけをサポートしている。

| 記法 | 意味 |
| --- | --- |
| `# 見出し` | 章。**新しいページから始まる** |
| `## 見出し` / `### 見出し` | 節・項 |
| 空行区切りの文 | 段落(日本語は行を連結するとき空白を入れない) |
| `- 項目` / `1. 項目` | 箇条書き(インデント2段階まで) |
| `> 引用` | 引用 |
| ` ```lang ` | コードブロック |
| `![キャプション](path)` | 図版(単独行で書く) |
| `---` | シーン区切り(`＊　＊　＊`) |
| `<!-- pagebreak -->` | 強制改ページ |
| `**強調**` / `*斜体*` / `` `コード` `` / `[リンク](url)` | インライン装飾 |
| `｜漢字《かんじ》` | ルビ(青空文庫記法。`｜` は漢字列の前なら省略可) |

図版のパスは、原稿ファイルからの相対でも本のディレクトリからの相対でも解決される。

### 原稿ファイルのフロントマター

各ファイルの先頭に、そのファイル固有の指定を置ける。

```markdown
---
title: まえがき      # 章タイトルを見出しと別にしたいとき
type: front         # front / body / back
toc: false          # この章を目次に載せない
page_break: false   # 章の前で改ページしない
---
```

## 目次の作られ方

見出しは Word 組み込みの `Heading 1`〜`Heading 3` スタイルで出力し、スタイル定義に
`outlineLvl` を入れている。**KDPの変換エンジンとKindleの目次ジャンプはこれを見ている**ため、
見た目だけ大きくした文字は章として認識されない。

そのうえで、`toc.style` で目次の形を選ぶ。

- `link` — 見出しにブックマーク(`_TocNNNNN`)を打ち、目次からリンクする。電子書籍向け
- `field` — Wordの目次フィールド(` TOC \o "1-2" \h \z \u `)を置く。Wordで開いて
  フィールドを更新するとページ番号入りの目次になる。ペーパーパック向け
- `both` — 両方
- `none` — 目次を作らない

`depth` で目次に載せる階層を決める(`1` なら章のみ、`2` なら `##` まで)。
EPUB側では同じ見出しから `nav.xhtml`(EPUB3)と `toc.ncx`(EPUB2互換)の両方を生成する。

## 入稿前チェック

ビルド前に、KDPで差し戻されやすい点を検査する。エラーが1件でもあればビルドは走らない。

- **メタデータ** — タイトル200文字、内容紹介4000文字、キーワード7個、ISBNのチェックディジット
- **原稿** — 章に `#` 見出しがあるか、見出しレベルの飛び、1ファイルに章が複数ないか、
  書きかけのメモ(`TODO` / `FIXME` / `※要確認`)が残っていないか
- **目次** — 目次に載る見出しが存在するか
- **画像** — ファイルの有無、KDPが受け付ける形式か、5MB超、
  ペーパーバックで版面幅いっぱいにしたときに300dpiを下回らないか
- **表紙** — 幅1000px以上(1600px以上を推奨)、縦横比1:1.6前後、JPEG/TIFF

`--strict` を付けると警告もエラー扱いになる。CIではこちらを使うとよい。

## 出力物とKDPへの入稿

`build/<slug>/` に次が出る。

| ファイル | 用途 |
| --- | --- |
| `<slug>-ebook.docx` | 電子書籍としてKDPにアップロードする原稿 |
| `<slug>-print.docx` | ペーパーバックの原稿。Wordで開いて目次を更新してからPDF書き出し |
| `<slug>.epub` | KDP推奨形式。電子書籍はこちらを優先してよい |
| `<slug>-kdp-metadata.md` | KDPの「本の詳細」画面にコピペするメタデータ一式 |
| `build-manifest.json` | ビルド日時・統計・成果物・警告のサマリ |

ペーパーバックは、`-print.docx` をWordで開き、目次を右クリックして「フィールド更新」を
実行してからPDFに書き出す(KDPはPDF入稿が確実)。概算ページ数は
`build-manifest.json` の `estimated_print_pages` に入っているので、背幅や価格設定の目安に使える。

表紙画像はKDPの登録画面で個別にアップロードする。`book.yaml` の `cover` を設定すると、
EPUBに表紙ページが埋め込まれ、入稿前チェックの対象にもなる。

## 自動ビルド(GitHub Actions)

`.github/workflows/kdp-build.yml` が、`manuscripts/` や `scripts/kdp/` の変更を検知して
テスト → 入稿前チェック → ビルドを実行し、生成物をアーティファクトとして保存する。
Actionsタブから `KDP Build` を手動実行することもできる(対象の本と `--strict` を指定可能)。

## モジュール構成

| モジュール | 役割 |
| --- | --- |
| `config.py` | `book.yaml` の読み込みと検証、判型・余白の解決 |
| `mdparse.py` | Markdown原稿 → 中間表現(docx/EPUB共通) |
| `docx_builder.py` | 中間表現 → OOXML(WordprocessingML)→ .docx |
| `epub_builder.py` | 中間表現 → XHTML/OPF/NAV → .epub |
| `images.py` | 画像のピクセル数・解像度・形式の判定 |
| `preflight.py` | 入稿前チェック |

docxとEPUBの生成に外部ライブラリは使っていない(依存はPyYAMLのみ)。仕様どおりのXMLを
組み立ててZIPに詰めているだけなので、出力が思ったとおりにならないときは各ビルダを直接読める。

## テスト

```bash
python -m unittest discover -s tests -v
```

生成物が開けることだけでなく、見出しスタイル、ブックマークと目次リンクの対応、判型、
EPUBのマニフェスト整合性まで検証している。
