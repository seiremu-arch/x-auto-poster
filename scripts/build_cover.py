#!/usr/bin/env python3
"""books/<slug>/ の表紙を作る。文字だけで組む(画像生成はしない)。

仕様は各言語の PLAN.md / LISTING.md にある「表紙の仕様」:
余白を大きく、1色ベース、要素は3つ(タイトル・サブタイトル・著者名)、細いセリフ体、
人物・光の粒子・後光などの意匠は使わない。サムネイル(縦200px)でタイトルが読めること。
五言語で同じデザインにして、文字だけ差し替える。

    python scripts/build_cover.py --fetch-fonts      # 初回だけ。npm から Noto Serif を取得
    python scripts/build_cover.py inner-voice         # books/inner-voice/build/inner-voice-cover.jpg
    python scripts/build_cover.py --all               # 全言語
    python scripts/build_cover.py --all --sheet PATH  # 全言語の縮小版を1枚に並べる(確認用)

フォントは OFL-1.1(SIL Open Font License)。表紙画像への使用は許されている。
リポジトリには入れず `books/.fonts/`(gitignore)に置く。
"""

import argparse
import json
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
BOOKS = ROOT / "books"
FONTS = BOOKS / ".fonts"

# KDP の推奨: 高さ:幅 = 1.6:1 の縦長。幅1600 × 高さ2560
WIDTH, HEIGHT = 1600, 2560
MARGIN = 200                      # 左右の余白
BACKGROUND = (243, 239, 230)      # 生成り
INK = (40, 44, 51)                # 墨に近い濃い青灰
INK_SOFT = (96, 101, 110)         # サブタイトルと著者名

FONT_PACKAGES = {
    "@expo-google-fonts/noto-serif-jp": ["NotoSerifJP_300Light.ttf", "NotoSerifJP_400Regular.ttf"],
    "@expo-google-fonts/noto-serif": ["NotoSerif_300Light.ttf", "NotoSerif_400Regular.ttf"],
}


# --------------------------------------------------------------------------- フォント

def fetch_fonts():
    FONTS.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        for package, wanted in FONT_PACKAGES.items():
            subprocess.run(["npm", "pack", package, "--silent"], cwd=tmp, check=True, capture_output=True)
        for archive in Path(tmp).glob("*.tgz"):
            with tarfile.open(archive) as tar:
                for member in tar.getmembers():
                    name = Path(member.name).name
                    if any(name in files for files in FONT_PACKAGES.values()):
                        member.name = name
                        tar.extract(member, FONTS)
    found = sorted(p.name for p in FONTS.glob("*.ttf"))
    print("fonts:", ", ".join(found))


def font(language, weight, size):
    family = "NotoSerifJP" if language == "ja" else "NotoSerif"
    path = FONTS / f"{family}_{weight}.ttf"
    if not path.exists():
        raise SystemExit(f"{path} がありません。先に `python scripts/build_cover.py --fetch-fonts` を実行してください")
    return ImageFont.truetype(str(path), size)


# --------------------------------------------------------------------------- 組版

def text_width(draw, text, typeface, tracking=0):
    if not text:
        return 0
    return draw.textlength(text, font=typeface) + tracking * (len(text) - 1)


def units(text, language):
    """改行できる単位。日本語は文字、それ以外は語。"""
    return list(text) if language == "ja" else text.split()


def join(parts, language):
    return "".join(parts) if language == "ja" else " ".join(parts)


def wrap(draw, text, typeface, max_width, language, tracking=0):
    """貪欲に詰めて折り返す(サブタイトル用)。"""
    lines, current = [], []
    for unit in units(text, language):
        trial = join(current + [unit], language)
        if current and text_width(draw, trial, typeface, tracking) > max_width:
            lines.append(join(current, language))
            current = [unit]
        else:
            current.append(unit)
    if current:
        lines.append(join(current, language))
    return lines


def fit_title(draw, title, language, max_width, forced_lines=None):
    """タイトルは最大2行。行の長さが揃う切れ目を選び、収まるいちばん大きい字で組む。"""
    candidates = []
    if forced_lines:
        candidates = [forced_lines]
    else:
        parts = units(title, language)
        candidates.append([title])
        for cut in range(1, len(parts)):
            candidates.append([join(parts[:cut], language), join(parts[cut:], language)])

    best = None
    for size in range(230, 80, -2):
        typeface = font(language, "300Light", size)
        for lines in candidates:
            widths = [text_width(draw, line, typeface) for line in lines]
            if max(widths) > max_width:
                continue
            # 1行で収まるならそれを優先。2行なら行の長さの差が小さいものを選ぶ
            score = (len(lines), max(widths) - min(widths))
            if best is None or score < best[0]:
                best = (score, size, lines)
        if best:
            return font(language, "300Light", best[1]), best[2], best[1]
    raise SystemExit(f"タイトルが収まりません: {title}")


def render(slug):
    meta = json.loads((BOOKS / slug / "book.json").read_text(encoding="utf-8"))
    language = meta.get("language", "ja")
    cover = meta.get("cover", {})

    image = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
    draw = ImageDraw.Draw(image)
    usable = WIDTH - 2 * MARGIN

    # タイトル: 中央よりやや上(高さの約4割の位置に、ブロックの中心を置く)
    title_font, title_lines, title_size = fit_title(draw, meta["title"], language, usable, cover.get("title_lines"))
    line_gap = int(title_size * (0.42 if language == "ja" else 0.22))
    ascent, descent = title_font.getmetrics()
    line_height = ascent + descent
    block = len(title_lines) * line_height + (len(title_lines) - 1) * line_gap
    top = int(HEIGHT * 0.40 - block / 2)
    for index, line in enumerate(title_lines):
        width = text_width(draw, line, title_font)
        draw.text(((WIDTH - width) / 2, top + index * (line_height + line_gap)), line, font=title_font, fill=INK)
    title_bottom = top + block

    # サブタイトル: タイトルの下に、大きく間を空けて小さく
    sub_size = 46 if language == "ja" else 48
    sub_font = font(language, "300Light", sub_size)
    sub_lines = wrap(draw, meta.get("subtitle", ""), sub_font, int(usable * 0.86), language)
    sub_line_height = int(sub_size * 1.75)
    y = title_bottom + int(title_size * 0.95)
    for line in sub_lines:
        width = text_width(draw, line, sub_font)
        draw.text(((WIDTH - width) / 2, y), line, font=sub_font, fill=INK_SOFT)
        y += sub_line_height

    # 著者名: 下のほう。字間を少し開ける
    author_font = font(language, "400Regular", 50)
    tracking = 6
    author = meta.get("author", "")
    width = text_width(draw, author, author_font, tracking)
    x, y = (WIDTH - width) / 2, int(HEIGHT * 0.86)
    for char in author:
        draw.text((x, y), char, font=author_font, fill=INK_SOFT)
        x += draw.textlength(char, font=author_font) + tracking

    out = BOOKS / slug / "build" / f"{slug}-cover.jpg"
    out.parent.mkdir(parents=True, exist_ok=True)
    image.save(out, "JPEG", quality=92, optimize=True)
    return out, title_lines, title_size


def contact_sheet(paths, out, thumb_height=200):
    """縮小版を横に並べる。KDP の一覧で見える大きさでタイトルが読めるかを確かめるため。"""
    thumbs = []
    for path in paths:
        img = Image.open(path)
        w = round(img.width * thumb_height / img.height)
        thumbs.append(img.resize((w, thumb_height), Image.LANCZOS))
    gap = 24
    sheet = Image.new("RGB", (sum(t.width for t in thumbs) + gap * (len(thumbs) + 1), thumb_height + 2 * gap), (255, 255, 255))
    x = gap
    for thumb in thumbs:
        sheet.paste(thumb, (x, gap))
        x += thumb.width + gap
    sheet.save(out)
    return out


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("slug", nargs="?", help="books/ の下のディレクトリ名")
    parser.add_argument("--all", action="store_true", help="book.json を持つ全ディレクトリ")
    parser.add_argument("--fetch-fonts", action="store_true", help="npm から Noto Serif / Noto Serif JP を取得する")
    parser.add_argument("--sheet", help="縮小版(縦200px)を並べた確認用の画像を書き出すパス")
    args = parser.parse_args(argv)

    if args.fetch_fonts:
        if not shutil.which("npm"):
            raise SystemExit("npm がありません")
        fetch_fonts()
        if not (args.slug or args.all):
            return 0

    slugs = sorted(p.parent.name for p in BOOKS.glob("*/book.json")) if args.all else [args.slug]
    if not slugs or slugs == [None]:
        parser.error("slug か --all を指定してください")

    outputs = []
    for slug in slugs:
        out, lines, size = render(slug)
        outputs.append(out)
        print(f"  {slug:16} {' / '.join(lines)}  ({size}px)  → {out.relative_to(ROOT)}")
    if args.sheet:
        print(f"  sheet → {contact_sheet(outputs, Path(args.sheet))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
