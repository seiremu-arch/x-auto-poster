#!/usr/bin/env python3
"""連作短編集のKindle用EPUB3を組み立てる。

使い方:
    python3 book/tools/build_epub.py vol1
    python3 book/tools/build_epub.py vol2
    python3 book/tools/build_epub.py          # 全巻をまとめて出力

book/volN/stories/ の中の NN_*.txt を番号順に読み、縦書きのEPUB3として
book/dist/ に出力する。各テキストは一行目を題、以降を本文とし、
「一」「二」などの数字だけの行を節の区切りとして扱う。

外部ライブラリは使わない。標準ライブラリのzipfileでEPUBを直接組む。
"""

import html
import re
import sys
import unicodedata
import zipfile
from pathlib import Path

AUTHOR = "Kazu A. Suzuki"

VOLUMES = {
    "vol1": {
        "title": "夢編集局",
        "subtitle": "十二の夜",
        "uuid": "urn:uuid:8f2c1a64-3d5e-4b90-a7c1-000000000001",
        "lang": "ja",
        "vertical": True,
    },
    "vol2": {
        "title": "均し",
        "subtitle": "夢編集局 第二集",
        "uuid": "urn:uuid:8f2c1a64-3d5e-4b90-a7c1-000000000002",
        "lang": "ja",
        "vertical": True,
    },
    "en1": {
        "title": "The Dream Editing Bureau",
        "subtitle": "Twelve Nights",
        "uuid": "urn:uuid:8f2c1a64-3d5e-4b90-a7c1-00000000e001",
        "lang": "en",
        "vertical": False,
    },
    "en2": {
        "title": "The Levelling",
        "subtitle": "The Dream Editing Bureau, Book Two",
        "uuid": "urn:uuid:8f2c1a64-3d5e-4b90-a7c1-00000000e002",
        "lang": "en",
        "vertical": False,
    },
    "de1": {
        "title": "Das Traumamt",
        "subtitle": "Zwölf Nächte",
        "uuid": "urn:uuid:8f2c1a64-3d5e-4b90-a7c1-00000000d001",
        "lang": "de",
        "vertical": False,
    },
    "de2": {
        "title": "Die Angleichung",
        "subtitle": "Das Traumamt, Band Zwei",
        "uuid": "urn:uuid:8f2c1a64-3d5e-4b90-a7c1-00000000d002",
        "lang": "de",
        "vertical": False,
    },
    "es1": {
        "title": "La Oficina de Sueños",
        "subtitle": "Doce noches",
        "uuid": "urn:uuid:8f2c1a64-3d5e-4b90-a7c1-00000000s001",
        "lang": "es",
        "vertical": False,
    },
    "es2": {
        "title": "La Nivelación",
        "subtitle": "La Oficina de Sueños, Libro Dos",
        "uuid": "urn:uuid:8f2c1a64-3d5e-4b90-a7c1-00000000s002",
        "lang": "es",
        "vertical": False,
    },
    "fr1": {
        "title": "Le Bureau des Rêves",
        "subtitle": "Douze nuits",
        "uuid": "urn:uuid:8f2c1a64-3d5e-4b90-a7c1-00000000f001",
        "lang": "fr",
        "vertical": False,
    },
    "fr2": {
        "title": "Le Nivellement",
        "subtitle": "Le Bureau des Rêves, Livre Deux",
        "uuid": "urn:uuid:8f2c1a64-3d5e-4b90-a7c1-00000000f002",
        "lang": "fr",
        "vertical": False,
    },
}

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"

SECTION_RE = re.compile(r"^(?:[一二三四五六七八九十]+|[IVXLC]+)$")

def stylesheet(vertical: bool) -> str:
    """巻ごとの組み方向に合わせたCSSを返す。"""
    if vertical:
        flow = """html {
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
.front h1 { letter-spacing: 0.5em; }
.front p { margin: 0 1.2em 0 0; }"""
    else:
        # 英語版は横組み。段落は字下げで繋ぎ、節の直後だけ字下げを外す
        flow = """html {
  line-height: 1.55;
}
body {
  font-family: "Iowan Old Style", "Palatino", Georgia, serif;
  margin: 0;
  padding: 0 1.2em;
  text-align: left;
}
h1 {
  font-size: 1.5em;
  font-weight: normal;
  letter-spacing: 0.04em;
  margin: 2.2em 0 1.6em;
  page-break-before: always;
}
h2 {
  font-size: 0.95em;
  font-weight: normal;
  letter-spacing: 0.22em;
  text-align: center;
  margin: 2.4em 0 1.4em;
}
p {
  margin: 0;
  text-indent: 1.25em;
}
h1 + p, h2 + p { text-indent: 0; }
.front { text-align: center; }
.front h1 { margin-top: 4em; page-break-before: avoid; }
.front p { text-indent: 0; margin: 0.8em 0; }"""
    return '@charset "UTF-8";\n' + flow + '\n'



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


def story_xhtml(story: dict, meta: dict) -> str:
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<html xmlns="http://www.w3.org/1999/xhtml" '
        'xmlns:epub="http://www.idpf.org/2007/ops" '
        f'xml:lang="{meta["lang"]}" lang="{meta["lang"]}">',
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


def front_xhtml(stories: list, meta: dict) -> str:
    total = sum(s["chars"] for s in stories)
    counted = {
        "ja": f"全{len(stories)}話　約{total:,}字",
        "en": f"{len(stories)} stories",
        "de": f"{len(stories)} Erzählungen",
        "es": f"{len(stories)} relatos",
        "fr": f"{len(stories)} nouvelles",
    }[meta["lang"]]
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<html xmlns="http://www.w3.org/1999/xhtml" '
        f'xml:lang="{meta["lang"]}" lang="{meta["lang"]}">',
        "<head>",
        f"<title>{html.escape(meta['title'])}</title>",
        '<meta charset="UTF-8"/>',
        '<link rel="stylesheet" type="text/css" href="style.css"/>',
        "</head>",
        '<body class="front">',
        f"<h1>{html.escape(meta['title'])}</h1>",
        f"<p>{html.escape(meta['subtitle'])}</p>",
        f"<p>{html.escape(AUTHOR)}</p>",
        f"<p>{counted}</p>",
        "</body>",
        "</html>",
    ]
    return "\n".join(lines)


def nav_xhtml(stories: list, meta: dict) -> str:
    nav_label = {"ja": "目次", "en": "Contents",
                 "de": "Inhalt", "es": "Índice",
                 "fr": "Sommaire"}[meta["lang"]]
    items = "\n".join(
        f'    <li><a href="p{i:02d}.xhtml">{html.escape(s["title"])}</a></li>'
        for i, s in enumerate(stories, start=1)
    )
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml"
      xmlns:epub="http://www.idpf.org/2007/ops"
      xml:lang="{meta["lang"]}" lang="{meta["lang"]}">
<head>
<title>{nav_label}</title>
<meta charset="UTF-8"/>
<link rel="stylesheet" type="text/css" href="style.css"/>
</head>
<body>
<nav epub:type="toc" id="toc">
<h1>{nav_label}</h1>
<ol>
{items}
</ol>
</nav>
</body>
</html>'''


def opf(stories: list, meta: dict) -> str:
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
         unique-identifier="bookid" xml:lang="{meta["lang"]}"
         prefix="rendition: http://www.idpf.org/vocab/rendition/#">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="bookid">{meta['uuid']}</dc:identifier>
    <dc:title>{html.escape(meta['title'])}</dc:title>
    <dc:creator>{html.escape(AUTHOR)}</dc:creator>
    <dc:language>{meta["lang"]}</dc:language>
    <meta property="rendition:layout">reflowable</meta>
    <meta property="rendition:spread">auto</meta>
    <meta property="ibooks:binding" refines="#bookid">true</meta>
  </metadata>
  <manifest>
    {nl.join(manifest)}
  </manifest>
  <spine page-progression-direction="{'rtl' if meta['vertical'] else 'ltr'}">
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


def build(vol: str) -> None:
    meta = VOLUMES[vol]
    stories_dir = ROOT / vol / "stories"
    paths = sorted(stories_dir.glob("[0-9][0-9]_*.txt"))
    if not paths:
        print(f"[{vol}] 本文がまだありません: {stories_dir}")
        return

    stories = [parse_story(p) for p in paths]
    DIST.mkdir(parents=True, exist_ok=True)
    out = DIST / f"{meta['title']}.epub"

    with zipfile.ZipFile(out, "w") as z:
        # mimetypeは非圧縮で先頭に置くことがEPUBの規格上の要件
        z.writestr(
            zipfile.ZipInfo("mimetype"),
            "application/epub+zip",
            compress_type=zipfile.ZIP_STORED,
        )
        z.writestr("META-INF/container.xml", CONTAINER, zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/style.css", stylesheet(meta["vertical"]), zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/content.opf", opf(stories, meta), zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/nav.xhtml", nav_xhtml(stories, meta), zipfile.ZIP_DEFLATED)
        z.writestr(
            "OEBPS/front.xhtml", front_xhtml(stories, meta), zipfile.ZIP_DEFLATED
        )
        for i, s in enumerate(stories, start=1):
            z.writestr(
                f"OEBPS/p{i:02d}.xhtml", story_xhtml(s, meta), zipfile.ZIP_DEFLATED
            )

    total = sum(s["chars"] for s in stories)
    print(f"[{vol}] 『{meta['title']}』 → {out}")
    print(f"  収録 {len(stories)}話　合計 {total:,}字　（目標 12話）")
    for i, s in enumerate(stories, start=1):
        print(f"   {i:2d}. {s['title']}　{s['chars']:,}字")

    # 縦書きで倒れる半角文字の混入を検出する。横組みの巻には関係がない
    if not meta["vertical"]:
        words = sum(len(t.split()) for s in stories for _, t in s["blocks"])
        print(f"  約 {words:,} words（横組みのため半角検査は省略）")
        return

    warned = False
    for s in stories:
        body = "".join(t for _, t in s["blocks"])
        bad = sorted({c for c in body if unicodedata.east_asian_width(c) in "NaH"
                      and not c.isspace()})
        if bad:
            warned = True
            print(f"   警告 [{s['title']}] 半角文字: {''.join(bad)}")
    if not warned:
        print("  半角文字の混入なし")


def main() -> None:
    args = sys.argv[1:]
    targets = args or list(VOLUMES)
    for vol in targets:
        if vol not in VOLUMES:
            raise SystemExit(f"不明な巻: {vol}（指定できるのは {', '.join(VOLUMES)}）")
        build(vol)


if __name__ == "__main__":
    main()
