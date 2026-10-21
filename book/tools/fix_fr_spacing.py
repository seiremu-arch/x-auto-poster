#!/usr/bin/env python3
"""フランス語版の約物前後の空白を不可分空白に直す。

使い方:
    python3 book/tools/fix_fr_spacing.py            # fr1/fr2 の全話
    python3 book/tools/fix_fr_spacing.py fr2/09     # 一話だけ

フランス語は `:` `;` `?` `!` の前と « » の内側に不可分空白が要り、千の位も
点ではなく不可分空白で区切る。規則としては単純だが、二十四話ぶんを手で打つと
必ずどこかで落ちる。落ちても字は読めるので通読では気づかず、リーダーで行が
変なところで折れて初めて分かる。だから機械で入れる。

変換は字面の規則だけでできるものに限る。内容には触らない。
  ・`:` `;` `?` `!` の直前 → 不可分空白を一つ（無い場合は挿入、ふつうの
    空白なら置換）
  ・« の直後、» の直前 → 同じ
  ・数字のあいだのふつうの空白（1 027 400）→ 不可分空白

桁区切り自体を入れる（1027400 → 1 027 400）ことはしない。どこで切るかは
数の意味の問題で、字面からは決められない。入っていないことは
check_tr_terms.py が報告する。

直したあとは必ず check_tr_terms.py を通す。この道具は検査の代わりではなく、
検査が鳴らないようにするための前処理である。
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NB = " "

# 置換は約物そのものを取り込む。先読みで書くと `*` が空文字にも当たって
# 不可分空白が二つ入る（最初にそう書いて二重になった）。
RULES = [
    # 約物の前。直前のふつうの空白は飲み込んでから一つ入れる
    (re.compile(r"[  ]*([;:?!])"), NB + r"\1"),
    # « の後ろ
    (re.compile(r"(«)[  ]*"), r"\1" + NB),
    # » の前
    (re.compile(r"[  ]*(»)"), NB + r"\1"),
    # 桁区切りのふつうの空白
    (re.compile(r"(?<=\d) (?=\d{3}(?!\d))"), NB),
]


def fix(text: str) -> str:
    out = []
    for line in text.split("\n"):
        # 節番号の行（I, II, …）と空行は触らない
        if not line.strip() or re.fullmatch(r"[IVXLC]+", line.strip()):
            out.append(line)
            continue
        for rx, rep in RULES:
            line = rx.sub(rep, line)
        out.append(line)
    return "\n".join(out)


def targets(args: list) -> list:
    if not args:
        return sorted(p for d in ("fr1", "fr2")
                      for p in (ROOT / d / "stories").glob("[0-9][0-9]_*.txt"))
    found = []
    for a in args:
        vol, _, num = a.partition("/")
        hits = sorted((ROOT / vol / "stories").glob(f"{num}_*.txt"))
        if not hits:
            raise SystemExit(f"見つかりません: {a}")
        found += hits
    return found


def main() -> int:
    changed = 0
    for path in targets(sys.argv[1:]):
        before = path.read_text(encoding="utf-8")
        after = fix(before)
        if before == after:
            continue
        path.write_text(after, encoding="utf-8")
        n = sum(1 for a, b in zip(before.split("\n"), after.split("\n")) if a != b)
        print(f"{path.relative_to(ROOT)}: {n}行を直した")
        changed += 1
    print(f"直したファイル {changed}件" if changed else "直すところなし")
    return 0


if __name__ == "__main__":
    sys.exit(main())
