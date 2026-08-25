"""画像ファイルのサイズ・形式を標準ライブラリだけで調べる。

docxの ``<wp:extent>`` と EPUB の manifest に必要な情報しか取らないので、
PNG / JPEG / GIF のヘッダだけを読む。
"""

from __future__ import annotations

import struct
from dataclasses import dataclass
from pathlib import Path

MIME_BY_EXT = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".svg": "image/svg+xml",
    ".webp": "image/webp",
    ".tif": "image/tiff",
    ".tiff": "image/tiff",
    ".bmp": "image/bmp",
}

#: KDPが受け付ける本文画像の形式
KDP_SAFE_FORMATS = {"image/jpeg", "image/png", "image/gif", "image/bmp", "image/tiff"}

EMU_PER_INCH = 914400


class ImageError(Exception):
    pass


@dataclass
class ImageInfo:
    path: Path
    mime: str
    width_px: int
    height_px: int
    dpi_x: float = 96.0
    dpi_y: float = 96.0

    @property
    def aspect(self) -> float:
        return self.width_px / self.height_px if self.height_px else 0.0

    def emu_for_width_mm(self, max_width_mm: float) -> tuple[int, int]:
        """指定の版面幅(mm)に収まるサイズを EMU で返す。"""
        natural_w_in = self.width_px / (self.dpi_x or 96.0)
        natural_h_in = self.height_px / (self.dpi_y or 96.0)
        max_w_in = max_width_mm / 25.4
        if natural_w_in > max_w_in and natural_w_in > 0:
            scale = max_w_in / natural_w_in
            natural_w_in *= scale
            natural_h_in *= scale
        return (
            max(1, int(round(natural_w_in * EMU_PER_INCH))),
            max(1, int(round(natural_h_in * EMU_PER_INCH))),
        )


def mime_for(path: str | Path) -> str:
    return MIME_BY_EXT.get(Path(path).suffix.lower(), "application/octet-stream")


def probe(path: str | Path) -> ImageInfo:
    """画像のピクセルサイズと解像度を返す。読めない形式なら ImageError。"""
    p = Path(path)
    data = p.read_bytes()
    mime = mime_for(p)

    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return _probe_png(p, data, mime)
    if data[:2] == b"\xff\xd8":
        return _probe_jpeg(p, data, mime)
    if data[:6] in (b"GIF87a", b"GIF89a"):
        w, h = struct.unpack("<HH", data[6:10])
        return ImageInfo(p, mime, w, h)
    raise ImageError(f"サイズを取得できない画像形式です: {p}")


def _probe_png(p: Path, data: bytes, mime: str) -> ImageInfo:
    if len(data) < 24 or data[12:16] != b"IHDR":
        raise ImageError(f"壊れたPNGです: {p}")
    width, height = struct.unpack(">II", data[16:24])
    dpi_x = dpi_y = 96.0
    offset = 8
    while offset + 8 <= len(data):
        length = struct.unpack(">I", data[offset : offset + 4])[0]
        ctype = data[offset + 4 : offset + 8]
        if ctype == b"pHYs" and offset + 8 + 9 <= len(data):
            ppu_x, ppu_y, unit = struct.unpack(">IIB", data[offset + 8 : offset + 17])
            if unit == 1:  # meters
                dpi_x = ppu_x * 0.0254
                dpi_y = ppu_y * 0.0254
            break
        if ctype == b"IDAT":
            break
        offset += 12 + length
    return ImageInfo(p, mime, width, height, dpi_x or 96.0, dpi_y or 96.0)


def _probe_jpeg(p: Path, data: bytes, mime: str) -> ImageInfo:
    dpi_x = dpi_y = 96.0
    i = 2
    width = height = 0
    while i + 4 <= len(data):
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
            i += 2
            continue
        seg_len = struct.unpack(">H", data[i + 2 : i + 4])[0]
        seg = data[i + 4 : i + 2 + seg_len]
        if marker == 0xE0 and seg[:5] == b"JFIF\x00" and len(seg) >= 12:
            units, x_density, y_density = struct.unpack(">BHH", seg[7:12])
            if units == 1 and x_density and y_density:
                dpi_x, dpi_y = float(x_density), float(y_density)
            elif units == 2 and x_density and y_density:  # dots per cm
                dpi_x, dpi_y = x_density * 2.54, y_density * 2.54
        if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            height, width = struct.unpack(">HH", seg[1:5])
            break
        i += 2 + seg_len
    if not width or not height:
        raise ImageError(f"JPEGのサイズを取得できませんでした: {p}")
    return ImageInfo(p, mime, width, height, dpi_x, dpi_y)
