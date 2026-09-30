#!/usr/bin/env python3
"""フランス語版の文体検査: 手順の外に出た命令形・禁止語・約物の前の空白。

`vous` で書くと決めた(Vault `e778004e3b`)ことの反証条件が命令形の検査。ドイツ語版では
`du` の命令形が章末と見出しに14件漏れた(`7586251f89`)。フランス語版は最初の章から回す。

「Remettez les noms, et cela redevient …」のような**条件の言い方**は、命令ではなく帰結の
説明なので許す。落とすのは手順の外にある**裸の指示**だけ。

    python books/inner-voice-fr/check_style.py          # 検査(見つかったら終了コード1)
    python books/inner-voice-fr/check_style.py --fix    # ; : ! ? の前と « » の内側を U+00A0 にする
"""

import argparse
import re
import sys
from pathlib import Path

MANUSCRIPT = Path(__file__).resolve().parent / "manuscript"
NBSP = " "

# vous の命令形。-ez で終わる語を文頭で拾い、不規則形を足す。副詞などの -ez は除く。
NOT_VERBS = {"Chez", "Assez", "Nez"}
IMPERATIVE = re.compile(r"(?:^|(?<=[.!?:»] ))\*{0,2}([A-ZÉÈÀ][a-zéèêëàâîïôûùç]+ez|Dites|Faites|Soyez|Ayez|Sachez)\b")
CONDITIONAL = re.compile(r"^\*{0,2}\S+[^.!?]{0,90}, (et|puis)\b")

BANNED = re.compile(
    r"univers\b|vibration|manifester|loi de l'attraction|moi supérieur|vrai moi|mission d'âme|"
    r"éveil|garanti|changera votre vie|intuition|votre instinct",
    re.IGNORECASE,
)
BANNED_ALLOWED = "ni univers ni vibrations"

LOOSE_SPACE = re.compile(r"(?<=\S) ([;:!?])|« |(?<=\S) »")


def is_step_or_quote(line):
    return bool(re.match(r"^\d+\. ", line)) or line.startswith(("- ", ">", "|"))


def check():
    findings = []
    for path in sorted(MANUSCRIPT.glob("*.md")):
        for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            line = raw.strip()
            if LOOSE_SPACE.search(line) and not line.startswith(("```", "http")):
                findings.append((path.name, number, "空白", line[:78]))
            if is_step_or_quote(line):
                continue
            if BANNED.search(line) and BANNED_ALLOWED not in line:
                findings.append((path.name, number, "禁止語", line[:78]))
            heading = line.startswith("#")
            body = line.lstrip("# ") if heading else line
            for match in IMPERATIVE.finditer(body):
                if match.group(1) in NOT_VERBS:
                    continue
                fragment = body[match.start():match.start() + 95]
                if CONDITIONAL.match(fragment):
                    continue
                # 「Avez-vous déjà lu … ?」は倒置の疑問文で、命令ではない
                end = re.search(r"[.!?]", body[match.start():])
                if end and end.group() == "?":
                    continue
                findings.append((path.name, number, "命令形(見出し)" if heading else "命令形", fragment[:78]))
    return findings


def fix():
    changed = 0
    for path in sorted(MANUSCRIPT.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        new = re.sub(r"(?<=\S) ([;:!?])", NBSP + r"\1", text)
        new = new.replace("« ", "«" + NBSP)
        new = re.sub(r"(?<=\S) »", NBSP + "»", new)
        # Markdown の記法(URL の : や見出しの後ろ)を壊さないよう、行頭の記号は触らない
        if new != text:
            path.write_text(new, encoding="utf-8")
            changed += 1
    return changed


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--fix", action="store_true", help="約物の前の空白を U+00A0 に置き換える")
    parser.add_argument("--quiet", action="store_true", help="件数だけ出す")
    args = parser.parse_args(argv)

    if args.fix:
        print(f"{fix()} ファイルの空白を直しました")

    findings = check()
    if not args.quiet:
        for name, number, kind, text in findings:
            print(f"  {kind}  {name}:{number}  {text}")
    print(f"{len(findings)} 件" if findings else "0 件 — 命令形・禁止語・約物の空白、いずれも問題なし")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
