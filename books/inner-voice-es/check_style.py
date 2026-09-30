#!/usr/bin/env python3
"""スペイン語版の文体検査。

五つを見る。見つかったら終了コード1。

- 命令形 — 手順の外の裸の指示(条件の言い方「…, y …」は許す)
- 禁止語 — 検証できない語と効果の断定
- 地域語 — 中立スペイン語から外れる語(Vault `cb294d65c0`)
- 性の一致 — 著者か読者に文法上の性が出る言い方(Vault `c36e89b074`)
- ¿ ¡ — 開きの記号が閉じの記号と同じ数あるか

    python books/inner-voice-es/check_style.py
    python books/inner-voice-es/check_style.py --quiet
"""

import argparse
import re
import sys
from pathlib import Path

MANUSCRIPT = Path(__file__).resolve().parent / "manuscript"

# tú の命令形(文頭に来るもの)。tú の命令形は三人称現在と同形なので、同形異義が多い。
# 「Para」(前置詞)と「Corta」(形容詞「短い」)は区別できないので入れない。
# 主語を省いた三人称(「…no usa X. Usa Y.」)も当たるので、そこは語順で避ける。
VERBS = (
    "Escribe|Toma|Pon|Anota|Cuenta|Marca|Copia|Espera|Mira|Di|Haz|Elige|Busca|Guarda|Deja|"
    "Prueba|Siéntate|Levántate|Camina|Repite|Divide|Tacha|Rodea|Reescribe|Vuelve|Nombra|Cierra|"
    "Abre|Usa|Lee|Relee|Coloca|Programa|Aleja|Responde|Pregunta|Decide|Recuerda|Olvida|Piensa|"
    "Intenta|Cambia|Inventa|Quita|Apaga|Detente|Respira|Fíjate|Observa|Vuelve"
)
IMPERATIVE = re.compile(rf"(?:^|(?<=[.!?:»] ))\*{{0,2}}({VERBS})\b")
CONDITIONAL = re.compile(rf"^\*{{0,2}}({VERBS})\b[^.!?]{{0,90}}, (y|entonces)\b")

BANNED = re.compile(
    r"\buniverso\b|\bvibraci|\bmanifestar|ley de (la )?atracción|yo superior|verdadero yo|"
    r"misión del alma|despertar espiritual|\bgarantizad|cambiará tu vida|\bcomprobad|\bintuición|tu instinto",
    re.IGNORECASE,
)
BANNED_ALLOWED = "no hay universo ni vibraciones"

REGIONAL = re.compile(
    r"\b(móvil|celular|coche|carro|ordenador|computadora|ahorita|guay|chévere|chido|"
    r"coger|cogí|zumo|jugo|conducir|manejar|aparcar|estacionar|departamento)\b"
    r"|\b[Vv]ale(?=[,.!])"                    # 相づちの「¡Vale!」だけ。「vale la pena」は中立
    r"|\b\w+(áis|éis)\b"                      # vosotros
    r"|\bvos\b|\b(sabés|tenés|podés|querés|sos)\b",  # voseo
    re.IGNORECASE,
)
# vosotros の語尾に見えて、そうでないもの
REGIONAL_OK = {"seis", "veintiséis", "dieciséis", "país", "maíz", "jamáis"}

# 著者(yo)か読者(tú)の述語に、性で変わる形容詞・分詞が来ているもの
GENDER = re.compile(
    r"\b(estoy|estaba|estuve|me sentí|me siento|me quedé|quedé|me puse|soy|era|fui|"
    r"estás|estabas|estuviste|te sientes|te sentiste|te quedas|te quedaste|eres)\s+"
    r"(muy\s+|tan\s+|más\s+|un poco\s+|bastante\s+)?"
    r"(\w+(ado|ada|ados|adas|ido|ida|idos|idas|oso|osa)|solo|sola|seguro|segura|listo|lista|"
    r"contento|contenta|cansado|cansada|dormido|dormida|obligado|obligada|pesado|pesada|ligero|ligera)\b",
    re.IGNORECASE,
)


MARKER = re.compile(r"\*\*\?\*\*")                      # 「わからない」の記号 **?** は疑問符ではない
ITALIC = re.compile(r"(?<!\*)\*(?!\*)[^*]+\*(?!\*)")      # 斜体 = 声の台詞の引用。地の文の命令ではない


def is_step_or_quote(line):
    return bool(re.match(r"^\d+\. ", line)) or line.startswith(("- ", ">", "|"))


def check():
    findings = []
    for path in sorted(MANUSCRIPT.glob("*.md")):
        for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            line = raw.strip()
            if not line:
                continue
            marks = MARKER.sub("", line)
            if marks.count("¿") != marks.count("?") or marks.count("¡") != marks.count("!"):
                findings.append((path.name, number, "¿¡", line[:78]))
            for match in REGIONAL.finditer(line):
                if match.group(0).lower() not in REGIONAL_OK:
                    findings.append((path.name, number, "地域語", f"«{match.group(0)}» {line[:60]}"))
            if GENDER.search(line):  # 引用ブロックのノートも著者自身の言葉なので対象にする
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
                findings.append((path.name, number, "命令形(見出し)" if heading else "命令形", fragment[:78]))
    return findings


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--quiet", action="store_true", help="件数だけ出す")
    args = parser.parse_args(argv)
    findings = check()
    if not args.quiet:
        for name, number, kind, text in findings:
            print(f"  {kind}  {name}:{number}  {text}")
    print(f"{len(findings)} 件" if findings else "0 件 — 命令形・禁止語・地域語・性の一致・¿¡、いずれも問題なし")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
