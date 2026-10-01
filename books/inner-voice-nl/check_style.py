#!/usr/bin/env python3
"""オランダ語版の文体検査: 命令形・禁止語・地域語・引用符・書きかけの言い直し。

オランダ語の命令形は動詞の語幹(「Schrijf」「Tel」)で、一人称の現在形と同じ形になる。
見分けるのは、**文頭の語幹のすぐ後ろに主語(je / jij / ik / we / u …)が無い**こと。
「Schrijf je het op, dan …」は主語つきの倒置で、条件の言い方なので命令ではない。
「Zet de namen terug, en …」のような帰結の説明も、ドイツ語版と同じく許す。

Amazon.nl はオランダとフランデレンの両方の読者が使うので、片方でしか通じない語を拾う
(スペイン語版の中立化 `cb294d65c0` と同じ考え方)。

性の一致の検査は無い。オランダ語は形容詞・分詞が人の性で変わらない。残るのは読者を\n「wie …, hij」で受ける総称の男性形だけなので、それを拾う。

    python books/inner-voice-nl/check_style.py
    python books/inner-voice-nl/check_style.py --quiet   # 件数だけ
"""

import argparse
import re
import sys
from pathlib import Path

MANUSCRIPT = Path(__file__).resolve().parent / "manuscript"

VERBS = (
    "Schrijf|Pak|Neem|Leg|Zet|Maak|Ga|Houd|Hou|Zeg|Tel|Vraag|Kijk|Lees|Kies|Zoek|Probeer|Blijf|Kom|"
    "Wacht|Antwoord|Schakel|Gebruik|Let|Vergelijk|Vervang|Ruim|Beslis|Laat|Sluit|Vergeet|Trek|Geef|"
    "Sta|Zit|Adem|Bel|Noteer|Markeer|Omcirkel|Streep|Herhaal|Denk|Luister|Stop|Doe|Splits|Deel|"
    "Verdeel|Noem|Kopieer|Wees|Onthoud|Bedenk|Schrap|Draai|Loop|Wandel|Ga|Leg|Spreek|Stel|Begin"
)
SUBJECT = r"(jij|u|ik|we|wij|hij|zij)\b"
# 「ze」は付けない: 語幹+ze は目的語(Tel ze op)。
# 「je」も付けない: 「Lees je klachten niet」の je は所有格で、これは命令形。
# 主語の je で倒置した「Schrijf je het op, dan …」は CONDITIONAL、「Kijk je even?」は疑問文の扱いで外れる。
# 文頭(行頭 / 文末記号のあと)に来る語幹。後ろに主語が来たら倒置なので除く。
# 「**Ten tweede: …** Denk aan …」のように、太字の閉じのあとに来る文頭も見る
IMPERATIVE = re.compile(rf"(?:^|(?<=[.!?:] )|(?<=[.!?:]\*\* ))\*{{0,2}}({VERBS})\b(?! {SUBJECT})(?!\?)")
# 「命令形 ..., en/dan ...」= 条件の言い方。命令ではないので許す。
CONDITIONAL = re.compile(rf"^\*{{0,2}}({VERBS})\b[^.!?]{{0,90}}, (en|dan)\b")
ITALIC = re.compile(r"(?<!\*)\*[^*]+\*(?!\*)")   # 斜体は頭の中の声の台詞。命令形でも著者の指示ではない

BANNED = re.compile(
    r"universum|trilling|manifester|wet van (de )?aantrekking|hoger zelf|ware zelf|zielsmissie|"
    r"\benergie|ontwaken|onderbewust|intuïtie|onderbuik|gegarandeerd|verandert je leven|bewezen",
    re.IGNORECASE,
)
# 序文の宣言だけは残す(使わないと宣言する文なので)。
BANNED_ALLOWED = "geen universum en geen trillingen"

REGIONAL = re.compile(
    r"\b(gsm|frigo|pinnen|gepind|pint|mobieltje|zetel|plezant|goesting|efkes|allez|amai|"
    r"ambetant|seffens|gij|ge|da's|nen|ne)\b",
    re.IGNORECASE,
)

# 読者を「wie …」で受けて hij / zijn / hem で続ける総称の男性形(Vault `0045c354b1` のオランダ語での残り)
# 「zijn」は動詞(〜である)と同形なので、所有格と分かる形だけ拾う
GENERIC = re.compile(r"\bWie\b[^.!?]*\b(hij|hem|zijn (eigen|hele|leven|hoofd|lichaam))\b")

# 書きながら言い直した跡(イタリア語版で四度残した。オランダ語でも最初から見る)
DRAFT = re.compile(r"…\s*(nee|beter gezegd|of eigenlijk|laat ik zeggen|ik bedoel)\s*:", re.IGNORECASE)


def is_step_or_quote(line):
    return bool(re.match(r"^\d+\. ", line)) or line.startswith(("- ", ">", "|"))


def check():
    findings = []
    for path in sorted(MANUSCRIPT.glob("*.md")):
        for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            line = raw.strip()
            for match in REGIONAL.finditer(line):
                findings.append((path.name, number, "地域語", f"“{match.group(0)}” {line[:60]}"))
            if '"' in line:
                findings.append((path.name, number, "引用符", line[:78]))
            elif line.count("“") != line.count("”"):
                findings.append((path.name, number, "引用符の対", line[:78]))
            if GENERIC.search(line):
                findings.append((path.name, number, "総称の hij", line[:78]))
            if DRAFT.search(line):
                findings.append((path.name, number, "言い直し", line[:78]))
            if is_step_or_quote(line):
                continue
            if BANNED.search(line) and BANNED_ALLOWED not in line:
                findings.append((path.name, number, "禁止語", line[:78]))
            heading = line.startswith("#")
            body = ITALIC.sub("", line.lstrip("# ") if heading else line)
            for match in IMPERATIVE.finditer(body):
                fragment = body[match.start():match.start() + 95]
                if CONDITIONAL.match(fragment):
                    continue
                end = re.search(r"[.!?]", body[match.start():])
                if end and body[match.start() + end.start()] == "?":
                    continue   # 疑問文(「Kijk je …?」の形は主語で除かれるが、念のため)
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
    print(f"{len(findings)} 件" if findings else "0 件 — 命令形・禁止語・地域語・引用符・総称の hij・言い直し、いずれも問題なし")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
