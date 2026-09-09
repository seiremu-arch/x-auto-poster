#!/usr/bin/env python3
"""books/<slug>/ の原稿から、字数レポート・通しMarkdown・EPUBを作る。

原稿は `books/<slug>/manuscript/*.md` にあり、並び順は `book.json` の `chapters` が持つ。
判断は持たない(何を書くかは `PLAN.md` と Vault のclaimノートにある)。ここがやるのは
数えることと、KDPに渡せる形に詰めることだけ。

    python scripts/build_book.py inner-voice             # 章ごとの字数
    python scripts/build_book.py inner-voice --markdown  # build/<slug>.md に1本化
    python scripts/build_book.py inner-voice --epub      # build/<slug>.epub
    python scripts/build_book.py inner-voice --check     # 芯の一文が3か所で一致しているか

Markdownは原稿で使う範囲だけを解釈する(見出し3段 / 段落 / 箇条書き / 番号リスト /
引用 / 水平線 / 強調 / コード)。表や画像は使わない前提なので、対応していない。
"""

import argparse
import html
import json
import re
import signal
import sys
import unicodedata
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOKS = ROOT / "books"

HEADING_RE = re.compile(r"^(#{1,3})\s+(.*)$")
UL_RE = re.compile(r"^[-*]\s+(.*)$")
OL_RE = re.compile(r"^\d+\.\s+(.*)$")
QUOTE_RE = re.compile(r"^>\s?(.*)$")
MARKUP_RE = re.compile(r"^(#{1,6}\s+|[-*]\s+|\d+\.\s+|>\s?)")
INLINE_RE = re.compile(r"[*`|]")


# --------------------------------------------------------------------------- 入力

def load_book(slug):
    book_dir = BOOKS / slug
    meta_path = book_dir / "book.json"
    if not meta_path.exists():
        raise SystemExit(f"{meta_path} がありません")
    meta = json.loads(meta_path.read_text(encoding="utf-8"))

    chapters = []
    for name in meta.get("chapters", []):
        path = book_dir / "manuscript" / name
        if not path.exists():
            continue  # 未執筆の章。飛ばして、レポートには「未」として出す
        chapters.append((name, path, path.read_text(encoding="utf-8")))
    return book_dir, meta, chapters


def chapter_title(text, fallback):
    for line in text.splitlines():
        match = HEADING_RE.match(line)
        if match and len(match.group(1)) == 1:
            return match.group(2).strip()
    return fallback


def count_chars(text):
    """本文の字数。記法と空白を落として数える(KDPの分量感に近づけるため)。"""
    body = []
    for line in text.splitlines():
        line = MARKUP_RE.sub("", line)
        body.append(INLINE_RE.sub("", line))
    return len(re.sub(r"\s", "", "".join(body)))


# --------------------------------------------------------------------------- Markdown → XHTML

def inline(text):
    out = html.escape(text, quote=False)
    out = re.sub(r"`([^`]+)`", r"<code>\1</code>", out)
    out = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", out)
    return out


def join_lines(lines):
    """日本語は行を詰めて繋ぐ。英数字どうしの境目にだけ空白を入れる。"""
    joined = ""
    for line in lines:
        line = line.strip()
        if not joined:
            joined = line
            continue
        if joined[-1].isascii() and joined[-1].isalnum() and line[:1].isascii() and line[:1].isalnum():
            joined += " "
        joined += line
    return joined


def blocks(text):
    """空行で区切ってブロックに分ける。"""
    current = []
    for line in text.splitlines():
        if line.strip():
            current.append(line)
        elif current:
            yield current
            current = []
    if current:
        yield current


def render_blocks(text, level=0):
    parts = []
    for block in blocks(text):
        first = block[0]

        match = HEADING_RE.match(first)
        if match:
            depth = len(match.group(1)) + level
            parts.append(f"<h{depth}>{inline(match.group(2).strip())}</h{depth}>")
            continue

        if all(line.strip() in ("---", "***") for line in block):
            parts.append("<hr/>")
            continue

        if all(QUOTE_RE.match(line) for line in block):
            inner = "\n".join(QUOTE_RE.match(line).group(1) for line in block)
            # 引用の中でも箇条書きや段落が使われるので、そのまま再帰させる
            parts.append("<blockquote>\n" + render_blocks(inner, level) + "\n</blockquote>")
            continue

        if all(UL_RE.match(line) for line in block):
            items = "".join(f"<li>{inline(UL_RE.match(line).group(1))}</li>" for line in block)
            parts.append(f"<ul>{items}</ul>")
            continue

        if all(OL_RE.match(line) for line in block):
            items = "".join(f"<li>{inline(OL_RE.match(line).group(1))}</li>" for line in block)
            parts.append(f"<ol>{items}</ol>")
            continue

        parts.append(f"<p>{inline(join_lines(block))}</p>")
    return "\n".join(parts)


# --------------------------------------------------------------------------- 出力

def build_markdown(meta, chapters, out_path):
    head = [f"# {meta['title']}", ""]
    if meta.get("subtitle"):
        head += [f"## {meta['subtitle']}", ""]
    head += [f"{meta.get('author', '')}", "", "---", ""]
    body = "\n\n".join(text.strip() for _, _, text in chapters)
    out_path.write_text("\n".join(head) + body + "\n", encoding="utf-8")
    return out_path


XHTML = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="{lang}" lang="{lang}">
<head><meta charset="utf-8"/><title>{title}</title>
<link rel="stylesheet" type="text/css" href="../style.css"/></head>
<body>
{body}
</body>
</html>
"""

CSS = """html { font-size: 100%; }
body { line-height: 1.8; margin: 0 1em; }
h1 { font-size: 1.4em; line-height: 1.5; margin: 2em 0 1.5em; font-weight: normal; }
h2 { font-size: 1.1em; margin: 2.5em 0 1em; }
h3 { font-size: 1em; margin: 2em 0 0.8em; }
p { margin: 0 0 1em; text-indent: 1em; }
li { margin: 0 0 0.5em; }
blockquote { margin: 1.5em 1em; padding-left: 0.8em; border-left: 2px solid #999; }
blockquote p { text-indent: 0; }
hr { border: 0; border-top: 1px solid #ccc; margin: 2em 4em; }
"""


def build_epub(meta, chapters, out_path):
    lang = meta.get("language", "ja")
    modified = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    docs = []
    for index, (name, _, text) in enumerate(chapters, start=1):
        title = chapter_title(text, name)
        docs.append((f"ch{index:02d}", title, XHTML.format(lang=lang, title=html.escape(title), body=render_blocks(text))))

    manifest = "\n".join(
        f'    <item id="{doc_id}" href="text/{doc_id}.xhtml" media-type="application/xhtml+xml"/>'
        for doc_id, _, _ in docs
    )
    spine = "\n".join(f'    <itemref idref="{doc_id}"/>' for doc_id, _, _ in docs)
    title = html.escape(meta["title"])
    subtitle = meta.get("subtitle")
    subtitle_tags = ""
    if subtitle:
        subtitle_tags = (
            f'\n    <dc:title id="sub">{html.escape(subtitle)}</dc:title>'
            '\n    <meta refines="#sub" property="title-type">subtitle</meta>'
        )
    opf = f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid" xml:lang="{lang}">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="bookid">{html.escape(meta.get("identifier", "urn:uuid:0"))}</dc:identifier>
    <dc:title id="main">{title}</dc:title>
    <meta refines="#main" property="title-type">main</meta>{subtitle_tags}
    <dc:creator>{html.escape(meta.get("author", ""))}</dc:creator>
    <dc:language>{lang}</dc:language>
    <meta property="dcterms:modified">{modified}</meta>
  </metadata>
  <manifest>
    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
    <item id="css" href="style.css" media-type="text/css"/>
{manifest}
  </manifest>
  <spine>
{spine}
  </spine>
</package>
"""
    toc = "\n".join(
        f'      <li><a href="text/{doc_id}.xhtml">{html.escape(chapter)}</a></li>'
        for doc_id, chapter, _ in docs
    )
    nav = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="{lang}" lang="{lang}">
<head><meta charset="utf-8"/><title>目次</title></head>
<body>
  <nav epub:type="toc" id="toc">
    <h1>目次</h1>
    <ol>
{toc}
    </ol>
  </nav>
</body>
</html>
"""
    container = """<?xml version="1.0" encoding="utf-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles><rootfile full-path="OEBPS/package.opf" media-type="application/oebps-package+xml"/></rootfiles>
</container>
"""

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out_path, "w") as epub:
        # mimetypeは先頭に、無圧縮で置く(EPUBの決まり)
        epub.writestr(zipfile.ZipInfo("mimetype"), "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        epub.writestr("META-INF/container.xml", container, compress_type=zipfile.ZIP_DEFLATED)
        epub.writestr("OEBPS/package.opf", opf, compress_type=zipfile.ZIP_DEFLATED)
        epub.writestr("OEBPS/nav.xhtml", nav, compress_type=zipfile.ZIP_DEFLATED)
        epub.writestr("OEBPS/style.css", CSS, compress_type=zipfile.ZIP_DEFLATED)
        for doc_id, _, document in docs:
            epub.writestr(f"OEBPS/text/{doc_id}.xhtml", document, compress_type=zipfile.ZIP_DEFLATED)
    return out_path


# --------------------------------------------------------------------------- 芯の一文の一致

VAULT_NOTES = ROOT / "vault" / "10-notes"
MEMORY = ROOT / "vault" / "MEMORY.md"


def squeeze(text):
    return re.sub(r"\s", "", text)


def check_core(book_dir, meta):
    """芯の一文が PLAN.md / claimノート / MEMORY.md の3か所に同じ文で現れるかを見る。

    片方だけ動かすと、判断の置き場所の分担(Vault `3f64e5ecd8`)が静かに破れる。
    人の注意で保つのをやめて、ここで落とす。
    """
    sentence = meta.get("core_sentence")
    if not sentence:
        return []
    needle = squeeze(sentence)

    targets = [("PLAN.md", book_dir / "PLAN.md"), ("MEMORY.md", MEMORY)]
    claim_id = meta.get("core_claim")
    if claim_id:
        found = sorted(VAULT_NOTES.glob(f"*claim-{claim_id}.md"))
        if not found:
            return [f"core_claim `{claim_id}` のノートが vault/10-notes にありません"]
        targets.append((found[0].name, found[0]))

    errors = []
    for label, path in targets:
        if not path.exists():
            errors.append(f"{label} がありません")
        elif needle not in squeeze(path.read_text(encoding="utf-8")):
            errors.append(f"{label} に芯の一文がありません: 「{sentence}」")
    return errors


# --------------------------------------------------------------------------- レポート

def width(text):
    """全角を2, 半角を1で数える(表の桁を揃えるため)。"""
    return sum(2 if unicodedata.east_asian_width(ch) in "WF" else 1 for ch in text)


def report(meta, chapters, written):
    total = 0
    print(f"{meta['title']} — {len(written)}/{len(meta.get('chapters', []))} 章")
    print()
    for name, _, text in chapters:
        chars = count_chars(text)
        total += chars
        title = chapter_title(text, name)
        print(f"  {title}{' ' * max(1, 34 - width(title))}{chars:>6,} 字")
    for name in meta.get("chapters", []):
        if name not in written:
            print(f"  ({name}){' ' * max(1, 32 - width(name))}      未")
    target = meta.get("target_chars")
    print()
    print(f"  合計 {total:,} 字", end="")
    if target:
        print(f" / 目安 {target:,} 字 ({total / target * 100:.0f}%)")
    else:
        print()
    return total


# --------------------------------------------------------------------------- main

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("slug", help="books/ の下のディレクトリ名(例: inner-voice)")
    parser.add_argument("--markdown", action="store_true", help="通しMarkdownを書き出す")
    parser.add_argument("--epub", action="store_true", help="EPUBを書き出す")
    parser.add_argument("--check", action="store_true", help="芯の一文の一致を検証する(食い違ったら終了コード1)")
    args = parser.parse_args(argv)

    book_dir, meta, chapters = load_book(args.slug)
    if not chapters:
        raise SystemExit(f"{book_dir / 'manuscript'} に原稿がありません")

    written = {name for name, _, _ in chapters}
    report(meta, chapters, written)

    build_dir = book_dir / "build"
    if args.markdown:
        build_dir.mkdir(parents=True, exist_ok=True)
        path = build_markdown(meta, chapters, build_dir / f"{args.slug}.md")
        print(f"\n  → {path.relative_to(ROOT)}")
    if args.epub:
        path = build_epub(meta, chapters, build_dir / f"{args.slug}.epub")
        print(f"  → {path.relative_to(ROOT)}")
    if args.check:
        errors = check_core(book_dir, meta)
        print()
        for error in errors:
            print(f"  ERROR {error}", file=sys.stderr)
        if errors:
            return 1
        print(f"  芯の一文は3か所で一致しています: 「{meta['core_sentence']}」")
    return 0


if __name__ == "__main__":
    # `| head` で閉じられたときに落ちないようにする
    if hasattr(signal, "SIGPIPE"):
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    sys.exit(main())
