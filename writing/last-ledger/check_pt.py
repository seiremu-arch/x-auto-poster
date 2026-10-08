#!/usr/bin/env python3
"""manuscript-pt/*.md の約物を検査する。

- 台詞の段落は「— 」（ダッシュ＋空白）で始まっているか（ダッシュの直後に空白がない誤りを拾う）
- 行ごとに “ ” の数が合っているか
- ほかの版の約物（« » ‘ ’）や半角の " が残っていないか
問題があればファイル名と行番号を出し、終了コード1で終わる。
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).parent / "manuscript-pt"
bad = 0
for p in sorted(ROOT.glob("*.md")):
    for n, line in enumerate(p.read_text(encoding="utf-8").split("\n"), 1):
        if re.match(r"—\S", line):
            print(f"{p.name}:{n}: 行頭の — のあとに空白がない"); bad += 1
        if line.count("“") != line.count("”"):
            print(f"{p.name}:{n}: “ ” の数が合わない"); bad += 1
        if re.search(r'[«»‘’"]', line):
            print(f"{p.name}:{n}: ほかの版の約物か半角の \" がある"); bad += 1
print("check_pt:", "OK" if not bad else f"{bad} 件")
sys.exit(1 if bad else 0)
