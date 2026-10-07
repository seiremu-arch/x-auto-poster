#!/usr/bin/env python3
"""ポルトガル語(ブラジル)版の文体検査: 命令形・禁止語・地域語・性の一致・引用符・書きかけの言い直し。

`você` で書くので、命令形は接続法の形(「Escreva」「Anote」)になり、直説法(「escreve」)と綴りが違う。
文頭にこの形が来たら、手順の外の命令とみなす。「Coloque os nomes de volta, e …」のような帰結の説明は許す。

地域: ブラジルのポルトガル語で書く(Vault `1a18342985`)。ポルトガルの語と形を拾う。
性の一致: 読者も著者も中立(Vault `0045c354b1` / `dba7c10f3f`)。イタリア語版とフランス語版で、
「検査の0件は検査の範囲の中での0件」と分かっているので、全章のあとで性に絞った読み返しもする。

    python books/inner-voice-pt/check_style.py
    python books/inner-voice-pt/check_style.py --quiet   # 件数だけ
"""

import argparse
import re
import sys
from pathlib import Path

MANUSCRIPT = Path(__file__).resolve().parent / "manuscript"

# você の命令形(接続法現在の三人称単数と同形)
VERBS = (
    "Escreva|Pegue|Coloque|Ponha|Marque|Conte|Copie|Espere|Olhe|Escolha|Procure|Mantenha|Deixe|"
    "Experimente|Sente-se|Levante-se|Caminhe|Ande|Repita|Divida|Risque|Circule|Reescreva|Volte|Nomeie|"
    "Feche|Abra|Use|Leia|Releia|Ajuste|Afaste|Responda|Pergunte|Decida|Lembre|Lembre-se|Esqueça|Pense|"
    "Pare|Invente|Tire|Desligue|Respire|Observe|Diga|Faça|Vá|Fique|Anote|Peça|Separe|Corte|Tente|"
    "Guarde|Jogue|Comece|Troque|Fale|Note|Repare|Confie|Desista|Evite|Aceite|Recuse|Mande|Envie"
)
IMPERATIVE = re.compile(rf"(?:^|(?<=[.!?:] )|(?<=[.!?:]\*\* ))\*{{0,2}}({VERBS})(?![\w-])")
# 文中の「…, pare / não pare …」のような否定の命令も拾う(イタリア語版で文中の命令形を取りこぼした)
NEG_IMPERATIVE = re.compile(rf"(?:^|(?<=[.!?:,;] )|(?<=[.!?:]\*\* ))\*{{0,2}}[Nn]ão ({VERBS.lower()})(?![\w-])")
CONDITIONAL = re.compile(rf"^\*{{0,2}}({VERBS})(?![\w-])[^.!?]{{0,90}}, (e|aí)\b")
ITALIC = re.compile(r"(?<!\*)\*(?!\*)[^*]+\*(?!\*)")   # 斜体は頭の中の声の台詞

BANNED = re.compile(
    r"\buniverso\b|vibraç|\bmanifestar|lei da atração|eu superior|verdadeiro eu|missão da alma|\benergia|"
    r"despertar espiritual|subconsciente|\bintuição|seu instinto|\bgarantid|mudar a sua vida|mudar sua vida|\bcomprovad",
    re.IGNORECASE,
)
BANNED_ALLOWED = "não há universo nem vibrações"

REGIONAL = re.compile(
    r"\b(telemóvel|ecrã|autocarro|comboio|frigorífico|pequeno-almoço|rapariga|miúdo|fixe|bué|farol|"
    r"teu|tua|teus|tuas|contigo|tu)\b|casa de banho"
    r"|\b(estou|está|estava|estão|estavam|estive|fico|fica|ficou|ficava|continuo|continua|ando|anda|andava) a "
    r"[a-zç]+(ar|er|ir)\b",   # estar a + 不定詞(ポルトガルの進行形)
    re.IGNORECASE,
)

_GENDERED = (r"(\w+(ado|ada|ido|ida|oso|osa)|sozinho|sozinha|cansado|cansada|certo|certa|seguro|segura|"
             r"pronto|pronta|quieto|quieta|calmo|calma|tranquilo|tranquila|satisfeito|satisfeita|preso|presa|"
             r"convicto|convicta|atento|atenta|surpreso|surpresa|obrigado|obrigada|sujeito|sujeita|"
             r"exausto|exausta|aberto|aberta|parado|parada|feito|feita|morto|morta|tenso|tensa|leve|pesado|pesada|"
             r"preciso|precisa|exato|exata|honesto|honesta|sincero|sincera|franco|franca)")
_MODS = r"((muito|tão|mais|meio|um pouco|bem|já|ainda|sempre|realmente|bastante|demais|quase|completamente)\s+){0,2}"
GENDER = re.compile(
    # 一人称だけの形。estava / era / ficava / me sentia などは三人称と同形なので、前に eu があるときだけ見る
    # (主語を省いた「Estava cansado」は拾えない。読み返しで拾う)
    r"\b(estou|estive|fiquei|fico|sou|fui|me senti|me sinto|continuo|permaneci|ando|não estou|não fiquei|não sou|não fui|"
    r"eu (não )?(estava|era|ficava|me sentia|continuava|andava)|"
    r"você está|você estava|você fica|você ficou|você ficava|você é|você era|você se sente|você se sentiu|você se sentia|"
    r"você não está|você não fica|você não é)\s+" + _MODS + _GENDERED.replace("leve|", "") + r"\b"
    r"|\b(eu|você) (mesmo|mesma)\b|\btodos (os|aqueles) que\b|\bobrigad[oa] (por|pela|pelo)\b"
    # 不定詞・現在分詞を挟む形(「Quero ser preciso」「Sendo honesto」)。第4章で取りこぼした
    r"|\b(quero|queria|vou|ia|preciso|precisava|tento|tentei|posso|pude) (ser|ficar|estar|me sentir) " + _MODS + _GENDERED + r"\b"
    r"|\b[Ss]endo (honesto|honesta|sincero|sincera|franco|franca|justo|justa|preciso|precisa|exato|exata)\b",
    re.IGNORECASE,
)

DRAFT = re.compile(r"…\s*(não|melhor dizendo|ou melhor|digamos)\s*:", re.IGNORECASE)


def is_step_or_quote(line):
    return bool(re.match(r"^\d+\. ", line)) or line.startswith(("- ", ">", "|"))


def check():
    findings = []
    for path in sorted(MANUSCRIPT.glob("*.md")):
        for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            line = raw.strip()
            plain = line.replace("~~", "")
            for match in REGIONAL.finditer(plain):
                findings.append((path.name, number, "地域語", f"“{match.group(0)}” {line[:60]}"))
            if GENDER.search(plain):  # 引用ブロックのノートも著者自身の言葉なので対象
                findings.append((path.name, number, "性の一致", line[:78]))
            if '"' in line:
                findings.append((path.name, number, "引用符", line[:78]))
            elif line.count("“") != line.count("”"):
                findings.append((path.name, number, "引用符の対", line[:78]))
            if DRAFT.search(line):
                findings.append((path.name, number, "言い直し", line[:78]))
            if is_step_or_quote(line):
                continue
            if BANNED.search(line) and BANNED_ALLOWED not in line:
                findings.append((path.name, number, "禁止語", line[:78]))
            heading = line.startswith("#")
            body = ITALIC.sub("", line.lstrip("# ") if heading else line)
            for pattern in (IMPERATIVE, NEG_IMPERATIVE):
                for match in pattern.finditer(body):
                    fragment = body[match.start():match.start() + 95]
                    if pattern is IMPERATIVE and CONDITIONAL.match(fragment):
                        continue
                    end = re.search(r"[.!?]", body[match.start():])
                    if end and end.group() == "?":
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
    print(f"{len(findings)} 件" if findings else "0 件 — 命令形・禁止語・地域語・性の一致・引用符・言い直し、いずれも問題なし")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
