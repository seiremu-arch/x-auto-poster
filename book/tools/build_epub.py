#!/usr/bin/env python3
"""連作短編集『夢編集局』のKindle用EPUB3を組み立てる。

使い方:
    python3 book/tools/build_epub.py

book/stories/ の中の NN_*.txt を番号順に読み、縦書きのEPUB3として
book/dist/ に出力する。各テキストは一行目を題、以降を本文とし、
「一」「二」などの数字だけの行を節の区切りとして扱う。

外部ライブラリは使わない。標準ライブラリのzipfileでEPUBを直接組む。
"""

import html
import re
import unicodedata
import zipfile
from pathlib import Path

BOOK_TITLE = "夢編集局"
BOOK_SUBTITLE = "十二の夜と、ひとつの選択"
AUTHOR = "著者名未設定"
LANG = "ja"
UUID = "urn:uuid:8f2c1a64-3d5e-4b90-a7c1-yumehenshukyoku"

ROOT = Path(__file__).resolve().parent.parent
STORIES = ROOT / "stories"
DIST = ROOT / "dist"

SECTION_RE = re.compile(r"^[一二三四五六七八九十]+$")

STYLE = """@charset "UTF-8";
html {
  -epub-writing-mode: vertical-rl;
  writing-mode: vertical-rl;
  line-height: 1.9;
}
body {
  font-family: "Hiragino Mincho ProN", "YuMincho", serif;
  margin: 0;
  padding: 0;
}
h1 {
  font-size: 1.4em;
  font-weight: normal;
  letter-spacing: 0.3em;
  margin: 0 2.5em 0 1.5em;
  page-break-before: always;
}
h2 {
  font-size: 1em;
  font-weight: normal;
  letter-spacing: 0.5em;
  margin: 0 3em 0 2em;
}
p {
  margin: 0;
  text-indent: 0;
  line-height: 1.9;
}
p.lead { margin-top: 2em; }
.front h1 { letter-spacing: 0.5em; }
.front p { margin: 0 1.2em 0 0; }
"""


def count_chars(text: str) -> int:
    return len(re.sub(r"\s", "", text))


def parse_story(path: Path) -> dict:
    lines = path.read_text(encoding="utf-8").split("\n")
    title = lines[0].strip()
    blocks = []
    for raw in lines[1:]:
        line = raw.strip()
        if not line:
            continue
        if SECTION_RE.fullmatch(line):
            blocks.append(("section", line))
        else:
            blocks.append(("para", line))
    return {
        "path": path,
        "title": title,
        "blocks": blocks,
        "chars": count_chars("".join(b[1] for b in blocks)),
    }


def story_xhtml(story: dict) -> str:
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<html xmlns="http://www.w3.org/1999/xhtml" '
        'xmlns:epub="http://www.idpf.org/2007/ops" '
        f'xml:lang="{LANG}" lang="{LANG}">',
        "<head>",
        f"<title>{html.escape(story['title'])}</title>",
        '<meta charset="UTF-8"/>',
        '<link rel="stylesheet" type="text/css" href="style.css"/>',
        "</head>",
        "<body>",
        f"<h1>{html.escape(story['title'])}</h1>",
    ]
    for kind, text in story["blocks"]:
        if kind == "section":
            parts.append(f"<h2>{html.escape(text)}</h2>")
        else:
            parts.append(f"<p>{html.escape(text)}</p>")
    parts += ["</body>", "</html>"]
    return "\n".join(parts)


def front_xhtml(stories: list) -> str:
    total = sum(s["chars"] for s in stories)
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<html xmlns="http://www.w3.org/1999/xhtml" '
        f'xml:lang="{LANG}" lang="{LANG}">',
        "<head>",
        f"<title>{html.escape(BOOK_TITLE)}</title>",
        '<meta charset="UTF-8"/>',
        '<link rel="stylesheet" type="text/css" href="style.css"/>',
        "</head>",
        '<body class="front">',
        f"<h1>{html.escape(BOOK_TITLE)}</h1>",
        f"<p>{html.escape(BOOK_SUBTITLE)}</p>",
        f"<p>{html.escape(AUTHOR)}</p>",
        f"<p>全{len(stories)}話　約{total:,}字</p>",
        "</body>",
        "</html>",
    ]
    return "\n".join(lines)


def nav_xhtml(stories: list) -> str:
    items = "\n".join(
        f'    <li><a href="p{i:02d}.xhtml">{html.escape(s["title"])}</a></li>'
        for i, s in enumerate(stories, start=1)
    )
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml"
      xmlns:epub="http://www.idpf.org/2007/ops"
      xml:lang="{LANG}" lang="{LANG}">
<head>
<title>目次</title>
<meta charset="UTF-8"/>
<link rel="stylesheet" type="text/css" href="style.css"/>
</head>
<body>
<nav epub:type="toc" id="toc">
<h1>目次</h1>
<ol>
{items}
</ol>
</nav>
</body>
</html>'''


def opf(stories: list) -> str:
    manifest = [
        '<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" '
        'properties="nav"/>',
        '<item id="style" href="style.css" media-type="text/css"/>',
        '<item id="front" href="front.xhtml" media-type="application/xhtml+xml"/>',
    ]
    spine = ['<itemref idref="front"/>', '<itemref idref="nav"/>']
    for i, _ in enumerate(stories, start=1):
        manifest.append(
            f'<item id="p{i:02d}" href="p{i:02d}.xhtml" '
            'media-type="application/xhtml+xml"/>'
        )
        spine.append(f'<itemref idref="p{i:02d}"/>')
    nl = "\n    "
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0"
         unique-identifier="bookid" xml:lang="{LANG}"
         prefix="rendition: http://www.idpf.org/vocab/rendition/#">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="bookid">{UUID}</dc:identifier>
    <dc:title>{html.escape(BOOK_TITLE)}</dc:title>
    <dc:creator>{html.escape(AUTHOR)}</dc:creator>
    <dc:language>{LANG}</dc:language>
    <meta property="rendition:layout">reflowable</meta>
    <meta property="rendition:spread">auto</meta>
    <meta property="ibooks:binding" refines="#bookid">true</meta>
  </metadata>
  <manifest>
    {nl.join(manifest)}
  </manifest>
  <spine page-progression-direction="rtl">
    {nl.join(spine)}
  </spine>
</package>'''


CONTAINER = '''<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0"
           xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf"
              media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>'''


def main() -> None:
    paths = sorted(STORIES.glob("[0-9][0-9]_*.txt"))
    if not paths:
        raise SystemExit(f"本文が見つかりません: {STORIES}")

    stories = [parse_story(p) for p in paths]
    DIST.mkdir(parents=True, exist_ok=True)
    out = DIST / f"{BOOK_TITLE}.epub"

    with zipfile.ZipFile(out, "w") as z:
        # mimetypeは非圧縮で先頭に置くことがEPUBの規格上の要件
        z.writestr(
            zipfile.ZipInfo("mimetype"),
            "application/epub+zip",
            compress_type=zipfile.ZIP_STORED,
        )
        z.writestr("META-INF/container.xml", CONTAINER, zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/style.css", STYLE, zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/content.opf", opf(stories), zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/nav.xhtml", nav_xhtml(stories), zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/front.xhtml", front_xhtml(stories), zipfile.ZIP_DEFLATED)
        for i, s in enumerate(stories, start=1):
            z.writestr(
                f"OEBPS/p{i:02d}.xhtml", story_xhtml(s), zipfile.ZIP_DEFLATED
            )

    total = sum(s["chars"] for s in stories)
    print(f"出力: {out}")
    print(f"収録: {len(stories)}話　合計 {total:,}字")
    for i, s in enumerate(stories, start=1):
        print(f"  {i:2d}. {s['title']}　{s['chars']:,}字")

    # 縦書きで倒れる半角文字の混入を検出する
    warned = False
    for s in stories:
        body = "".join(t for _, t in s["blocks"])
        bad = sorted({c for c in body if unicodedata.east_asian_width(c) in "NaH"
                      and not c.isspace()})
        if bad:
            warned = True
            print(f"  警告 [{s['title']}] 半角文字: {''.join(bad)}")
    if not warned:
        print("半角文字の混入なし")


if __name__ == "__main__":
    main()
