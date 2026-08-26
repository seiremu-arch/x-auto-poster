#!/usr/bin/env python3
"""拡張機能のアイコン(16/48/128px)を生成する。

外部ライブラリを使わずに、図形を4x4のスーパーサンプリングで描画して
PNGとして書き出す。アイコンを作り直したい場合はこのスクリプトを実行する。

    python3 amazon-product-extractor/icons/generate_icons.py
"""

import os
import struct
import zlib

ORANGE = (255, 153, 0)
ORANGE_DARK = (230, 126, 0)
WHITE = (255, 255, 255)

SAMPLES = 4  # 1辺あたりのサブサンプル数


def rounded_rect(x, y, x0, y0, x1, y1, radius):
    """点(x, y)が角丸矩形の内側かどうか。"""
    if not (x0 <= x <= x1 and y0 <= y <= y1):
        return False
    cx = min(max(x, x0 + radius), x1 - radius)
    cy = min(max(y, y0 + radius), y1 - radius)
    return (x - cx) ** 2 + (y - cy) ** 2 <= radius ** 2


def rect(x, y, x0, y0, x1, y1):
    return x0 <= x <= x1 and y0 <= y <= y1


def sample(x, y):
    """単位座標(0..1)の1点の色を返す。背景の外側はNone(透明)。"""
    if not rounded_rect(x, y, 0.02, 0.02, 0.98, 0.98, 0.22):
        return None

    # 箱(ふた・本体)。中央の縦リボンと、ふたと本体の境目は背景色で抜く
    ribbon = rect(x, y, 0.46, 0.26, 0.54, 0.82)
    lid = rounded_rect(x, y, 0.16, 0.26, 0.84, 0.40, 0.035)
    body = rounded_rect(x, y, 0.23, 0.44, 0.77, 0.82, 0.05)
    if (lid or body) and not ribbon:
        return WHITE

    # 下端をわずかに濃くして立体感を出す
    if y > 0.86:
        return ORANGE_DARK
    return ORANGE


def render(size):
    step = 1.0 / (size * SAMPLES)
    rows = []
    for py in range(size):
        row = bytearray()
        for px in range(size):
            r = g = b = a = 0.0
            for sy in range(SAMPLES):
                for sx in range(SAMPLES):
                    x = (px * SAMPLES + sx + 0.5) * step
                    y = (py * SAMPLES + sy + 0.5) * step
                    color = sample(x, y)
                    if color is None:
                        continue
                    r += color[0]
                    g += color[1]
                    b += color[2]
                    a += 255
            n = SAMPLES * SAMPLES
            if a == 0:
                row += bytes((0, 0, 0, 0))
                continue
            # 色は不透明部分だけで平均する(縁の色にじみを防ぐ)
            opaque = a / 255
            row += bytes((
                round(r / opaque),
                round(g / opaque),
                round(b / opaque),
                round(a / n),
            ))
        rows.append(bytes(row))
    return rows


def write_png(path, size, rows):
    raw = b"".join(b"\x00" + row for row in rows)

    def chunk(tag, data):
        body = tag + data
        return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body))

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(raw, 9))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    for size in (16, 48, 128):
        path = os.path.join(here, f"icon{size}.png")
        write_png(path, size, render(size))
        print(f"generated {path}")


if __name__ == "__main__":
    main()
