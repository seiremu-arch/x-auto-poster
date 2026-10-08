#!/usr/bin/env python3
"""manuscript-nl/*.md の約物を検査する。

- 行ごとに ‘ と ’ の数が合っているか（台詞は ‘ ’、アポストロフィは半角の '）
- 入れ子の “ ” の数が合っているか
- 半角の " が残っていないか
- ’ の直後に文字が続いていないか（アポストロフィを ’ で書いた誤り）
問題があればファイル名と行番号を出し、終了コード1で終わる。
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).parent / "manuscript-nl"
bad = 0
for p in sorted(ROOT.glob("*.md")):
    for n, line in enumerate(p.read_text(encoding="utf-8").split("\n"), 1):
        if line.count("‘") != line.count("’"):
            print(f"{p.name}:{n}: ‘ ’ の数が合わない"); bad += 1
        if line.count("“") != line.count("”"):
            print(f"{p.name}:{n}: “ ” の数が合わない"); bad += 1
        if re.search(r"’\w", line):
            print(f"{p.name}:{n}: アポストロフィが ’ になっている"); bad += 1
        if '"' in line:
            print(f"{p.name}:{n}: 半角の \" がある"); bad += 1
print("check_nl:", "OK" if not bad else f"{bad} 件")
sys.exit(1 if bad else 0)
