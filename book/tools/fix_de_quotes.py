#!/usr/bin/env python3
"""ドイツ語版の閉じ引用符を „ の相方（“）に直す。

使い方:
    python3 book/tools/fix_de_quotes.py

原稿を書くとき、開きは „ と打てても閉じはつい英語の " を打ってしまう。
読めてしまうので目では気づきにくく、check_tr_terms.py が毎回拾うことになる。
拾ってから直すより、書いたら通す手順にしておくほうが早い。

ドイツ語版の本文に限って、裸の " をすべて “ に置き換える。本文中に
英語の引用符を意図して使う場面はないので、一律で構わない。
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    changed = 0
    for path in sorted(ROOT.glob("de[0-9]/stories/[0-9][0-9]_*.txt")):
        t = path.read_text(encoding="utf-8")
        n = t.count('"')
        if not n:
            continue
        path.write_text(t.replace('"', "“"), encoding="utf-8")
        print(f"{path.relative_to(ROOT)}: 閉じ引用符 {n}個を直した")
        changed += 1

    print("直すものなし" if not changed else f"{changed}ファイル")
    return 0


if __name__ == "__main__":
    sys.exit(main())
