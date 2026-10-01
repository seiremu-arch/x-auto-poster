#!/usr/bin/env python3
"""manuscript-fr/*.md にフランス語の組版規則を当てる（何度かけても同じ結果になる）。

- « » の内側は改行なしスペース（U+00A0）
- ? ! ; の前は細い改行なしスペース（U+202F）
- : の前は改行なしスペース（U+00A0）
"""
import pathlib, re

NBSP, NNBSP = " ", " "
ROOT = pathlib.Path(__file__).parent / "manuscript-fr"


def fix(text):
    out = []
    for line in text.split("\n"):
        line = re.sub(r"«[   ]*", "«" + NBSP, line)
        line = re.sub(r"[   ]*»", NBSP + "»", line)
        line = re.sub(r"(?<=\S)[   ]*([?!;])", NNBSP + r"\1", line)
        line = re.sub(r"(?<=\S)[   ]+:", NBSP + ":", line)
        out.append(line)
    return "\n".join(out)


if __name__ == "__main__":
    n = 0
    for p in sorted(ROOT.glob("*.md")):
        s = p.read_text(encoding="utf-8")
        t = fix(s)
        if t != s:
            p.write_text(t, encoding="utf-8")
            n += 1
    print("fr_typo:", n, "files updated")
