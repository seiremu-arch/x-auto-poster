#!/usr/bin/env python3
"""『最後の帳簿1 三つに分けられた遺産』を KDP 入稿用の縦書き EPUB3 に組む。

    python3 writing/last-ledger/build_epub.py               # 縦書き（KDP日本語版）
    python3 writing/last-ledger/build_epub.py --horizontal  # 横書き
    python3 writing/last-ledger/build_epub.py --english     # 英語版（manuscript-en/）

manuscript/*.md を読み、book/ に .epub と統合 .md を出力する。
著者名などは METADATA を書き換える。
"""
import html, pathlib, re, sys, zipfile, datetime, uuid

ROOT = pathlib.Path(__file__).parent
OUT  = ROOT / "book"

# 縦書き（漢数字）が既定。--horizontal で横書き（算用数字）版、
# --english で英語版（横書き・左開き）を作る。
ENGLISH  = "--english" in sys.argv
VERTICAL = not ENGLISH and "--horizontal" not in sys.argv
if ENGLISH:
    SRC = ROOT / "manuscript-en"
elif VERTICAL:
    SRC = ROOT / "build" / "vertical"
else:
    SRC = ROOT / "manuscript"
SUFFIX = "" if VERTICAL else "_横書き"
BASENAME = "最後の帳簿1_三つに分けられた遺産"

METADATA = {
    "title":     "最後の帳簿　三つに分けられた遺産",
    "series":    "最後の帳簿",
    "series_no": 1,
    "author":    "Kazu A. Suzuki",
    "author_file_as": "Suzuki, Kazu A.",   # EPUBの並べ替え用（姓, 名）
    "publisher": "",                     # 個人出版なら空でよい
    "language":  "ja",
    "uuid":      "urn:uuid:" + str(uuid.uuid5(uuid.NAMESPACE_URL,
                  "last-ledger-vol1-mitsu-ni-wakerareta-isan")),
}

if ENGLISH:
    METADATA.update({
        "title":     "The Last Ledger: An Estate in Three Parts",
        "subtitle":  "An Estate in Three Parts",
        "series":    "The Last Ledger",
        "language":  "en",
        "original":  "最後の帳簿　三つに分けられた遺産",
        "uuid":      "urn:uuid:" + str(uuid.uuid5(uuid.NAMESPACE_URL,
                      "last-ledger-vol1-an-estate-in-three-parts-en")),
    })
    SUFFIX = ""
    BASENAME = "The_Last_Ledger_1_An_Estate_in_Three_Parts"
LANG = METADATA["language"]

ORDER = [("prologue", "Prologue" if ENGLISH else "プロローグ")] + \
        [("ch%02d" % i, None) for i in range(1, 28)] + \
        [("epilogue", "Epilogue" if ENGLISH else "エピローグ")]

WMODE = """html {
  -epub-writing-mode: vertical-rl;
  -webkit-writing-mode: vertical-rl;
  writing-mode: vertical-rl;
}""" if VERTICAL else """html {
  -epub-writing-mode: horizontal-tb;
  -webkit-writing-mode: horizontal-tb;
  writing-mode: horizontal-tb;
}"""

CSS = """@charset "UTF-8";
""" + WMODE + """
body {
  font-family: "游明朝", "YuMincho", "Hiragino Mincho ProN", serif;
  line-height: 1.75;
  margin: 0;
  padding: 0;
  text-align: justify;
}
h1 {
  font-size: 1.3em;
  font-weight: normal;
  margin: 3em 0 2.5em 0;
  line-height: 1.6;
}
p {
  margin: 0;
  text-indent: 0;
}
p.sep {
  margin: 1.6em 0;
  text-align: center;
  text-indent: 0;
}
p.cite {
  margin: 1.2em 0;
  text-indent: 0;
}
p.blank { margin: 1em 0; }
.tobira {
  margin: 0;
  text-align: center;
}
.tobira h1 { font-size: 1.8em; margin: 6em 0 0 0; }
.tobira .series { font-size: 0.9em; margin: 0 3em 0 0; }
.tobira .author { font-size: 1.0em; margin: 4em 0 0 0; }
.colophon { font-size: 0.9em; line-height: 2.0; }
.latin {
  writing-mode: horizontal-tb;
  -epub-writing-mode: horizontal-tb;
  -webkit-writing-mode: horizontal-tb;
  display: inline-block;
  text-orientation: mixed;
  font-family: "Times New Roman", serif;
}
nav ol { list-style: none; padding: 0; margin: 0; }
nav li { margin: 0.5em 0; }
"""

if ENGLISH:
    CSS = """@charset "UTF-8";
""" + WMODE + """
body {
  font-family: Georgia, "Times New Roman", serif;
  line-height: 1.5;
  margin: 0;
  padding: 0;
  text-align: justify;
  hyphens: auto;
  -webkit-hyphens: auto;
}
h1 {
  font-size: 1.3em;
  font-weight: normal;
  text-align: center;
  margin: 3em 0 2em 0;
  line-height: 1.4;
}
p {
  margin: 0;
  text-indent: 1.2em;
}
p.first { text-indent: 0; }
p.sep {
  margin: 1.2em 0;
  text-align: center;
  text-indent: 0;
}
p.cite {
  margin: 0.6em 0 0.6em 2em;
  text-indent: 0;
  text-align: left;
}
.tobira { margin: 0; text-align: center; }
.tobira h1 { font-size: 1.8em; margin: 5em 0 0.5em 0; }
.tobira .series { font-size: 0.9em; margin: 0; text-indent: 0; letter-spacing: 0.1em; }
.tobira .author { font-size: 1.0em; margin: 4em 0 0 0; text-indent: 0; }
.colophon p { text-indent: 0; margin: 0 0 0.8em 0; font-size: 0.9em; }
nav ol { list-style: none; padding: 0; margin: 0; }
nav li { margin: 0.5em 0; }
"""

SEP_RE  = re.compile(r'^　+※\s*$')
BOLD_RE = re.compile(r'\*\*(.+?)\*\*')
ITAL_RE = re.compile(r'(?<![*\w])\*(?!\s)(.+?)(?<!\s)\*(?![*\w])')


def esc(t):
    return html.escape(t, quote=False)


def md_to_xhtml_body(md):
    """本文マークダウンを XHTML の断片にする。"""
    out, title = [], None
    after_break = True          # 英語版：章頭と※の直後の段落は字下げしない
    for raw in md.split("\n"):
        line = raw.rstrip()
        if not line:
            continue
        if line.startswith("# "):
            title = line[2:].strip()
            out.append("<h1>%s</h1>" % esc(title))
            after_break = True
            continue
        if SEP_RE.match(line):
            out.append('<p class="sep">※</p>')
            after_break = True
            continue
        cls = "cite" if line.startswith("　　") else None
        body = esc(line)
        body = BOLD_RE.sub(lambda m: "<strong>%s</strong>" % m.group(1), body)
        if ENGLISH:
            body = ITAL_RE.sub(lambda m: "<em>%s</em>" % m.group(1), body)
            if cls is None and after_break:
                cls = "first"
            after_break = False
        out.append('<p class="%s">%s</p>' % (cls, body) if cls else "<p>%s</p>" % body)
    return title, "\n".join(out)


def xhtml_page(title, body, cls=None):
    b = ' class="%s"' % cls if cls else ""
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<!DOCTYPE html>\n'
            '<html xmlns="http://www.w3.org/1999/xhtml" '
            'xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="%s" lang="%s">\n'
            '<head>\n<meta charset="UTF-8"/>\n<title>%s</title>\n'
            '<link rel="stylesheet" type="text/css" href="style.css"/>\n</head>\n'
            '<body%s>\n%s\n</body>\n</html>\n' % (LANG, LANG, esc(title), b, body))


def build():
    OUT.mkdir(exist_ok=True)
    m = METADATA
    chapters, combined = [], []

    for stem, forced in ORDER:
        md = (SRC / (stem + ".md")).read_text(encoding="utf-8")
        title, body = md_to_xhtml_body(md)
        title = forced or title or stem
        chapters.append((stem, title, xhtml_page(title, body)))
        combined.append(md.rstrip() + "\n")

    # --- 統合原稿（テキストで読み返す用） ---
    if ENGLISH:
        head = "# %s\n\n%s, Book %d\n\n%s\n\n" % (m["title"], m["series"], m["series_no"], m["author"])
    else:
        head = "# %s\n\n%s　第%d巻\n\n%s\n\n" % (m["title"], m["series"], m["series_no"], m["author"])
    (OUT / ("%s%s.md" % (BASENAME, SUFFIX))).write_text(
        head + "\n\n".join(combined), encoding="utf-8")

    # --- 扉・奥付 ---
    year = datetime.date.today().year
    if ENGLISH:
        tobira = xhtml_page(m["title"],
            '<h1>%s</h1>\n<p class="series">%s &#183; Book One</p>\n'
            '<p class="author">%s</p>'
            % (esc(m["subtitle"]), esc(m["series"].upper()), esc(m["author"])), "tobira")
        colo = xhtml_page("Copyright",
            '<p><em>%s</em></p>\n<p>%s, Book %d</p>\n'
            '<p>Copyright &#169; %d %s. All rights reserved.</p>\n'
            '<p>Originally published in Japanese as <span lang="ja" xml:lang="ja">%s</span>.</p>\n'
            '<p>This is a work of fiction. Names, characters, businesses, places and events '
            'are the products of the author&#8217;s imagination. Any resemblance to actual '
            'persons, living or dead, or to actual events is purely coincidental.</p>\n'
            % (esc(m["title"]), esc(m["series"]), m["series_no"], year, esc(m["author"]),
               esc(m["original"])), "colophon")
    else:
        tobira = xhtml_page(m["title"],
            '<p class="series">%s　第%d巻</p>\n<h1>%s</h1>\n'
            '<p class="author"><span class="latin">%s</span></p>'
            % (esc(m["series"]), m["series_no"], esc(m["title"]), esc(m["author"])), "tobira")
        colo = xhtml_page("奥付",
            '<h1>奥付</h1>\n<p>%s</p>\n<p>%s　第%d巻</p>\n<p>&#160;</p>\n'
            '<p>著者　<span class="latin">%s</span></p>\n<p>発行　%d年</p>\n<p>&#160;</p>\n'
            '<p>本作品はフィクションです。実在の人物・団体・地名とは関係ありません。</p>\n'
            % (esc(m["title"]), esc(m["series"]), m["series_no"], esc(m["author"]), year), "colophon")

    # --- 目次 ---
    TOC = "Contents" if ENGLISH else "目次"
    items = "\n".join('<li><a href="%s.xhtml">%s</a></li>' % (s, esc(t))
                      for s, t, _ in chapters)
    nav = ('<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE html>\n'
           '<html xmlns="http://www.w3.org/1999/xhtml" '
           'xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="%s" lang="%s">\n'
           '<head><meta charset="UTF-8"/><title>%s</title>'
           '<link rel="stylesheet" type="text/css" href="style.css"/></head>\n<body>\n'
           '<nav epub:type="toc" id="toc"><h1>%s</h1>\n<ol>\n%s\n</ol></nav>\n'
           '</body>\n</html>\n' % (LANG, LANG, TOC, TOC, items))

    navpoints = "\n".join(
        '<navPoint id="n%d" playOrder="%d"><navLabel><text>%s</text></navLabel>'
        '<content src="%s.xhtml"/></navPoint>' % (i, i, esc(t), s)
        for i, (s, t, _) in enumerate(chapters, 1))
    ncx = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">\n'
           '<head><meta name="dtb:uid" content="%s"/></head>\n'
           '<docTitle><text>%s</text></docTitle>\n<navMap>\n%s\n</navMap>\n</ncx>\n'
           % (m["uuid"], esc(m["title"]), navpoints))

    manifest = ['<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>',
                '<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>',
                '<item id="css" href="style.css" media-type="text/css"/>',
                '<item id="tobira" href="tobira.xhtml" media-type="application/xhtml+xml"/>',
                '<item id="colophon" href="colophon.xhtml" media-type="application/xhtml+xml"/>']
    spine = ['<itemref idref="tobira"/>', '<itemref idref="nav"/>']
    for s, _, _ in chapters:
        manifest.append('<item id="%s" href="%s.xhtml" media-type="application/xhtml+xml"/>' % (s, s))
        spine.append('<itemref idref="%s"/>' % s)
    spine.append('<itemref idref="colophon"/>')

    opf = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<package xmlns="http://www.idpf.org/2007/opf" version="3.0" '
           'unique-identifier="bookid" xml:lang="%s" '
           'prefix="rendition: http://www.idpf.org/vocab/rendition/#">\n'
           '<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">\n'
           '<dc:identifier id="bookid">%s</dc:identifier>\n'
           '<dc:title>%s</dc:title>\n'
           '<dc:creator id="creator">%s</dc:creator>\n'
           '<meta refines="#creator" property="role" scheme="marc:relators">aut</meta>\n'
           '<meta refines="#creator" property="file-as">%s</meta>\n'
           '<dc:language>%s</dc:language>\n'
           '<dc:date>%s</dc:date>\n'
           '<meta property="dcterms:modified">%sT00:00:00Z</meta>\n'
           '<meta property="rendition:layout">reflowable</meta>\n'
           '<meta property="rendition:spread">auto</meta>\n'
           '<meta name="primary-writing-mode" content="%s"/>\n'
           '<meta name="book-type" content="comic"/>\n'
           '</metadata>\n<manifest>\n%s\n</manifest>\n'
           '<spine toc="ncx" page-progression-direction="%s">\n%s\n</spine>\n</package>\n'
           % (LANG, m["uuid"], esc(m["title"]), esc(m["author"]), esc(m["author_file_as"]),
              m["language"], datetime.date.today().isoformat(),
              datetime.date.today().isoformat(),
              "vertical-rl" if VERTICAL else "horizontal-tb",
              "\n".join(manifest), "rtl" if VERTICAL else "ltr", "\n".join(spine)))
    # 小説なので book-type は付けない（コミック扱いになるのを避ける）
    opf = opf.replace('<meta name="book-type" content="comic"/>\n', "")

    container = ('<?xml version="1.0" encoding="UTF-8"?>\n'
                 '<container version="1.0" '
                 'xmlns="urn:oasis:names:tc:opendocument:xmlns:container">\n'
                 '<rootfiles><rootfile full-path="OEBPS/content.opf" '
                 'media-type="application/oebps-package+xml"/></rootfiles>\n</container>\n')

    epub = OUT / ("%s%s.epub" % (BASENAME, SUFFIX))
    with zipfile.ZipFile(epub, "w") as z:
        z.writestr(zipfile.ZipInfo("mimetype"), "application/epub+zip",
                   compress_type=zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml", container, zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/content.opf", opf, zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/toc.ncx", ncx, zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/nav.xhtml", nav, zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/style.css", CSS, zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/tobira.xhtml", tobira, zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/colophon.xhtml", colo, zipfile.ZIP_DEFLATED)
        for s, _, page in chapters:
            z.writestr("OEBPS/%s.xhtml" % s, page, zipfile.ZIP_DEFLATED)

    if ENGLISH:
        words = sum(len((SRC / (s + ".md")).read_text(encoding="utf-8").split())
                    for s, _, _ in chapters)
        print("Edition: English (horizontal, left-to-right)")
        print("EPUB:", epub.name, "(%.1f KB)" % (epub.stat().st_size / 1024))
        print("Units:", len(chapters), "/ about", format(words, ","), "words")
        return
    chars = sum(len(re.sub(r"\s", "", (SRC / (s + ".md")).read_text(encoding="utf-8")))
                for s, _, _ in chapters)
    print("組み方向:", "縦書き（漢数字）" if VERTICAL else "横書き（算用数字）")
    print("EPUB:", epub.name, "(%.1f KB)" % (epub.stat().st_size / 1024))
    print("章数:", len(chapters), "／本文", format(chars, ","), "字")


if __name__ == "__main__":
    build()
