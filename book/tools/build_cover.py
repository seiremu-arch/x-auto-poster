#!/usr/bin/env python3
"""KDP用の表紙画像を生成する。

使い方:
    python3 book/tools/build_cover.py vol1
    python3 book/tools/build_cover.py          # 全巻

意匠は本文の「色の帯」から取っている。作中で技師がモニタに見るのは夢の
映像ではなく、記憶素片を示す色の帯だけである。

第一巻は、大半の帯を淡い灰に揃え、一本だけ第一話の悪夢と同じ赤黒い帯を
残した。均された社会の中に一本だけ残る、下げきれなかった荷重を示す。

第二巻は同じ帯を揃えた状態にする。高さのばらつきを詰め、赤い帯も他の帯と
ほとんど見分けがつかない濃さまで落とす。二冊並べたとき、一冊目に残っていた
一本が二冊目で消えかけて見える。分散が下がったのか、見えなくなったのかを
区別できないという最終話の主題を、そのまま表紙の差にした。

英語版（en1）は第一巻と同じ種・同じ濃さ・同じばらつきで帯を描く。帯の意匠は
原書と揃え、字だけをラテン文字の横組みに変える。二つの版が同じ本であることを
表紙で示すため、帯の並びは一本も動かさない。

出力: book/dist/cover_vol1.jpg など （1600×2560px、KDP推奨の1.6:1）
"""

import random
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# ここを書き換えれば著者名が変わる。
# ラテン文字だけの名前は横組み、日本語を含む名前は縦組みで配置される。
AUTHOR = "Kazu A. Suzuki"

VOLUMES = {
    "vol1": {
        "title": "夢編集局",
        "subtitle": "十二の夜",
        "seed": 20260902,
        "accent_alpha": 215,   # 赤黒い帯の濃さ
        "height_spread": 0.10,  # 帯の高さのばらつき
        "alpha_range": (28, 90),
        "vertical": True,
    },
    "en1": {
        # 第一巻の英語版。帯の数値はすべて vol1 と同一にする
        "title": "The Dream\nEditing\nBureau",
        "subtitle": "Twelve Nights",
        "seed": 20260902,
        "accent_alpha": 215,
        "height_spread": 0.10,
        "alpha_range": (28, 90),
        "vertical": False,
    },
    "vol2": {
        "title": "均し",
        "subtitle": "夢編集局 第二集",
        "seed": 20260902,       # 同じ種を使い、同じ帯の並びを保つ
        "accent_alpha": 58,     # ほとんど見分けがつかないところまで落とす
        "height_spread": 0.03,  # 高さを揃える
        "alpha_range": (46, 62),
        "vertical": True,
    },
    "en2": {
        # 第二巻の英語版。帯の数値はすべて vol2 と同一にする
        "title": "The\nLevelling",
        "subtitle": "The Dream Editing Bureau, Book Two",
        "seed": 20260902,
        "accent_alpha": 58,
        "height_spread": 0.03,
        "alpha_range": (46, 62),
        "vertical": False,
    },
    "de1": {
        # 第一巻のドイツ語版。帯の数値はすべて vol1 と同一にする
        "title": "Das\nTraumamt",
        "subtitle": "Zwölf Nächte",
        "seed": 20260902,
        "accent_alpha": 215,
        "height_spread": 0.10,
        "alpha_range": (28, 90),
        "vertical": False,
    },
    "de2": {
        # 第二巻のドイツ語版。帯の数値はすべて vol2 と同一にする
        "title": "Die\nAngleichung",
        "subtitle": "Das Traumamt, Band Zwei",
        "seed": 20260902,
        "accent_alpha": 58,
        "height_spread": 0.03,
        "alpha_range": (46, 62),
        "vertical": False,
    },
    "es1": {
        # 第一巻のスペイン語版。帯の数値はすべて vol1 と同一にする
        "title": "La Oficina\nde Sueños",
        "subtitle": "Doce noches",
        "seed": 20260902,
        "accent_alpha": 215,
        "height_spread": 0.10,
        "alpha_range": (28, 90),
        "vertical": False,
    },
    "es2": {
        # 第二巻のスペイン語版。帯の数値はすべて vol2 と同一にする
        "title": "La\nNivelación",
        "subtitle": "La Oficina de Sueños, Libro Dos",
        "seed": 20260902,
        "accent_alpha": 58,
        "height_spread": 0.03,
        "alpha_range": (46, 62),
        "vertical": False,
    },
    "fr1": {
        # 第一巻のフランス語版。帯の数値はすべて vol1 と同一にする
        "title": "Le Bureau\ndes Rêves",
        "subtitle": "Douze nuits",
        "seed": 20260902,
        "accent_alpha": 215,
        "height_spread": 0.10,
        "alpha_range": (28, 90),
        "vertical": False,
    },
    "fr2": {
        # 第二巻のフランス語版。帯の数値はすべて vol2 と同一にする
        "title": "Le\nNivellement",
        "subtitle": "Le Bureau des Rêves, Livre Deux",
        "seed": 20260902,
        "accent_alpha": 58,
        "height_spread": 0.03,
        "alpha_range": (46, 62),
        "vertical": False,
    },
    "it1": {
        # 第一巻のイタリア語版。帯の数値はすべて vol1 と同一にする
        "title": "L'Ufficio\ndei Sogni",
        "subtitle": "Dodici notti",
        "seed": 20260902,
        "accent_alpha": 215,
        "height_spread": 0.10,
        "alpha_range": (28, 90),
        "vertical": False,
    },
    "it2": {
        # 第二巻のイタリア語版。帯の数値はすべて vol2 と同一にする
        "title": "Il\nLivellamento",
        "subtitle": "L'Ufficio dei Sogni, Libro Due",
        "seed": 20260902,
        "accent_alpha": 58,
        "height_spread": 0.03,
        "alpha_range": (46, 62),
        "vertical": False,
    },
    "nl1": {
        # 第一巻のオランダ語版。帯の数値はすべて vol1 と同一にする
        "title": "Het\nDroombureau",
        "subtitle": "Twaalf nachten",
        "seed": 20260902,
        "accent_alpha": 215,
        "height_spread": 0.10,
        "alpha_range": (28, 90),
        "vertical": False,
    },
    "nl2": {
        # 第二巻のオランダ語版。帯の数値はすべて vol2 と同一にする
        "title": "De\nNivellering",
        "subtitle": "Het Droombureau, Deel Twee",
        "seed": 20260902,
        "accent_alpha": 58,
        "height_spread": 0.03,
        "alpha_range": (46, 62),
        "vertical": False,
    },
    "pt1": {
        # 第一巻のブラジルポルトガル語版。帯の数値はすべて vol1 と同一にする
        "title": "A Reparti\u00e7\u00e3o\ndos Sonhos",
        "subtitle": "Doze noites",
        "seed": 20260902,
        "accent_alpha": 215,
        "height_spread": 0.10,
        "alpha_range": (28, 90),
        "vertical": False,
    },
    "pt2": {
        # 第二巻のブラジルポルトガル語版。帯の数値はすべて vol2 と同一にする
        "title": "O\nNivelamento",
        "subtitle": "A Reparti\u00e7\u00e3o dos Sonhos, Livro Dois",
        "seed": 20260902,
        "accent_alpha": 58,
        "height_spread": 0.03,
        "alpha_range": (46, 62),
        "vertical": False,
    },
}

W, H = 1600, 2560
ROOT = Path(__file__).resolve().parent.parent
FONT = "/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf"
# IPAゴシックの欧文字形は字幅が広く間延びするため、ラテン文字には別を使う
FONT_LATIN = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"

BG = (14, 15, 18)
BAND_BASE = (58, 62, 70)
BAND_ACCENT = (122, 26, 30)  # 第一話の「赤黒く濁っていた」帯
INK = (238, 236, 230)
INK_DIM = (150, 150, 148)


def draw_bands(img: Image.Image, meta: dict) -> None:
    """背景に記憶素片の帯を描く。巻によって揃い方が変わる。"""
    d = ImageDraw.Draw(img, "RGBA")
    rng = random.Random(meta["seed"])

    n = 46
    margin = 150
    span = W - margin * 2
    step = span / n

    spread = meta["height_spread"]
    a_lo, a_hi = meta["alpha_range"]

    for i in range(n):
        x = margin + step * i
        w = step * rng.uniform(0.30, 0.62)

        # 帯ごとに上下の伸びと濃さを変える。spreadが小さいほど揃う
        top = H * (0.11 + rng.uniform(-spread / 2, spread / 2))
        bottom = H * (0.895 + rng.uniform(-spread / 2, spread / 2))
        alpha = int(rng.uniform(a_lo, a_hi))

        d.rectangle([x, top, x + w, bottom], fill=BAND_BASE + (alpha,))

    # 一本だけ、下げきれなかった帯
    aa = meta["accent_alpha"]
    ax = margin + step * 31
    aw = step * 0.72
    d.rectangle([ax, H * 0.05, ax + aw, H * 0.96], fill=BAND_ACCENT + (aa,))
    # 芯を少し明るくして濁りを出す
    d.rectangle([ax + aw * 0.32, H * 0.05, ax + aw * 0.68, H * 0.96],
                fill=(150, 38, 40, int(aa * 0.74)))


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


def draw_horizontal_title(d: ImageDraw.ImageDraw, meta: dict) -> None:
    """ラテン文字の題を左寄せの横組みで置く。英語版用。"""
    lines = meta["title"].split("\n")
    f_title = ImageFont.truetype(FONT_LATIN, 150)
    f_sub = ImageFont.truetype(FONT_LATIN, 50)

    x = int(W * 0.105)
    y = int(H * 0.125)
    leading = int(f_title.size * 1.14)

    for line in lines:
        bbox = f_title.getbbox(line)
        d.text((x - bbox[0], y), line, font=f_title, fill=INK)
        y += leading

    # 副題は題の下に、細い罫を挟んで置く
    y += int(H * 0.012)
    d.rectangle([x, y, x + int(W * 0.17), y + 2], fill=(110, 110, 112))
    y += int(H * 0.028)
    bbox = f_sub.getbbox(meta["subtitle"])
    d.text((x - bbox[0], y), meta["subtitle"], font=f_sub, fill=INK_DIM)


def build(vol: str) -> None:
    meta = VOLUMES[vol]
    img = Image.new("RGB", (W, H), BG)
    draw_bands(img, meta)

    d = ImageDraw.Draw(img)

    if not meta["vertical"]:
        draw_horizontal_title(d, meta)
    else:
        # 題が短いほど字を大きくして、天地の収まりを揃える
        title = meta["title"]
        f_title = ImageFont.truetype(FONT, 172 if len(title) >= 4 else 214)
        f_sub = ImageFont.truetype(FONT, 58)

        # 題は右寄せの縦組み
        draw_vertical(d, title, int(W * 0.755), int(H * 0.115), f_title, INK,
                      spacing=1.16)

        # 副題は題の左に一段落として置く
        draw_vertical(d, meta["subtitle"], int(W * 0.575), int(H * 0.135),
                      f_sub, INK_DIM, spacing=1.35)

    f_author = ImageFont.truetype(FONT, 52)

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

    out = ROOT / "dist" / f"cover_{vol}.jpg"
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "JPEG", quality=92, optimize=True)

    kb = out.stat().st_size / 1024
    shown = meta["title"].replace("\n", " ")
    print(f"[{vol}] 『{shown}』 → {out}")
    print(f"  {W}×{H}px（比率 {H / W:.2f}:1）／{kb:.0f}KB／著者 {AUTHOR}")


def main() -> None:
    targets = sys.argv[1:] or list(VOLUMES)
    for vol in targets:
        if vol not in VOLUMES:
            raise SystemExit(f"不明な巻: {vol}（指定できるのは {', '.join(VOLUMES)}）")
        build(vol)


if __name__ == "__main__":
    main()
