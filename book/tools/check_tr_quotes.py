#!/usr/bin/env python3
"""巻をまたいで引用される文が、一字一句同じかを検査する。

使い方:
    python3 book/tools/check_en_quotes.py

第二巻第八話（夢の海）は、保管庫に残った記録として、第一巻の各話と
第二巻第六話に出てきた文をそのまま引用している。原文では同じ文字列なので、
訳文でも同じでなければ繋がりが切れる。通しで読んでも「似ているが少し違う」は
見落とすので、文字列一致で確かめる。言語ごとに別々に見る。

日本語側で同じであることも併せて確認する。原文がずれていれば、
訳文を揃えても意味がない。ただし、地の文と記録の抜粋では中黒と読点が
入れ替わる（光、痛み、閉じる ↔ 光・痛み・閉じる）。これは文体の違いで
あって不一致ではないので、区切り記号は正規化してから比べる。
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def normalise(s: str) -> str:
    """中黒と読点の違いを吸収する。地の文と記録の抜粋で入れ替わるため。"""
    return s.replace("\u30fb", "\u3001")


# (説明, 日本語の文字列, {言語: 訳文}, 出現すべきファイル（言語接頭辞なし）)
QUOTES = [
    (
        "読み手の欄外記載（第一巻XII → 第二巻VIII）",
        "ただし本日、被験者七号の夢に、私の下宿の階段が出た",
        {
            "en": "However, the stair of my lodgings appeared today "
                  "in Subject 7's dream.",
            "de": "Allerdings erschien heute im Traum von Proband sieben "
                  "die Treppe meiner Pension.",
            "es": "Sin embargo, hoy apareci\u00f3 en el sue\u00f1o del sujeto "
                  "siete la escalera de mi pensi\u00f3n.",
            "fr": "Cependant, l'escalier de ma pension est apparu "
                  "aujourd'hui dans le rêve du sujet sept.",
            "it": "Tuttavia, oggi nel sogno del soggetto sette è comparsa "
                  "la scala della mia pensione.",
            "nl": "Vandaag echter verscheen in de droom van proefpersoon "
                  "zeven de trap van mijn pension.",
            "pt": "No entanto, hoje apareceu no sonho do sujeito sete "
                  "a escada da minha pens\u00e3o.",
        },
        [("1", "12"), ("2", "08")],
    ),
    (
        "被害回復拒否の自由記述（第二巻VI → 第二巻VIII）",
        "兄が入れたものだと分かっている。分かっていても、思ってしまう",
        {
            "en": "I know it is something my brother put there. "
                  "Knowing it, I feel it all the same.",
            "de": "Ich wei\u00df, dass es etwas ist, das mein Bruder "
                  "hineingelegt hat. Ich wei\u00df es, und ich empfinde "
                  "es trotzdem.",
            "es": "S\u00e9 que es algo que mi hermano me meti\u00f3 dentro. "
                  "Lo s\u00e9, y lo siento igual.",
            "fr": "Je sais que c'est quelque chose que mon frère y a mis. "
                  "Je le sais, et je le ressens quand même.",
            "it": "So che è una cosa che mio fratello mi ha messo dentro. "
                  "Lo so, e lo sento comunque.",
            "nl": "Ik weet dat het iets is wat mijn broer erin heeft gezet. "
                  "Ik weet het, en ik voel het toch.",
            "pt": "Sei que \u00e9 uma coisa que meu irm\u00e3o colocou ali. "
                  "Sei disso, e sinto do mesmo jeito.",
        },
        [("2", "06"), ("2", "08")],
    ),
    (
        "辞退の自由記述（第一巻II → 第二巻VIII）",
        "蓮見律子は、待機期間中に自力で荷重を下げ、処置を辞退した",
        {
            "en": "Hasumi Ritsuko lowered her own load during the waiting "
                  "period and withdrew from the procedure.",
            "de": "Hasumi Ritsuko hat w\u00e4hrend der Wartezeit ihre Last "
                  "aus eigener Kraft gesenkt und ist von der Bearbeitung "
                  "zur\u00fcckgetreten.",
            "es": "Hasumi Ritsuko baj\u00f3 su propia carga durante el "
                  "periodo de espera y se retir\u00f3 del tratamiento.",
            "fr": "Hasumi Ritsuko a abaissé sa propre charge pendant le "
                  "délai d'attente et a renoncé au traitement.",
            "it": "Hasumi Ritsuko ha abbassato da sé il proprio carico "
                  "durante il periodo d'attesa e ha rinunciato al "
                  "trattamento.",
            "nl": "Hasumi Ritsuko heeft tijdens de wachttijd op eigen kracht "
                  "haar lading verlaagd en heeft de behandeling afgewezen.",
            "pt": "Hasumi Ritsuko baixou a pr\u00f3pria carga por conta "
                  "pr\u00f3pria durante o per\u00edodo de espera e recusou "
                  "o procedimento.",
        },
        [("1", "02"), ("2", "08")],
    ),
    (
        "翻訳の不採用候補（第一巻IV → 第二巻VIII）",
        "光・痛み・閉じる",
        {"en": "light, pain, closing", "de": "Licht, Schmerz, Schlie\u00dfen",
         "es": "Luz, dolor, cerrar",
         "fr": "Lumière, douleur, fermer",
         "it": "Luce, dolore, chiudere",
         "nl": "Licht, pijn, sluiten",
         "pt": "Luz, dor, fechar"},
        [("1", "04"), ("2", "08")],
    ),
    (
        "翻訳の不採用候補・その二（第一巻IV → 第二巻VIII）",
        "動く・止まる・分からない",
        {"en": "moving, stopping, not knowing",
         "de": "Bewegen, Anhalten, Nichtwissen",
         "es": "Moverse, detenerse, no saber",
         "fr": "Bouger, s'arrêter, ne pas savoir",
         "it": "Muoversi, fermarsi, non sapere",
         "nl": "Bewegen, stoppen, niet weten",
         "pt": "Mover, parar, n\u00e3o saber"},
        [("1", "04"), ("2", "08")],
    ),
]

LANGS = ["en", "de", "es", "fr", "it", "nl", "pt"]

# 語彙表の「定型句」。原文が意図して繰り返す文は、訳文でも一字一句同じに
# 出なければならない。どの語彙表にもそう書いてあるが、守られているかを
# 見る仕組みがなかった。英語版第一巻で、第一話 "set down the water" に対し
# 第九話が "pour the water" になっていて、通読でしか見つけられなかった。
#
# 上の QUOTES と違い、出現すべきファイルは決め打ちにしない。原文にその文が
# 出る話を数え、同じ番号の訳文に対応する訳が出るかを見る。話を足しても
# 表を直さなくて済む。
#
# 載せるのは、文脈によらず同じ字面で出る句だけにする。たとえば
# 「記録にありません」は、校正官の台詞としてはどの言語でも一定だが、
# 地の文に埋まるときは英独仏で言い回しが変わる（西語の No consta は短いので
# 両方に出る）。「無視してよい値」も第二巻第八話では複数形になる。これらを
# 載せると、正しい訳を誤りとして鳴らす検査になるので載せない。四版すべてで
# 不変であることを確かめた三句だけを置く。残りは人が読んで見るしかない。
FORMULAE = [
    (
        "水を置く",
        "水を置くことだけだ",
        {
            "en": "set down the water",
            "de": "das Wasser hinstellen",
            "es": "dejar el agua",
            "fr": "poser l'eau",
            "it": "è posare l'acqua",
            "nl": "is het water neerzetten",
            "pt": "\u00e9 colocar a \u00e1gua",
        },
    ),
    (
        "要は換気",
        "要は換気",
        {
            "en": "is ventilation, basically",
            "de": "ist im Grunde L\u00fcften",
            "es": "es, en el fondo, ventilar",
            "fr": "au fond, c'est a\u00e9rer",
            "it": "in fondo, è dare aria",
            "nl": "in wezen ventileren",
            "pt": "no fundo, \u00e9 ventilar",
        },
    ),
    (
        "性別のない、湿度のない声",
        "性別のない、湿度のない声",
        {
            "en": "voice with no gender and no humidity",
            "de": "Stimme ohne Geschlecht und ohne Feuchtigkeit",
            "es": "voz sin g\u00e9nero y sin humedad",
            "fr": "voix sans genre et sans humidit\u00e9",
            "it": "voce senza genere e senza umidit\u00e0",
            "nl": "stem zonder geslacht en zonder vochtigheid",
            "pt": "voz sem g\u00eanero e sem umidade",
        },
    ),
]


def check_formulae() -> int:
    """定型句が、原文に出るすべての話で、訳文にも出るかを見る。"""
    problems = 0
    print("【定型句】")
    for label, ja, trs in FORMULAE:
        slots = []
        for vol in ("1", "2"):
            for p in sorted((ROOT / f"vol{vol}" / "stories")
                            .glob("[0-9][0-9]_*.txt")):
                if ja in p.read_text(encoding="utf-8"):
                    slots.append((vol, p.name[:2]))
        if not slots:
            problems += 1
            print(f"  \u00d7 {label}: 原文のどの話にも出ない（表のほうが古い）")
            continue

        missing = []
        for lang in LANGS:
            tr = trs.get(lang)
            if tr is None:
                missing.append(f"{lang}（対応文が未登録）")
                continue
            for vol, num in slots:
                d = ROOT / f"{lang}{vol}" / "stories"
                if not d.is_dir():
                    continue
                hits = sorted(d.glob(f"{num}_*.txt"))
                if not hits:
                    continue
                if tr.lower() not in hits[0].read_text(
                        encoding="utf-8").lower():
                    missing.append(str(hits[0].relative_to(ROOT)))

        n = len(slots)
        if missing:
            problems += len(missing)
            print(f"  \u00d7 {label}（原文 {n}話）")
            for m in missing:
                print(f"      見つからない: {m}")
        else:
            print(f"  \u25cb {label}（原文 {n}話）")
    return problems



def main() -> int:
    problems = 0

    for lang in LANGS:
        if not (ROOT / f"{lang}1").is_dir():
            continue
        print(f"【{lang}】")
        for label, ja, trs, slots in QUOTES:
            tr = trs.get(lang)
            if tr is None:
                # 言語を足した直後。落ちるのではなく、足りないと言う
                problems += 1
                print(f"  × {label}: この言語の対応文が未登録")
                continue
            missing = []
            for vol, num in slots:
                hits = sorted((ROOT / f"{lang}{vol}" / "stories")
                              .glob(f"{num}_*.txt"))
                if not hits:
                    missing.append(f"{lang}{vol}/{num}（ファイルなし）")
                    continue
                if tr.lower() not in hits[0].read_text(
                        encoding="utf-8").lower():
                    missing.append(str(hits[0].relative_to(ROOT)))

            if missing:
                problems += len(missing)
                print(f"  × {label}")
                print(f"      訳文: {tr}")
                for m in missing:
                    print(f"      見つからない: {m}")
            else:
                print(f"  ○ {label}")

    # 原文側も同じ文字列であることを確かめる。訳文を揃える前に原文を見る
    print("【原文】")
    for label, ja, _trs, slots in QUOTES:
        hits_n = 0
        for vol, num in slots:
            hits = sorted((ROOT / f"vol{vol}" / "stories").glob(f"{num}_*.txt"))
            if hits and normalise(ja) in normalise(
                    hits[0].read_text(encoding="utf-8")):
                hits_n += 1
        if hits_n != len(slots):
            problems += 1
            print(f"  × {label}: 原文側は {hits_n}/{len(slots)} ファイルにしかない")
        else:
            print(f"  ○ {label}")

    problems += check_formulae()

    print()
    print(f"要対応 {problems} 件" if problems else "引用の不一致なし")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
