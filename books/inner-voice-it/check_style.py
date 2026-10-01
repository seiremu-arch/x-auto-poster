#!/usr/bin/env python3
"""イタリア語版の文体検査。見つかったら終了コード1。

- 命令形 — 手順の外の裸の指示(条件の言い方「…, e …」と疑問文は許す)
- 禁止語 — 検証できない語と効果の断定
- 性の一致 — 著者か読者に文法上の性が出る言い方(Vault `0045c354b1` / `dba7c10f3f`)。
  イタリア語は essere を取る近過去(sono tornato/a)と再帰動詞(mi sono lamentato/a)でも
  性が出るので、スペイン語より当たりやすい

    python books/inner-voice-it/check_style.py
"""

import argparse
import re
import sys
from pathlib import Path

MANUSCRIPT = Path(__file__).resolve().parent / "manuscript"

# tu の命令形。-are 動詞は三人称現在と同形(「Usa」「Guarda」)なので、描写文では主語を書いて避ける
VERBS = (
    "Scrivi|Prendi|Metti|Segna|Conta|Copia|Aspetta|Guarda|Scegli|Cerca|Tieni|Lascia|Prova|"
    "Siediti|Alzati|Cammina|Ripeti|Dividi|Cancella|Cerchia|Riscrivi|Torna|Nomina|Chiudi|Apri|Usa|"
    "Leggi|Rileggi|Imposta|Allontana|Rispondi|Chiedi|Decidi|Ricorda|Dimentica|Pensa|Smetti|"
    "Inventa|Togli|Spegni|Fermati|Respira|Osserva|Rimetti|Annota|Fai|Di'"
)
IMPERATIVE = re.compile(rf"(?:^|(?<=[.!?:»] ))\*{{0,2}}({VERBS})(?![\w'])")
CONDITIONAL = re.compile(rf"^\*{{0,2}}({VERBS})(?![\w'])[^.!?]{{0,90}}, (e|poi)\b")
ITALIC = re.compile(r"(?<!\*)\*(?!\*)[^*]+\*(?!\*)")

BANNED = re.compile(
    r"\buniverso\b|\bvibrazion|\bmanifestare|legge dell'attrazione|sé superiore|vero sé|"
    r"missione dell'anima|risveglio spirituale|\bgarantit|cambierà la tua vita|\bintuizione|il tuo istinto",
    re.IGNORECASE,
)
BANNED_ALLOWED = "né universo né vibrazioni"

_GENDERED = (r"(\w+(ato|ata|ati|ate|ito|ita|iti|ite|uto|uta|uti|ute|oso|osa)|solo|sola|sicuro|sicura|"
             r"stanco|stanca|pronto|pronta|contento|contenta|convinto|convinta|rimasto|rimasta|"
             r"preso|presa|messo|messa|chiuso|chiusa|sceso|scesa|morto|morta|fermo|ferma|"
             r"pesante\b(?!x)|leggero|leggera|calmo|calma|tranquillo|tranquilla|obbligato|obbligata)")
GENDER = re.compile(
    r"\b(sono|ero|fui|sarò|sarei|mi sono|mi ero|mi sento|mi sentivo|mi sentii|resto|rimango|"
    r"sei|eri|sarai|saresti|ti sei|ti eri|ti senti|ti sentivi|resti|rimani)\s+"
    r"((molto|così|più|un po'|troppo|abbastanza|già|appena|mai|anche|ancora|sempre|davvero|proprio)\s+){0,2}"
    + _GENDERED.replace(r"pesante\b(?!x)|", "") + r"\b"
    + r"|\bda (solo|sola)\b",
    re.IGNORECASE,
)


def is_step_or_quote(line):
    return bool(re.match(r"^\d+\. ", line)) or line.startswith(("- ", ">", "|"))


def check():
    findings = []
    for path in sorted(MANUSCRIPT.glob("*.md")):
        for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            line = raw.strip()
            if not line:
                continue
            if GENDER.search(line):  # 引用ブロックのノートも著者自身の言葉なので対象
                findings.append((path.name, number, "性の一致", line[:78]))
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
                if end and end.group() == "?":
                    continue
                findings.append((path.name, number, "命令形(見出し)" if heading else "命令形", fragment[:78]))
    return findings


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)
    findings = check()
    if not args.quiet:
        for name, number, kind, text in findings:
            print(f"  {kind}  {name}:{number}  {text}")
    print(f"{len(findings)} 件" if findings else "0 件 — 命令形・禁止語・性の一致、いずれも問題なし")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
