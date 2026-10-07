#!/usr/bin/env python3
"""manuscript-it/*.md の約物を検査する。

- 行ごとに « と » の数が合っているか
- « の直後・» の直前にスペースが入っていないか（イタリア語の慣例）
問題があればファイル名と行番号を出し、終了コード1で終わる。
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).parent / "manuscript-it"
bad = 0
for p in sorted(ROOT.glob("*.md")):
    for n, line in enumerate(p.read_text(encoding="utf-8").split("\n"), 1):
        if line.count("«") != line.count("»"):
            print(f"{p.name}:{n}: « » の数が合わない"); bad += 1
        if re.search(r"«\s|\s»", line):
            print(f"{p.name}:{n}: « » の内側にスペース"); bad += 1
print("check_it:", "OK" if not bad else f"{bad} 件")
sys.exit(1 if bad else 0)
