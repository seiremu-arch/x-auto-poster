#!/usr/bin/env python3
"""第一巻『夢編集局』のKDP用表紙画像を生成する。

使い方:
    python3 book/tools/build_cover.py

意匠は本文の「色の帯」から取っている。作中で技師がモニタに見るのは
夢の映像ではなく、記憶素片を示す色の帯だけである。表紙では大半の帯を
淡い灰に揃え、一本だけ第一話の悪夢と同じ赤黒い帯を残した。均された
社会の中に一本だけ残る、下げきれなかった荷重を示す。

出力: book/dist/cover.jpg （1600×2560px、KDP推奨の1.6:1）
"""

import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# ここを書き換えれば著者名が変わる。
# ラテン文字だけの名前は横組み、日本語を含む名前は縦組みで配置される。
AUTHOR = "Kazu A. Suzuki"
TITLE = "夢編集局"
SUBTITLE = "十二の夜"

W, H = 1600, 2560
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "dist" / "cover.jpg"
FONT = "/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf"
# IPAゴシックの欧文字形は字幅が広く間延びするため、ラテン文字には別を使う
FONT_LATIN = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"

BG = (14, 15, 18)
BAND_BASE = (58, 62, 70)
BAND_ACCENT = (122, 26, 30)  # 第一話の「赤黒く濁っていた」帯
INK = (238, 236, 230)
INK_DIM = (150, 150, 148)


def draw_bands(img: Image.Image) -> None:
    """背景に記憶素片の帯を描く。"""
    d = ImageDraw.Draw(img, "RGBA")
    rng = random.Random(20260902)

    n = 46
    margin = 150
    span = W - margin * 2
    step = span / n

    for i in range(n):
        x = margin + step * i
        w = step * rng.uniform(0.30, 0.62)

        # 帯ごとに上下の伸びと濃さを変える
        top = H * rng.uniform(0.06, 0.16)
        bottom = H * rng.uniform(0.84, 0.95)
        alpha = int(rng.uniform(28, 90))

        color = BAND_BASE + (alpha,)
        d.rectangle([x, top, x + w, bottom], fill=color)

    # 一本だけ、下げきれなかった帯
    ax = margin + step * 31
    aw = step * 0.72
    d.rectangle([ax, H * 0.05, ax + aw, H * 0.96], fill=BAND_ACCENT + (215,))
    # 芯を少し明るくして濁りを出す
    d.rectangle([ax + aw * 0.32, H * 0.05, ax + aw * 0.68, H * 0.96],
                fill=(150, 38, 40, 160))


def draw_vertical(d: ImageDraw.ImageDraw, text: str, x: int, y: int,
                  font: ImageFont.FreeTypeFont, fill, spacing: float = 1.18) -> int:
    """縦書きで一列描き、次の文字のy座標を返す。"""
    size = font.size
    for ch in text:
        bbox = font.getbbox(ch)
        cw = bbox[2] - bbox[0]
        d.text((x - cw / 2 - bbox[0], y), ch, font=font, fill=fill)
        y += int(size * spacing)
    return y


def main() -> None:
    img = Image.new("RGB", (W, H), BG)
    draw_bands(img)

    d = ImageDraw.Draw(img)

    f_title = ImageFont.truetype(FONT, 172)
    f_sub = ImageFont.truetype(FONT, 58)
    f_author = ImageFont.truetype(FONT, 52)

    # 題は右寄せの縦組み
    title_x = int(W * 0.755)
    title_y = int(H * 0.115)
    draw_vertical(d, TITLE, title_x, title_y, f_title, INK, spacing=1.16)

    # 副題は題の左に一段落として置く
    sub_x = int(W * 0.575)
    sub_y = int(H * 0.135)
    draw_vertical(d, SUBTITLE, sub_x, sub_y, f_sub, INK_DIM, spacing=1.35)

    # 著者名。ラテン文字を縦組みにすると字が寝てしまうので、横組みで置く
    if AUTHOR.isascii():
        f_author = ImageFont.truetype(FONT_LATIN, 52)
        bbox = f_author.getbbox(AUTHOR)
        d.text((int(W * 0.135) - bbox[0], int(H * 0.845)),
               AUTHOR, font=f_author, fill=INK_DIM)
    else:
        draw_vertical(d, AUTHOR, int(W * 0.16), int(H * 0.735), f_author,
                      INK_DIM, spacing=1.3)

    # 下部に細い罫を一本
    d.rectangle([int(W * 0.10), int(H * 0.955),
                 int(W * 0.90), int(H * 0.955) + 2], fill=(70, 70, 74))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, "JPEG", quality=92, optimize=True)

    kb = OUT.stat().st_size / 1024
    print(f"出力: {OUT}")
    print(f"寸法: {W}×{H}px（比率 {H / W:.2f}:1）")
    print(f"容量: {kb:.0f}KB")
    print(f"著者名: {AUTHOR}")


if __name__ == "__main__":
    main()
