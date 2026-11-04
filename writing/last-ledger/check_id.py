#!/usr/bin/env python3
"""manuscript-id/*.md の約物を検査する。

- 行ごとに “ ” の数が合っているか（台詞は二重引用符）
- 入れ子の ‘ ’ の数が合っているか（’ の直後に文字が続くものはアポストロフィとみなして数えない）
- ほかの版の約物（« »、行頭の — ）や半角の " が残っていないか
問題があればファイル名と行番号を出し、終了コード1で終わる。
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).parent / "manuscript-id"
bad = 0
for p in sorted(ROOT.glob("*.md")):
    for n, line in enumerate(p.read_text(encoding="utf-8").split("\n"), 1):
        if line.count("“") != line.count("”"):
            print(f"{p.name}:{n}: “ ” の数が合わない"); bad += 1
        if line.count("‘") != len(re.findall(r"’(?!\w)", line)):
            print(f"{p.name}:{n}: ‘ ’ の数が合わない"); bad += 1
        if re.search(r'[«»"]', line) or line.startswith("— "):
            print(f"{p.name}:{n}: ほかの版の約物か半角の \" がある"); bad += 1
print("check_id:", "OK" if not bad else f"{bad} 件")
sys.exit(1 if bad else 0)
