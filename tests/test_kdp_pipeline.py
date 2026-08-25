"""KDP制作パイプラインのテスト。

    python -m unittest discover -s tests -v

生成物(docx / EPUB)は「開けること」だけでなく、KDPで実際に効いてくる点
(見出しスタイル、ブックマークと目次リンクの対応、判型、EPUBのマニフェスト
整合性)まで検証する。
"""

from __future__ import annotations

import re
import struct
import sys
import tempfile
import unittest
import zipfile
import zlib
from pathlib import Path
from xml.etree import ElementTree as ET

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from kdp import preflight  # noqa: E402
from kdp.config import BookConfig, ConfigError, mm_to_twips  # noqa: E402
from kdp.docx_builder import build_docx  # noqa: E402
from kdp.epub_builder import build_epub  # noqa: E402
from kdp.mdparse import (  # noqa: E402
    ImageBlock,
    ListBlock,
    Ruby,
    parse_blocks,
    parse_file,
    parse_manuscript,
)

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
OPF = "{http://www.idpf.org/2007/opf}"
XHTML = "{http://www.w3.org/1999/xhtml}"

SAMPLE_BOOK = REPO_ROOT / "manuscripts" / "sample-book"


def write_png(path: Path, width: int = 1200, height: int = 800) -> None:
    """テスト用の単色PNGを標準ライブラリだけで作る。"""

    def chunk(tag: bytes, data: bytes) -> bytes:
        return (
            struct.pack(">I", len(data))
            + tag
            + data
            + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        )

    raw = b"".join(b"\x00" + b"\xc8\xd2\xdc" * width for _ in range(height))
    path.write_bytes(
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
        + chunk(b"pHYs", struct.pack(">IIB", 11811, 11811, 1))  # 300dpi
        + chunk(b"IDAT", zlib.compress(raw, 9))
        + chunk(b"IEND", b"")
    )


def make_book(tmp: Path, *, extra_yaml: str = "", chapters: dict[str, str] | None = None) -> Path:
    """テスト用の最小構成の本を作る。"""
    root = tmp / "book"
    (root / "manuscript").mkdir(parents=True)
    (root / "assets").mkdir(parents=True)
    (root / "book.yaml").write_text(
        "slug: test-book\n"
        "title: テストの本\n"
        "subtitle: サブタイトル\n"
        "author: 著者名\n"
        "publisher: テスト出版\n"
        "published: 2026-01-01\n"
        "description: テスト用の説明文。\n"
        "keywords: [テスト, 自動化]\n" + extra_yaml,
        encoding="utf-8",
    )
    chapters = chapters or {
        "01-first.md": (
            "# 第1章　はじまり\n\n"
            "本文の｜段落《だんらく》です。**強調**と[リンク](https://example.com)。\n\n"
            "## 節のみだし\n\n"
            "- 箇条書き1\n- 箇条書き2\n\n"
            "```python\nprint(1)\n```\n"
        ),
        "02-second.md": "# 第2章　つづき\n\n二章目の本文。\n\n### 深い見出し\n\nさらに本文。\n",
    }
    for name, body in chapters.items():
        (root / "manuscript" / name).write_text(body, encoding="utf-8")
    return root


def load(root: Path):
    book = BookConfig.load(root)
    return book, parse_manuscript(book.manuscript_files())


# --------------------------------------------------------------------------- 設定


class ConfigTest(unittest.TestCase):
    def test_sample_book_loads(self) -> None:
        book = BookConfig.load(SAMPLE_BOOK)
        self.assertEqual(book.slug, "kdp-pipeline-guide")
        self.assertTrue(book.manuscript_files())
        self.assertEqual(book.print_.toc.style, "field")
        self.assertEqual(book.ebook.toc.style, "link")

    def test_trim_sizes(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = make_book(Path(td), extra_yaml="print:\n  trim: a5\n")
            book = BookConfig.load(root)
            self.assertAlmostEqual(book.print_.width_mm, 148.0)
            self.assertAlmostEqual(book.print_.height_mm, 210.0)

        with tempfile.TemporaryDirectory() as td:
            root = make_book(Path(td), extra_yaml="print:\n  trim: 5.5x8.5\n")
            book = BookConfig.load(root)
            self.assertAlmostEqual(book.print_.width_mm, 139.7, places=1)

    def test_missing_title_is_an_error(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "b"
            root.mkdir()
            (root / "book.yaml").write_text("author: だれか\n", encoding="utf-8")
            with self.assertRaises(ConfigError):
                BookConfig.load(root)

    def test_manuscript_order_follows_filename(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = make_book(
                Path(td),
                chapters={
                    "03-c.md": "# C\n\n本文。\n",
                    "01-a.md": "# A\n\n本文。\n",
                    "02-b.md": "# B\n\n本文。\n",
                },
            )
            book = BookConfig.load(root)
            names = [p.name for p in book.manuscript_files()]
            self.assertEqual(names, ["01-a.md", "02-b.md", "03-c.md"])


# ------------------------------------------------------------------------- 原稿解析


class MarkdownTest(unittest.TestCase):
    def test_blocks(self) -> None:
        blocks = parse_blocks(
            "# 章タイトル\n\n段落です。\n続きの行。\n\n"
            "- 項目1\n- 項目2\n\n> 引用\n\n```sh\nls\n```\n\n"
            "![キャプション](img.png)\n\n---\n\n<!-- pagebreak -->\n"
        )
        kinds = [type(b).__name__ for b in blocks]
        self.assertEqual(
            kinds,
            [
                "Heading",
                "Paragraph",
                "ListBlock",
                "Quote",
                "CodeBlock",
                "ImageBlock",
                "SceneBreak",
                "PageBreak",
            ],
        )
        self.assertEqual(blocks[0].text, "章タイトル")
        self.assertIsInstance(blocks[2], ListBlock)
        self.assertEqual(len(blocks[2].items), 2)
        self.assertEqual(blocks[4].lang, "sh")

    def test_japanese_lines_join_without_space(self) -> None:
        (para,) = parse_blocks("日本語の行。\nつぎの行。\n")
        self.assertEqual(para.inlines[0].value, "日本語の行。つぎの行。")

    def test_ruby(self) -> None:
        (para,) = parse_blocks("｜難読《なんどく》と漢字《かんじ》。\n")
        rubies = [n for n in para.inlines if isinstance(n, Ruby)]
        self.assertEqual([(r.base, r.ruby) for r in rubies], [("難読", "なんどく"), ("漢字", "かんじ")])

    def test_front_matter(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "x.md"
            p.write_text("---\ntitle: 別のタイトル\ntype: front\ntoc: false\n---\n\n# 見出し\n\n本文。\n", encoding="utf-8")
            chapter = parse_file(p)
            self.assertEqual(chapter.title, "別のタイトル")
            self.assertEqual(chapter.kind, "front")
            self.assertFalse(chapter.in_toc)

    def test_headings_get_sequential_index(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = make_book(Path(td))
            _book, doc = load(root)
            indexes = [h.index for _c, h in doc.headings(3)]
            self.assertEqual(indexes, sorted(indexes))
            self.assertEqual(len(set(indexes)), len(indexes))

    def test_image_resolves_relative_to_source(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = make_book(Path(td))
            write_png(root / "assets" / "fig.png")
            (root / "manuscript" / "01-first.md").write_text(
                "# 章\n\n![図](../assets/fig.png)\n", encoding="utf-8"
            )
            _book, doc = load(root)
            images = [b for b in doc.chapters[0].blocks if isinstance(b, ImageBlock)]
            self.assertEqual(len(images), 1)
            self.assertIsNotNone(images[0].resolve(root))


# --------------------------------------------------------------------------- docx


class DocxTest(unittest.TestCase):
    def _build(self, root: Path, profile: str) -> zipfile.ZipFile:
        book, doc = load(root)
        out = root / f"out-{profile}.docx"
        build_docx(book, doc, profile, out)
        return zipfile.ZipFile(out)

    def test_required_parts_and_wellformed_xml(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            zf = self._build(make_book(Path(td)), "ebook")
            for part in (
                "[Content_Types].xml",
                "_rels/.rels",
                "word/document.xml",
                "word/_rels/document.xml.rels",
                "word/styles.xml",
                "word/settings.xml",
                "word/numbering.xml",
            ):
                self.assertIn(part, zf.namelist())
            for name in zf.namelist():
                if name.endswith((".xml", ".rels")):
                    ET.fromstring(zf.read(name))

    def test_headings_use_builtin_styles_with_outline_levels(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            zf = self._build(make_book(Path(td)), "ebook")
            body = zf.read("word/document.xml").decode()
            self.assertIn('<w:pStyle w:val="Heading1"/>', body)
            self.assertIn('<w:pStyle w:val="Heading2"/>', body)
            styles = zf.read("word/styles.xml").decode()
            for level in range(3):
                self.assertIn(f'<w:outlineLvl w:val="{level}"/>', styles)
            # 章の先頭で必ず改ページする
            self.assertIn("<w:pageBreakBefore/>", styles)

    def test_toc_links_match_heading_bookmarks(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            zf = self._build(make_book(Path(td)), "ebook")
            body = zf.read("word/document.xml").decode()
            bookmarks = set(re.findall(r'<w:bookmarkStart w:id="\d+" w:name="(_Toc\d+)"/>', body))
            anchors = set(re.findall(r'<w:hyperlink w:anchor="(_Toc\d+)">', body))
            self.assertTrue(anchors)
            self.assertTrue(anchors <= bookmarks, f"リンク先のないアンカー: {anchors - bookmarks}")

    def test_print_profile_page_setup(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = make_book(
                Path(td),
                extra_yaml="print:\n  trim: 6x9\n  page_numbers: true\n  mirror_margins: true\n",
            )
            zf = self._build(root, "print")
            body = zf.read("word/document.xml").decode()
            self.assertIn(f'<w:pgSz w:w="{mm_to_twips(152.4)}" w:h="{mm_to_twips(228.6)}"/>', body)
            self.assertIn("word/footer1.xml", zf.namelist())
            self.assertIn('<w:footerReference w:type="default" r:id="rId4"/>', body)
            self.assertIn(" PAGE ", zf.read("word/footer1.xml").decode())
            self.assertIn("<w:mirrorMargins/>", zf.read("word/settings.xml").decode())
            # 印刷用は既定でページ番号付きの目次フィールドを使う
            self.assertIn("w:fldSimple", body)
            self.assertIn("TOC", body)

    def test_ebook_profile_has_no_footer(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            zf = self._build(make_book(Path(td)), "ebook")
            self.assertNotIn("word/footer1.xml", zf.namelist())
            self.assertNotIn("<w:mirrorMargins/>", zf.read("word/settings.xml").decode())

    def test_ruby_and_hyperlink_and_list(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            zf = self._build(make_book(Path(td)), "ebook")
            body = zf.read("word/document.xml").decode()
            self.assertIn("<w:ruby>", body)
            self.assertIn("<w:rubyBase>", body)
            self.assertIn("<w:numPr>", body)
            rels = zf.read("word/_rels/document.xml.rels").decode()
            self.assertIn('TargetMode="External"', rels)
            self.assertIn("https://example.com", rels)

    def test_image_is_embedded(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = make_book(Path(td))
            write_png(root / "assets" / "fig.png")
            (root / "manuscript" / "01-first.md").write_text(
                "# 章\n\n![図1 テスト](../assets/fig.png)\n\n本文。\n", encoding="utf-8"
            )
            zf = self._build(root, "print")
            media = [n for n in zf.namelist() if n.startswith("word/media/")]
            self.assertEqual(len(media), 1)
            body = zf.read("word/document.xml").decode()
            self.assertIn("<w:drawing>", body)
            self.assertIn('<Default Extension="png"', zf.read("[Content_Types].xml").decode())
            rid = re.search(r'<a:blip r:embed="(rId\d+)"/>', body)
            self.assertIsNotNone(rid)
            self.assertIn(rid.group(1), zf.read("word/_rels/document.xml.rels").decode())

    def test_missing_image_becomes_a_warning_not_a_crash(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = make_book(Path(td))
            (root / "manuscript" / "01-first.md").write_text(
                "# 章\n\n![図](../assets/none.png)\n", encoding="utf-8"
            )
            book, doc = load(root)
            result = build_docx(book, doc, "ebook", root / "o.docx")
            self.assertTrue(any("見つかりません" in w for w in result.warnings))


# --------------------------------------------------------------------------- EPUB


class EpubTest(unittest.TestCase):
    def _build(self, root: Path) -> zipfile.ZipFile:
        book, doc = load(root)
        out = root / "out.epub"
        build_epub(book, doc, out)
        return zipfile.ZipFile(out)

    def test_mimetype_is_first_and_stored(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            zf = self._build(make_book(Path(td)))
            first = zf.infolist()[0]
            self.assertEqual(first.filename, "mimetype")
            self.assertEqual(first.compress_type, zipfile.ZIP_STORED)
            self.assertEqual(zf.read("mimetype"), b"application/epub+zip")

    def test_manifest_and_spine_are_consistent(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            zf = self._build(make_book(Path(td)))
            opf = ET.fromstring(zf.read("OEBPS/package.opf"))
            manifest = {
                item.get("id"): item.get("href")
                for item in opf.iter(f"{OPF}item")
            }
            names = set(zf.namelist())
            for href in manifest.values():
                self.assertIn(f"OEBPS/{href}", names, f"マニフェストのファイルがない: {href}")
            spine = [ref.get("idref") for ref in opf.iter(f"{OPF}itemref")]
            self.assertTrue(spine)
            for idref in spine:
                self.assertIn(idref, manifest, f"spineのidrefがマニフェストにない: {idref}")
            self.assertIn("nav", manifest)
            self.assertIn("ncx", manifest)

    def test_nav_links_point_at_real_anchors(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            zf = self._build(make_book(Path(td)))
            nav = ET.fromstring(zf.read("OEBPS/nav.xhtml"))
            hrefs = [
                a.get("href")
                for a in nav.iter(f"{XHTML}a")
                if a.get("href") and "#" in a.get("href")
            ]
            self.assertTrue(hrefs)
            for href in hrefs:
                file_part, _, anchor = href.partition("#")
                doc = ET.fromstring(zf.read(f"OEBPS/{file_part}"))
                ids = {el.get("id") for el in doc.iter() if el.get("id")}
                self.assertIn(anchor, ids, f"リンク先のidがない: {href}")

    def test_content_markup(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            zf = self._build(make_book(Path(td)))
            chapter = zf.read("OEBPS/text/ch001.xhtml").decode()
            self.assertIn("<ruby>", chapter)
            self.assertIn("<rt>", chapter)
            self.assertIn("<h1", chapter)
            self.assertIn("<pre><code", chapter)
            self.assertIn('href="https://example.com"', chapter)

    def test_identifier_is_stable(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = make_book(Path(td))
            first = ET.fromstring(self._build(root).read("OEBPS/package.opf"))
            second = ET.fromstring(self._build(root).read("OEBPS/package.opf"))

            def ident(tree):
                return next(tree.iter("{http://purl.org/dc/elements/1.1/}identifier")).text

            self.assertEqual(ident(first), ident(second))
            self.assertTrue(ident(first).startswith("urn:uuid:"))

    def test_cover_is_registered(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = make_book(Path(td), extra_yaml="cover: assets/cover.png\n")
            write_png(root / "assets" / "cover.png", 1600, 2560)
            zf = self._build(root)
            opf = zf.read("OEBPS/package.opf").decode()
            self.assertIn('properties="cover-image"', opf)
            self.assertIn("OEBPS/text/cover.xhtml", zf.namelist())


# ---------------------------------------------------------------------- プリフライト


class PreflightTest(unittest.TestCase):
    def test_clean_book_has_no_errors(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            book, doc = load(make_book(Path(td)))
            report = preflight.run(book, doc)
            self.assertEqual([i.message for i in report.errors], [])
            self.assertEqual(report.stats["chapters"], 2)

    def test_sample_book_passes(self) -> None:
        book = BookConfig.load(SAMPLE_BOOK)
        doc = parse_manuscript(book.manuscript_files())
        report = preflight.run(book, doc, profiles=["ebook", "print"])
        self.assertEqual([i.format() for i in report.errors], [])

    def test_too_many_keywords(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            kws = "keywords: [a, b, c, d, e, f, g, h]\n"
            book, doc = load(make_book(Path(td), extra_yaml=kws))
            report = preflight.run(book, doc)
            self.assertTrue(any("keywords" in i.message for i in report.errors))

    def test_invalid_isbn(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            book, doc = load(make_book(Path(td), extra_yaml='isbn: "978-4-00-000000-1"\n'))
            report = preflight.run(book, doc)
            self.assertTrue(any("ISBN" in i.message for i in report.errors))

    def test_valid_isbn_passes(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            book, doc = load(make_book(Path(td), extra_yaml='isbn: "9784000000000"\n'))
            report = preflight.run(book, doc)
            self.assertFalse(any("ISBN" in i.message for i in report.errors))

    def test_missing_image_is_an_error(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = make_book(Path(td))
            (root / "manuscript" / "01-first.md").write_text(
                "# 章\n\n![図](../assets/none.png)\n\n" + "本文。" * 100 + "\n", encoding="utf-8"
            )
            book, doc = load(root)
            report = preflight.run(book, doc)
            self.assertTrue(any("画像ファイルが見つかりません" in i.message for i in report.errors))

    def test_low_resolution_image_warns_for_print(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = make_book(Path(td))
            write_png(root / "assets" / "small.png", 320, 200)
            (root / "manuscript" / "01-first.md").write_text(
                "# 章\n\n![小さい図](../assets/small.png)\n", encoding="utf-8"
            )
            book, doc = load(root)
            report = preflight.run(book, doc, profiles=["print"])
            self.assertTrue(any("解像度" in i.message for i in report.warnings))

    def test_cover_aspect_ratio_warning(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = make_book(Path(td), extra_yaml="cover: assets/cover.png\n")
            write_png(root / "assets" / "cover.png", 2000, 2000)
            book, doc = load(root)
            report = preflight.run(book, doc)
            self.assertTrue(any("縦横比" in i.message for i in report.warnings))

    def test_strict_mode_fails_on_warnings(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            book, doc = load(make_book(Path(td), extra_yaml="description: ''\n"))
            report = preflight.run(book, doc)
            self.assertTrue(report.ok(strict=False))
            self.assertFalse(report.ok(strict=True))


# ------------------------------------------------------------------------ CLI


class CliTest(unittest.TestCase):
    def test_build_sample_book(self) -> None:
        import build_book

        with tempfile.TemporaryDirectory() as td:
            code = build_book.main(
                [str(SAMPLE_BOOK), "--out", td, "--quiet"]
            )
            self.assertEqual(code, 0)
            out = Path(td)
            produced = sorted(p.name for p in out.iterdir())
            self.assertIn("kdp-pipeline-guide-ebook.docx", produced)
            self.assertIn("kdp-pipeline-guide-print.docx", produced)
            self.assertIn("kdp-pipeline-guide.epub", produced)
            self.assertIn("kdp-pipeline-guide-kdp-metadata.md", produced)
            self.assertIn("build-manifest.json", produced)

    def test_check_only_writes_nothing(self) -> None:
        import build_book

        with tempfile.TemporaryDirectory() as td:
            code = build_book.main([str(SAMPLE_BOOK), "--out", td, "--check-only", "--quiet"])
            self.assertEqual(code, 0)
            self.assertEqual(list(Path(td).iterdir()), [])

    def test_preflight_error_stops_the_build(self) -> None:
        import build_book

        with tempfile.TemporaryDirectory() as td:
            root = make_book(Path(td), extra_yaml="keywords: [a, b, c, d, e, f, g, h]\n")
            code = build_book.main([str(root), "--out", str(Path(td) / "out"), "--quiet"])
            self.assertEqual(code, 1)


if __name__ == "__main__":
    unittest.main()
