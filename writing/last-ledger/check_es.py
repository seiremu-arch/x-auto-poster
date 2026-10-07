#!/usr/bin/env python3
"""manuscript-es/*.md の約物を検査する。

- « と » の数が合っているか
- 文中の ? ! に対応する ¿ ¡ があるか（行ごとに数を比べる）
問題があればファイル名と行番号を出し、終了コード1で終わる。
"""
import pathlib, sys

ROOT = pathlib.Path(__file__).parent / "manuscript-es"
bad = 0
for p in sorted(ROOT.glob("*.md")):
    for n, line in enumerate(p.read_text(encoding="utf-8").split("\n"), 1):
        if line.count("«") != line.count("»"):
            print(f"{p.name}:{n}: « » の数が合わない"); bad += 1
        if line.count("¿") != line.count("?"):
            print(f"{p.name}:{n}: ¿ ? の数が合わない"); bad += 1
        if line.count("¡") != line.count("!"):
            print(f"{p.name}:{n}: ¡ ! の数が合わない"); bad += 1
print("check_es:", "OK" if not bad else f"{bad} 件")
sys.exit(1 if bad else 0)
