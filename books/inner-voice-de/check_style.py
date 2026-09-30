#!/usr/bin/env python3
"""ドイツ語版の文体検査: 手順の外に出た命令形を落とす。

`du` で書くと決めた(Vault `7586251f89`)ことの反証条件がこれ。命令形が手順の節の外に
出ていたら、距離が近くなったぶんが指示に変わっている。

命令形を全部禁じると、ドイツ語としては不自然になる。「Setz die Namen zurück, und ...」の
ような**条件の言い方**(「〜すると、〜になる」)は命令ではなく帰結の説明なので許す。
落とすのは、手順の外にある**裸の指示**だけ。

    python books/inner-voice-de/check_style.py          # 命令形と禁止語
    python books/inner-voice-de/check_style.py --quiet   # 件数だけ
"""

import argparse
import re
import sys
from pathlib import Path

MANUSCRIPT = Path(__file__).resolve().parent / "manuscript"

VERBS = (
    "Schreib|Setz|Nimm|Mach|Leg|Stell|Geh|Halt|Sag|Zähl|Frag|Prüf|Notier|Markier|Übertrag|Teil|"
    "Kreis|Streich|Wiederhol|Denk|Sieh|Hör|Lies|Wähl|Bau|Erfind|Behalt|Such|Find|Probier|Bring|"
    "Bleib|Komm|Warte|Antworte|Tausch|Schalt|Reduzier|Trenn|Beginn|Benutz|Verwend|Beobachte|Achte|"
    "Vergleich|Ersetz|Räum|Press|Kürz|Entscheid|Wechsel|Lass|Trag|Öffne|Schließ|Vergiss|Form|Zieh|"
    "Gib|Steh|Sitz|Atme|Wart|Ruf"
)
# 文頭(行頭 / 句点のあと)に来る命令形。`\b` が無いと「Zählen」「Sagen」を拾う。
IMPERATIVE = re.compile(rf"(?:^|(?<=[.!?:] ))\*{{0,2}}({VERBS})e?\b")
# 「命令形 ..., und/dann ...」= 条件の言い方。命令ではないので許す。
CONDITIONAL = re.compile(rf"^\*{{0,2}}({VERBS})e?\b[^.!?]{{0,90}}, (und|dann)\b")

BANNED = re.compile(
    "Universum|Schwingung|manifestier|Gesetz der Anziehung|höheres Selbst|wahres Selbst|"
    "Seelenplan|Erwachen|garantiert|verändert dein Leben|Intuition|Bauchgefühl",
    re.IGNORECASE,
)
# 序文の宣言だけは残す(使わないと宣言する文なので)。
BANNED_ALLOWED = "Hier kommt kein Universum vor"


def is_step_or_quote(line):
    return bool(re.match(r"^\d+\. ", line)) or line.startswith(("- ", ">", "|"))


def check():
    findings = []
    for path in sorted(MANUSCRIPT.glob("*.md")):
        for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            line = raw.strip()
            if is_step_or_quote(line):
                continue
            if BANNED.search(line) and BANNED_ALLOWED not in line:
                findings.append((path.name, number, "禁止語", line[:78]))
            heading = line.startswith("#")
            body = line.lstrip("# ") if heading else line
            for match in IMPERATIVE.finditer(body):
                fragment = body[match.start():match.start() + 95]
                if CONDITIONAL.match(fragment):
                    continue
                where = "命令形(見出し)" if heading else "命令形"
                findings.append((path.name, number, where, fragment[:78]))
    return findings


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--quiet", action="store_true", help="件数だけ出す")
    args = parser.parse_args(argv)

    findings = check()
    if not args.quiet:
        for name, number, kind, text in findings:
            print(f"  {kind}  {name}:{number}  {text}")
    print(f"{len(findings)} 件" if findings else "0 件 — 手順の外に命令形はなく、禁止語も出ていません")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
