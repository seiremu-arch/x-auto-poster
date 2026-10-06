#!/usr/bin/env python3
"""フランス語版の文体検査: 手順の外に出た命令形・禁止語・約物の前の空白。

`vous` で書くと決めた(Vault `e778004e3b`)ことの反証条件が命令形の検査。ドイツ語版では
`du` の命令形が章末と見出しに14件漏れた(`7586251f89`)。フランス語版は最初の章から回す。

「Remettez les noms, et cela redevient …」のような**条件の言い方**は、命令ではなく帰結の
説明なので許す。落とすのは手順の外にある**裸の指示**だけ。

    python books/inner-voice-fr/check_style.py          # 検査(見つかったら終了コード1)
    python books/inner-voice-fr/check_style.py --fix    # ; : ! ? の前と « » の内側を U+00A0 にする

性の一致(Vault `0045c354b1` / `dba7c10f3f`):
- 読者に向けた一致(vous êtes allé など)は失敗として数える
- 著者の一人称の一致(j'ai été surpris など)も失敗にする。著者は中立と決まった(2026-10-06)
- 総称の on に性で変わる形が続くもの(quand on est fatigué)も失敗にする
"""

import argparse
import re
import sys
from pathlib import Path

MANUSCRIPT = Path(__file__).resolve().parent / "manuscript"
NBSP = " "

# vous の命令形。-ez で終わる語を文頭で拾い、不規則形を足す。副詞などの -ez は除く。
NOT_VERBS = {"Chez", "Assez", "Nez"}
IMPERATIVE = re.compile(r"(?:^|(?<=[.!?:»] )|(?<=[.!?:]\*\* ))\*{0,2}([A-ZÉÈÀ][a-zéèêëàâîïôûùç]+ez|Dites|Faites|Soyez|Ayez|Sachez)\b")
CONDITIONAL = re.compile(r"^\*{0,2}\S+[^.!?]{0,90}, (et|puis)\b")

BANNED = re.compile(
    # 語の途中には当てない(「réveil」の中の「éveil」、「universel」の中の「univers」)
    r"\buniverse?\b|\bvibration|\bmanifester|loi de l'attraction|moi supérieur|vrai moi|mission d'âme|"
    r"\béveil|\bgaranti|changera votre vie|\bintuition|votre instinct",
    re.IGNORECASE,
)
BANNED_ALLOWED = "ni univers ni vibrations"

# 性で形が変わる過去分詞・形容詞(男性形。女性形は -e が付くので当たらない)
_MASC = (r"(surpris|plaint|rentré|allé|resté|devenu|revenu|venu|parti|passé|sorti|arrivé|tombé|"
         r"sûr|seul|occupé|assis|débordé|endormi|senti|obligé|indécis|content|fatigué|épuisé|"
         r"prêt|convaincu|habitué|perdu|certain|lourd|léger|souvenu|arrêté|servi|tenu|garé|invité|bruyant|arrangé)")
READER_GENDER = re.compile(r"\bvous\s+(êtes|serez|étiez|soyez|seriez|vous êtes|vous serez|vous étiez|vous seriez|avez été|a rendu)\s+"
                           r"(\w+\s+)?" + _MASC + r"\b|\bvous\s+n'êtes\s+pas\s+" + _MASC + r"\b", re.IGNORECASE)
AUTHOR_GENDER = re.compile(r"\b(je suis|j'étais|je me suis|j'ai été|je serai|je reste|m'étais|me suis|"
                           r"je ne suis (pas|plus|jamais)|je ne me suis (pas|plus|jamais)|je n'étais (pas|plus)|je n'ai pas été|"
                           r"je m'(en|y) suis|me rend|me rendait)\s+"
                           r"(\w+\s+){0,3}?" + _MASC + r"\b|\btout seul\b|\bLaissé à moi-même\b|"
                           r"\bm'(a|ont|avait|avaient) (blessé|humilié|surpris|vexé|déçu|étonné|touché)\b|"
                           r"\bje ne suis pas (fait|qualifié|devenu)\b|\bje me sentais (\w+\s+)?" + _MASC + r"\b", re.IGNORECASE)
# 総称の on に性で変わる形が続くもの(「quand on est fatigué」)。読者の性(Vault 0045c354b1)の残り
GENERIC_ON = re.compile(r"\bon (est|reste|restait|était)\s+(\w+\s+)?" + _MASC + r"\b", re.IGNORECASE)

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
            if READER_GENDER.search(line):
                findings.append((path.name, number, "性の一致(読者)", line[:78]))
            plain = line.replace("~~", "")  # 抹消線で語が切れて当たらなくなるのを防ぐ
            if AUTHOR_GENDER.search(plain):  # 著者は中立と決まった(2026-10-06、Vault dba7c10f3f)
                findings.append((path.name, number, "性の一致(著者)", line[:78]))
            if GENERIC_ON.search(plain):
                findings.append((path.name, number, "性の一致(総称のon)", line[:78]))
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
    print(f"{len(findings)} 件" if findings else "0 件 — 命令形・禁止語・約物の空白・読者と著者の性、いずれも問題なし")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
