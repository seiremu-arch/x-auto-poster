"""KDP(Kindle Direct Publishing)向け原稿ビルドパイプライン。

Markdown原稿 + book.yaml から、KDPにそのまま入稿できる
docx(電子書籍用 / ペーパーバック用)と EPUB3 を生成する。
"""

__all__ = [
    "config",
    "mdparse",
    "docx_builder",
    "epub_builder",
    "preflight",
]
