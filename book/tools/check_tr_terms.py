#!/usr/bin/env python3
"""訳文の用語ゆれ・表記ゆれを機械で検査する。

使い方:
    python3 book/tools/check_tr_terms.py

GLOSSARY.md で固定した語の「やってはいけない変形」と、
言語ごとの綴り・組み方の規則を正規表現で当てる。十二話を通して読む代わりに、
ずれやすいところだけを機械に見せる。

人名も見る。原文に読み仮名がない姓は訳者が読みを決めることになり、
決め方を間違えても英文だけ読んでいるかぎり気づけない（杉本を Suginoto と
読んでいた事例がある）。原文に姓があるのに対応する英語名がない話は、
読みを決め直したか、落としたかのどちらかなので報告する。
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STORIES = sorted(ROOT.glob("[a-z][a-z][0-9]/stories/[0-9][0-9]_*.txt"))

# (説明, 正規表現) ─ 当たったら報告する
CHECKS_EN = [
    ("技師は technician（engineer は不可）", r"\bengineers?\b"),
    ("半色は half-shade（ハイフンなし・colour 綴りは不可）", r"\bhalf[ ]shade\b|\bhalf-?colou?r\b"),
    ("校正官は the Proofreader（大文字・ハイフンなし）", r"\bproofreader\b|\bProof[- ]reader\b"),
    ("情動荷重は affective load", r"\bemotional load\b|\bemotion load\b|\baffect load\b"),
    ("素片は fragment", r"\bshards?\b|\bsegments? of memory\b|\bmemory pieces?\b"),
    ("照合機は the Comparator", r"\bcollator\b|\bmatching machine\b"),
    ("残差は residual（residue は不可）", r"\bresidues?\b"),
    ("均し計画は the Levelling Plan（大文字）", r"\blevelling plan\b"),
    ("幸福指数は the Happiness Index（大文字）", r"\bhappiness index\b"),
    ("校正官の声は no humidity（moisture は不可）", r"no moisture in it"),
    ("水は paper cup（plastic/paper-cup は不可）", r"\bplastic cup\b|\bpaper-cup\b"),
    ("百分率は per cent（percent は不可）", r"\bpercent\b"),
    # size / prize / seize は正しい綴りなので、iz の前を4字以上に絞る
    ("英国綴り: -ise/-isation", r"\b\w{4,}iz(e|es|ed|ing|ation|ations)\b"),
    ("英国綴り: colour/behaviour/favour など", r"\bcolors?\b|\bbehavior\b|\bfavor(s|ed|ite)?\b|\bhonor\b"),
    ("英国綴り: centre/metre", r"\bcenters?\b|\bmeters?\b(?! of )"),
    ("英国綴り: defence/offence", r"\bdefense\b|\boffense\b"),
    ("英国綴り: grey", r"\bgray\b"),
    ("漢数字の残り（〇・一二三…）", r"[〇一二三四五六七八九十]"),
    ("全角文字の残り（字下げの U+3000 以外）", r"[^\x00-\x7F　—–‘’“”…¥]"),
    ("二重空白", r"[a-z,.] {2,}[A-Za-z]"),
    ("行末の空白", r"[ \t]+$"),
    ("曲がっていない引用符（本文は \" で統一）", r"[“”]"),
]

# ドイツ語版。英語とは守るものが違うので別に持つ。
#   ・小数点は読点（0,05）。英語の 0.05 が残ると数値の意味が変わる
#   ・引用符は „ ... “。英語の " が残ると組みが崩れる
#   ・新正書法（dass / muss）。daß は旧正書法
#   ・ドイツ式の ß を使う。gross / Strasse はスイス式
CHECKS_DE = [
    # 独語の桁区切りも点なので（114.206）、点を一律に弾くと誤検出になる。
    # 桁区切りは必ず3桁ずつ。荷重は必ず 0, で始まる。その二つで切り分ける。
    # 時刻も独語では点を使う（2.40 Uhr）ので、Uhr が続くものは除く。
    ("荷重の小数点は読点（0,05）。0.05 は不可",
     r"\b0\.\d+(?! Uhr)|\b\d+\.\d{1,2}(?!\d)(?! Uhr)"
     r"|\b\d+\.\d{4,}"),
    ("引用符は „ ... “（\" は不可）", r"\""),
    ("旧正書法 daß（dass にする）", r"\bda\u00df\b"),
    ("スイス式 ss（ß にする）",
     r"\bgross\b|\bgr\u00f6sser\b|\bStrasse\b|\bwei\u00df?ss\b|\bhei\u00dfst\b"
     r"|\bweiss\b|\bheisst\b|\bFuss\b|\bmuss?te\b(?<!musste)"),
    ("校正官は der Korrektor（Lektor / Proofreader は不可）",
     r"\bLektor\w*\b|\bProofreader\b"),
    ("半色は der Halbton（Halbfarbe / half-shade は不可）",
     r"\bHalbfarbe\w*\b|\bhalf-shade\b"),
    # 素片(技術語)は Fragment。ただし原文には普通名詞の「断片」も出るので、
    # Bruchstück を一律に禁じると誤検出になる。明らかな誤用だけを拾う。
    ("素片は das Fragment（Erinnerungsbruchst\u00fcck / Ged\u00e4chtnissplitter は不可）",
     r"\bErinnerungsbruchst\u00fcck\w*\b|\bGed\u00e4chtnissplitter\w*\b"
     r"|\bErinnerungssplitter\w*\b"),
    ("情動荷重は die affektive Last（Emotionslast は不可）",
     r"\bEmotionslast\w*\b|\bGef\u00fchlslast\w*\b"),
    ("照合機は der Komparator", r"\bVergleicher\b|\bAbgleicher\b"),
    ("残差は das Residuum（Restwert は不可）", r"\bRestwert\w*\b"),
    ("均し計画は der Angleichungsplan",
     r"\bNivellierungsplan\b|\bGl\u00e4ttungsplan\b"),
    ("英語が混じっている", r"\bthe\b|\bProofreader\b|\bper cent\b|\bfragment\b"),
    ("百分率は Prozent", r"\bpercent\b"),
    ("漢数字の残り（〇・一二三…）", r"[〇一二三四五六七八九十]"),
    ("行末の空白", r"[ \t]+$"),
]

# スペイン語版。会話はレイヤ（—）で組む。引用符で組むと英語からの翻訳書に見える。
CHECKS_ES = [
    ("荷重の小数点は読点（0,05）。0.05 は不可",
     r"\b0\.\d+|\b\d+\.\d{1,2}(?!\d)|\b\d+\.\d{4,}"),
    ("会話はレイヤ（—）。引用符 \" \u201c \u201e は不可",
     r"\"|[\u201c\u201d\u201e]"),
    ("会話のダッシュはレイヤ（—, U+2014）。ハイフンや半角ダッシュは不可",
     r"^\u3000?[-\u2013]\s*[A-ZÁÉÍÓÚÑ¿¡]"),
    ("半色は la media tinta（medio color は不可）",
     r"\bmedio color\b|\bmedia sombra\b|\bsemitono\b"),
    ("校正官は el Corrector（revisor / corrector de pruebas は不可）",
     r"\brevisor\w*\b|\bcorrector de pruebas\b"),
    ("素片は el fragmento（esquirla / astilla は不可）",
     r"\besquirla\w*\b|\bastilla\w*\b"),
    ("情動荷重は la carga afectiva（carga emocional は不可）",
     r"\bcarga emocional\b|\bpeso emocional\b"),
    ("照合機は el Comparador", r"\bcotejador\b|\bemparejador\b"),
    ("残差は el residuo（residual は不可）", r"\bresidual\w*\b"),
    ("均し計画は el Plan de Nivelación",
     r"\bPlan de Igualación\b|\bPlan de Allanamiento\b"),
    ("英独が混じっている",
     r"\bthe\b|\bProofreader\b|\bder Korrektor\b|\bdas Fragment\b"
     r"|\bHalbton\b|\bper cent\b"),
    ("漢数字の残り（〇・一二三…）", r"[〇一二三四五六七八九十]"),
    ("行末の空白", r"[ \t]+$"),
]

# フランス語版。スペイン語と似ているが、数字と句読点の規則が違う。
#   ・千の位は点ではなく不可分空白（1 027 400）。ここが西独との分かれ目で、
#     言語をまたいで作業していると最も入りやすい誤り
#   ・`:` `;` `?` `!` の前と « » の内側に不可分空白（U+00A0）が要る。
#     入れ忘れても字は読めるが、リーダーで行が変なところで切れる
#   ・フランス語の数字は点を一切使わないので、桁の間の点は一律に誤り
CHECKS_FR = [
    ("小数点は読点（0,05）。仏語は数字の間に点を使わない",
     r"\d\.\d"),
    ("千の位の区切りは不可分空白（1 027 400）。区切りがない",
     r"\d{5,}"),
    ("千の位の区切りは不可分空白 U+00A0。ふつうの空白は不可",
     r"\d\u0020\d{3}(?!\d)"),
    ("`:` `;` `?` `!` の前は不可分空白 U+00A0",
     r"[^\u00a0\n][;:?!]"),
    ("« の後ろは不可分空白 U+00A0", r"\u00ab[^\u00a0]"),
    ("» の前は不可分空白 U+00A0", r"[^\u00a0]\u00bb"),
    ("会話は長ダッシュ（—）。引用符 \" \u201c \u201e は不可",
     r"\"|[\u201c\u201d\u201e]"),
    ("会話のダッシュは長ダッシュ（—, U+2014）。ハイフンや半角ダッシュは不可",
     r"^\u3000?[-\u2013]\s*[A-ZÀÂÇÉÈÊËÎÏÔÙÛÜ]"),
    ("半色は la demi-teinte（demi-couleur / demi-ton は不可）",
     r"\bdemi-couleur\b|\bdemi-ton\b|\bsimiligravure\b"),
    ("校正官は le Correcteur（relecteur / correcteur d'épreuves は不可）",
     r"\brelecteur\w*\b|\bcorrecteur d'épreuves\b"),
    ("素片は le fragment（éclat / esquille は不可）",
     r"\béclats?\b|\besquille\w*\b"),
    ("情動荷重は la charge affective（charge émotionnelle は不可）",
     r"\bcharge émotionnelle\b|\bpoids émotionnel\b"),
    ("照合機は le Comparateur", r"\bcollationneur\b|\bapparieur\b"),
    ("残差は le résidu（résiduel は不可）", r"\brésiduel\w*\b"),
    ("均し計画は le Plan de Nivellement",
     r"\bPlan d'Égalisation\b|\bPlan d'Aplanissement\b"),
    ("技師は le technicien（ingénieur は不可）", r"\bingénieur\w*\b"),
    ("百分率は pour cent（pourcent / % は不可）", r"\bpourcent\w*\b|%"),
    ("英独西が混じっている",
     r"\bthe\b|\bProofreader\b|\bder Korrektor\b|\bdas Fragment\b"
     r"|\bHalbton\b|\bper cent\b|\bel Corrector\b|\bmedia tinta\b"),
    ("漢数字の残り（〇・一二三…）", r"[〇一二三四五六七八九十]"),
    ("行末の空白", r"[ \t]+$"),
]

# イタリア語版。会話はカポラーリ（« »）で組む。西語・仏語のダッシュではない。
#   ・約物の前に空白を入れない。仏語とは逆の規則で、両方を並行して書いていると
#     入りやすい（仏語版の直後に書いたので、特に見る）
#   ・« » の内側にも空白を入れない
#   ・千の位は点（1.027.400）。仏語の不可分空白ではなく、西語・独語と同じ
CHECKS_IT = [
    # 点は桁区切りに使うので一律に弾けない。桁区切りは必ず3桁ずつ、
    # 荷重は必ず 0, で始まる。その二つで切り分ける（西語版と同じ）。
    ("荷重の小数点は読点（0,05）。0.05 は不可",
     r"\b0\.\d+|\b\d+\.\d{1,2}(?!\d)|\b\d+\.\d{4,}"),
    ("会話はカポラーリ（« »）。引用符 \" \u201c \u201e は不可",
     r"\"|[\u201c\u201d\u201e]"),
    ("« の直後に空白を入れない", r"\u00ab[ \u00a0]"),
    ("» の直前に空白を入れない", r"[ \u00a0]\u00bb"),
    ("約物の前に空白を入れない（仏語の規則が混じっている）",
     r"[ \u00a0][;:?!]"),
    ("半色は la mezzatinta（mezzo colore / semitono は不可）",
     r"\bmezzo colore\b|\bsemitono\b|\bmezza tinta\b"),
    ("校正官は il Correttore（revisore / correttore di bozze は不可）",
     r"\brevisor\w*\b|\bcorrettore di bozze\b"),
    ("素片は il frammento（scheggia / coccio は不可）",
     r"\bscheggi\w*\b|\bcocci\w*\b"),
    ("情動荷重は il carico affettivo（carico emotivo は不可）",
     r"\bcarico emotivo\b|\bpeso emotivo\b"),
    ("照合機は il Comparatore", r"\bcollazionatore\b|\babbinatore\b"),
    ("残差は il residuo（residuale は不可）", r"\bresidual\w*\b"),
    ("均し計画は il Piano di Livellamento",
     r"\bPiano di Appianamento\b|\bPiano di Uguagliamento\b"),
    ("技師は il tecnico（ingegnere は不可）", r"\bingegner\w*\b"),
    ("百分率は per cento（percento / % は不可）", r"\bpercento\b|%"),
    ("他言語の用語が混じっている",
     r"\bthe\b|\bProofreader\b|\bder Korrektor\b|\bel Corrector\b"
     r"|\ble Correcteur\b|\bHalbton\b|\bhalf-shade\b|\bmedia tinta\b"
     r"|\bdemi-teinte\b|\bper cent\b"),
    # 仏語版の直後に書くので、機能語がそのまま残る。伊語に存在しない綴りだけを
    # 挙げる（伊 come に対する仏 comme のように、一字違いで別語になるものを狙う）。
    # 第一話で「tremò come a contrecuore」と書いていたのを手で見つけたため、
    # 同じ漏れ方を機械で落とす。西語の pero は伊語の「梨の木」と同綴りなので
    # 入れない。
    ("仏語の機能語が混じっている",
     r"\bc'est\b|\bn'est\b|\bqu'il\b|\bl'on\b|\bdans\b|\bpour\b"
     r"|\bavec\b|\bsans\b|\bmais\b|\bcomme\b|\bselon\b|\bainsi\b"
     r"|\bencore\b|\btoujours\b|\bcontrec\w+|\bgrimace\b"),
    ("西語の機能語が混じっている",
     r"\bdijo\b|\bcuando\b|\bpuede\b|\bsiempre\b|\bentonces\b"
     r"|\btambi\u00e9n\b|\bporque\b"),
    # 自分が繰り返す綴り誤り。sceso を scceso と書く癖が第二話・第十話で出た。
    # 伊語に scc という連続はない（西語・仏語にもない）ことを確かめてから入れた。
    # 「tutti tre」は辞書にはあるが、文芸の標準は e を入れる形。
    # 伊語版の初稿で15箇所出た。仏語の tous les trois、西語の los tres
    # から直訳すると e が落ちる。
    ("数詞の前に e が落ちている（tutti tre → tutti e tre）",
     r"\b[Tt]utt[ie] (?:tre|due|quattro)\b"),
    ("scc は伊語に現れない連続（sceso を scceso と書いていないか）", r"scc"),
    # rognare は伊語では「ぶつぶつ言う」。削る意味の仏語 rogner に引かれて
    # 第十話で使っていた。削るは limare / rifilare。
    # 検査の本体は re.IGNORECASE を付けないので、文頭の大文字も明示する
    ("rognare は伊語では別の意味（削るは limare）", r"\b[Rr]ognat?\w*"),
    ("漢数字の残り（〇・一二三…）", r"[〇一二三四五六七八九十]"),
    ("行末の空白", r"[ \t]+$"),
]

# オランダ語版。会話は二重引用符（“ ”）で組む。オランダの文芸は
# 一重引用符（‘ ’）も「 」も使うが、一重にするとアポストロフィ
# （'s ochtends, z'n）と同じ字になり、開きと閉じの数を機械で数えられない。
# 数えられることを優先した。
#   ・約物の前に空白を入れない。仏語とは逆の規則
#   ・千の位は点（1.027.400）、小数点は読点（0,038）。西語・伊語・独語と同じ
#   ・複合語はつなげて書く。分けて書くのはオランダ語で「英語病」と呼ばれる誤り
CHECKS_NL = [
    # 点は桁区切りに使うので一律に弾けない。切り分け方は西語・伊語と同じ。
    ("荷重の小数点は読点（0,05）。0.05 は不可",
     r"\b0\.\d+|\b\d+\.\d{1,2}(?!\d)|\b\d+\.\d{4,}"),
    ("会話は “ ”。\" „ « » は不可",
     r"\"|[„«»]"),
    ("約物の前に空白を入れない（仏語の規則が混じっている）",
     r"[  ][;:?!]"),
    ("半色は de halftint（halve tint / halftoon は不可）",
     r"\bhalve (?:tint|kleur)\b|\bhalftoon\b|\bhalf tint\b"),
    ("校正官は de Corrector（proeflezer / revisor は不可）",
     r"\bproeflezer\w*\b|\brevisor\w*\b|\bcorrector van drukproeven\b"),
    ("素片は het fragment（splinter / scherf は不可）",
     r"\bsplinter\w*\b|\bscherf\b|\bscherven\b"),
    ("情動荷重は de affectieve lading（emotionele lading は不可）",
     r"\bemotionele lading\b|\bemotioneel gewicht\b"),
    ("照合機は de Vergelijker", r"\bcollationeerder\b|\bmatcher\b"),
    ("残差は het residu（residueel は不可）", r"\bresidue\w*\b"),
    ("均し計画は het Nivelleringsplan",
     r"\bGelijkmakingsplan\b|\bEgalisatieplan\b|\bNivellatieplan\b"),
    ("技師は de technicus（ingenieur は不可）", r"\bingenieur\w*\b"),
    ("百分率は procent（percent / % は不可）", r"\bpercent\b|%"),
    # オランダ語の複合語は一語につなげる。分けて書く誤りは「英語病」
    # （Engelse ziekte）と呼ばれ、この作品の造語でいちばん起きやすい。
    ("複合語を分けて書いている（オランダ語はつなげる）",
     r"\bdroom (?:redactie|bureau|belasting|editie)\b"
     r"|\bwacht lijst\b|\bgeluks index\b|\breferentie apparaat\b"
     r"|\bwachtrij voor vergetelheid\b"),
    ("他言語の用語が混じっている",
     r"\bthe\b|\bProofreader\b|\bder Korrektor\b|\bel Corrector\b"
     r"|\ble Correcteur\b|\bil Correttore\b|\bHalbton\b"
     r"|\bhalf-shade\b|\bmedia tinta\b|\bdemi-teinte\b"
     r"|\bmezzatinta\b|\bper cent\b"),
    # 独語はオランダ語と近いので、機能語がそのまま残っても目で気づきにくい。
    # オランダ語に存在しない綴りだけを挙げる（蘭 is / en / niet / ook /
    # zich / werd / tussen に対する独 ist / und / nicht / auch / sich /
    # wurde / zwischen）。蘭語にもある den は入れない。
    ("独語の機能語が混じっている",
     r"\bist\b|\bund\b|\bnicht\b|\bauch\b|\bsich\b|\bwurde\b"
     r"|\bzwischen\b|\büber\b|\bnach\b|\bdem\b|\beine\b"
     r"|\bnur\b|\bschon\b|\bimmer\b"),
    # 比較は dan。als を使うのはオランダ語で最も有名な誤りで、話し言葉では
    # 広く使われるが文章では誤りとされる。「zonder meer als」は比較ではない
    # ので除く。
    ("比較は dan（groter als → groter dan）",
     r"(?<!zonder )\b(?:meer|groter|kleiner|hoger|lager|langer|korter"
     r"|minder|beter|slechter|anders|eerder|verder|vaker) als\b"),
    # このシリーズの造語はほとんどが het 語。de と書くと、読んでいて
    # 気づきにくいまま冠詞だけが間違っている文になる。
    ("冠詞が違う（het 語に de を付けている）",
     r"\b[Dd]e (?:fragment|geheugen|residu|register|Bureau|Archief|getal"
     r"|vak|verslag|formulier|percentage|gevoel|effect|punt|[Pp]lan|oog"
     r"|hoofd|model|apparaat|niveau|bed|water|bekertje|identificatienummer"
     r"|contaminatiepercentage|referentieapparaat|eindrapport)\b"),
    ("漢数字の残り（〇・一二三…）", r"[〇一二三四五六七八九十]"),
    ("行末の空白", r"[ \t]+$"),
]

# ブラジルポルトガル語版。会話は travessão（—、U+2014）で組む。西語・仏語と
# 同じ組み方で、ブラジル文芸の標準でもある。
#   ・正書法はブラジル。registo / facto / objecto / actual のような
#     ポルトガル本国の綴りは不可
#   ・西語が近い。読んでいて気づきにくい混入なので、別に検査を置く
#   ・千の位は点（1.027.400）、小数点は読点（0,038）
CHECKS_PT = [
    # 点は桁区切りに使うので一律に弾けない。切り分け方は西語・伊語と同じ。
    ("荷重の小数点は読点（0,05）。0.05 は不可",
     r"\b0\.\d+|\b\d+\.\d{1,2}(?!\d)|\b\d+\.\d{4,}"),
    ("会話は travessão（—）。引用符 \" \u201c \u201e \u00ab は不可",
     r"\"|[\u201c\u201d\u201e\u00ab\u00bb]"),
    ("会話のダッシュは travessão（—, U+2014）。ハイフンや半角ダッシュは不可",
     r"^\u3000?[-\u2013]\s*[A-Z\u00c1\u00c9\u00cd\u00d3\u00da\u00c3\u00d5\u00c2\u00ca\u00d4\u00c7]"),
    ("約物の前に空白を入れない（仏語の規則が混じっている）",
     r"[ \u00a0][;:?!]"),
    ("半色は a meia-tinta（meia cor / semitom は不可）",
     r"\bmeia cor\b|\bsemiton?\w*\b|\bmeio tom\b"),
    ("校正官は o Corretor（revisor は不可）", r"\brevisor\w*\b"),
    ("素片は o fragmento（estilha\u00e7o / lasca は不可）",
     r"\bestilha\u00e7\w*\b|\blasca\w*\b"),
    ("情動荷重は a carga afetiva（carga emocional は不可）",
     r"\bcarga emocional\b|\bpeso emocional\b"),
    ("照合機は o Comparador", r"\bconferidor\b|\bcombinador\b"),
    ("残差は o res\u00edduo（residual は不可）", r"\bresidual\w*\b"),
    ("均し計画は o Plano de Nivelamento",
     r"\bPlano de Igual\w+\b|\bPlano de Equaliza\w+\b"),
    ("技師は o t\u00e9cnico（engenheiro は不可）", r"\bengenheir\w*\b"),
    ("百分率は por cento（porcento / % は不可）", r"\bporcento\b|%"),
    # ポルトガル本国の綴り。ブラジル版なので混ぜない。
    ("ポルトガル本国の綴りが混じっている（ブラジル正書法で書く）",
     r"\bregisto\w*\b|\bfacto\b|\bfactos\b|\bobjec\w+|\bprojec\w+"
     r"|\bac\u00e7\u00e3o\b|\bac\u00e7\u00f5es\b|\bactu\w+|\bcontact\w+"
     r"|\bdirector\w*\b|\b\u00f3ptim\w+|\bel\u00e9ctric\w+|\bexact\w+"),
    # 西語はポルトガル語と近く、一語残っても通読では気づきにくい。
    # ポルトガル語に存在しない綴りだけを挙げる（葡 e / muito / mas /
    # ent\u00e3o / agora / quando / disse に対する西 y / muy / pero /
    # entonces / ahora / cuando / dijo）。葡語にもある nunca・antes・porque は
    # 入れない。as は葡語の冠詞なので as\u00ed だけを見る。
    ("西語の機能語が混じっている",
     r"\by\b|\bmuy\b|\bpero\b|\bentonces\b|\bahora\b|\bcuando\b"
     r"|\bdijo\b|\bhacia\b|\bestaba\b|\bhab\u00eda\b|\btambi\u00e9n\b"
     r"|\bsiempre\b|\baqu\u00ed\b|\bdespu\u00e9s\b|\bsin\b|\bcon\b"
     r"|\bdel\b|\bes\b|\bhay\b|\bas\u00ed\b|\bqu\u00e9\b"),
    ("他言語の用語が混じっている",
     r"\bthe\b|\bProofreader\b|\bder Korrektor\b|\bel Corrector\b"
     r"|\ble Correcteur\b|\bil Correttore\b|\bde Corrector\b|\bHalbton\b"
     r"|\bhalf-shade\b|\bmedia tinta\b|\bdemi-teinte\b|\bmezzatinta\b"
     r"|\bhalftint\b|\bper cent\b"),
    # 綴り字記号の落ち。シリーズの用語で起きやすいものだけを挙げる。
    ("綴り字記号が落ちている（n\u00famero / \u00edndice / t\u00e9cnico など）",
     # tecnicamente は無標（強勢が移るので記号が付かない）。tecnic\w* で
     # 括ると正しい語を誤りとして鳴らすので、名詞・形容詞の形だけを見る。
     r"\bnumero\b|\bnumeros\b|\bindice\b|\bindices\b|\btecnic[oa]s?\b"
     r"|\bcondomino\w*\b|\bgenero\b|\borgao\w*\b|\bresiduo\b"
     r"|\bperiodo\b|\bproprio\w*\b|\bultimo\w*\b"),
    ("漢数字の残り（〇・一二三…）", r"[〇一二三四五六七八九十]"),
    ("行末の空白", r"[ \t]+$"),
]

CHECKS = {"en": CHECKS_EN, "de": CHECKS_DE, "es": CHECKS_ES,
          "fr": CHECKS_FR, "it": CHECKS_IT, "nl": CHECKS_NL,
          "pt": CHECKS_PT}

# 原文の姓 -> 英語表記。第二巻は原文の読み仮名、第一巻は通用する読みによる。
# 「その話に原文の姓が出るなら、英文にもこの綴りが出る」ことだけを見る。
NAMES = {
    "vol1": {
        "01": [("梶", "Kaji"), ("杉本", "Sugimoto")],
        "02": [("戸並", "Tonami"), ("蓮見", "Hasumi")],
        "03": [("桐山", "Kiriyama"), ("宮田", "Miyata")],
        "04": [("桜井", "Sakurai"), ("志村", "Shimura")],
        "05": [("芦田", "Ashida"), ("望月", "Mochizuki")],
        "06": [("沢田", "Sawada")],
        "07": [("桑野", "Kuwano"), ("戸倉", "Tokura")],
        "08": [("宮下", "Miyashita"), ("岸", "Kishi")],
        "09": [("有村", "Arimura"), ("木内", "Kiuchi")],
        "10": [("塚原", "Tsukahara")],
        "11": [("須賀", "Suga")],
        "12": [("堀", "Hori")],
    },
    "vol2": {
        "01": [("伴", "Ban")],
        "02": [("瀬能", "Seno")],
        "03": [("早瀬", "Hayase"), ("湯浅", "Yuasa")],
        "04": [("名越", "Nagoshi")],
        "05": [("神保", "Jinbo")],
        "06": [("蓼沼", "Tadenuma"), ("桑島", "Kuwashima")],
        "07": [("岩見", "Iwami")],
        "08": [("久留須", "Kurusu")],
        "09": [("硲", "Hazama")],
        "10": [("荻堂", "Ogido")],
        "11": [("黛", "Mayuzumi")],
        "12": [("湊", "Minato")],
    },
}

# 例外: 固有名詞・意図した表記
ALLOWED = {
    r"\bmeters?\b(?! of )": ["parameters"],
    r"\b\w{4,}iz(e|es|ed|ing|ation|ations)\b": ["capsize", "capsized",
                                                 "downsize", "oversize"],
}


def check_names() -> int:
    """原文に姓があるのに、訳文に対応するローマ字名がない話を報告する。

    ローマ字形は英・独・西・仏で同じなので、四言語すべてを同じ表で見る。
    英語版だけ見ていたときは、他の三言語が素通りだった。
    """
    bad = 0
    vols = [(f"{lang}{n}", f"vol{n}")
            for lang in ("en", "de", "es", "fr", "it", "nl", "pt")
            for n in (1, 2)]
    for en_vol, ja_vol in vols:
        for num, pairs in NAMES[ja_vol].items():
            en_hits = sorted((ROOT / en_vol / "stories").glob(f"{num}_*.txt"))
            ja_hits = sorted((ROOT / ja_vol / "stories").glob(f"{num}_*.txt"))
            if not en_hits or not ja_hits:
                continue
            en_text = en_hits[0].read_text(encoding="utf-8")
            ja_text = ja_hits[0].read_text(encoding="utf-8")
            for ja_name, en_name in pairs:
                if ja_name not in ja_text:
                    print(f"{ja_vol}/{num}: 原文に『{ja_name}』がない"
                          f"（人名表のほうが古い可能性）")
                    bad += 1
                elif en_name not in en_text:
                    print(f"{en_vol}/{en_hits[0].name}: "
                          f"『{ja_name}』に対応する {en_name} が訳文にない")
                    bad += 1
    return bad


QUOTE3 = "\u3000" * 3          # 書類の引用に使う三字下げ
JA_SEC = re.compile(r"^[一二三四五六七八九十]+$")
TR_SEC = re.compile(r"^[IVXLC]+$")


def paragraphs(lines: list, sec: re.Pattern) -> list:
    """段落の一覧を返す。三字下げの連続は一塊、節番号と空行は除く。

    check_tr_structure.py と同じ数え方。行番号で突き合わせてはいけない。
    長い書類の表題は原文で一行、訳文では二行に割れるのが普通で（第十一話は
    原文203行に対し訳文205行）、行で揃えると以降が全部ずれる。
    """
    out = []
    in_quote = False
    for line in lines:
        if not line.strip() or sec.fullmatch(line.strip()):
            continue
        if line.startswith(QUOTE3):
            if not in_quote:
                out.append(line)
            in_quote = True
        else:
            in_quote = False
            out.append(line)
    return out


def check_it_quotes() -> int:
    """伊語版の会話がカポラーリで組まれているかを、原文と段落で突き合わせる。

    最初は「行頭のダッシュを禁止する」正規表現で書いたが、これは誤検出した。
    書類からの一文は四版すべてが「全角空白＋ダッシュ」で組んでいて、伊語も
    それに合わせる必要があるからである。

    次に行番号で突き合わせたが、これも誤検出した。訳文は書類の表題を二行に
    割るので、原文と行数が合わない。段落で数えるのが正しい。

    原文の段落が 　「 で始まるもの（丸ごと発話）だけを見て、対応する伊語の
    段落に « があることを確かめる。地の文に埋まった「」は引用符でも強調でも
    あり、四版の扱いが揃っていないので見ない。

    あわせて « と » の数が合うかも見る。別の文字なので片方だけ打ち間違えても
    文としては読めてしまう。
    """
    bad = 0
    for tr_vol, ja_vol in (("it1", "vol1"), ("it2", "vol2")):
        for path in sorted((ROOT / tr_vol / "stories")
                           .glob("[0-9][0-9]_*.txt")):
            ja_hits = sorted((ROOT / ja_vol / "stories")
                             .glob(f"{path.name[:2]}_*.txt"))
            if not ja_hits:
                continue
            ja = paragraphs(
                ja_hits[0].read_text(encoding="utf-8").split("\n"), JA_SEC)
            it = paragraphs(
                path.read_text(encoding="utf-8").split("\n"), TR_SEC)
            if len(ja) != len(it):
                print(f"{path.relative_to(ROOT)}: 段落数が違うため照合できない"
                      f"（原文 {len(ja)} / 訳文 {len(it)}）")
                bad += 1
                continue
            for n, (jp, ip) in enumerate(zip(ja, it), start=1):
                if jp.startswith("\u3000\u300c") and "\u00ab" not in ip:
                    print(f"{path.relative_to(ROOT)}: 第{n}段落は原文が"
                          f"発話だがカポラーリがない")
                    bad += 1
            t = path.read_text(encoding="utf-8")
            op, cl = t.count("\u00ab"), t.count("\u00bb")
            if op != cl:
                print(f"{path.relative_to(ROOT)}: カポラーリの数が合わない"
                      f"（開き \u00ab {op} / 閉じ \u00bb {cl}）")
                bad += 1
    return bad


def check_nl_quotes() -> int:
    """蘭語版の会話が二重引用符で組まれているかを、原文と段落で突き合わせる。

    数え方は check_it_quotes と同じ。行番号ではなく段落で揃える。

    “ と ” は別の字なので、片方だけ打ち間違えても文としては読める。
    一重引用符にしなかったのはこのためで、一重だとアポストロフィと同じ字に
    なって数えられない。
    """
    bad = 0
    for tr_vol, ja_vol in (("nl1", "vol1"), ("nl2", "vol2")):
        for path in sorted((ROOT / tr_vol / "stories")
                           .glob("[0-9][0-9]_*.txt")):
            ja_hits = sorted((ROOT / ja_vol / "stories")
                             .glob(f"{path.name[:2]}_*.txt"))
            if not ja_hits:
                continue
            ja = paragraphs(
                ja_hits[0].read_text(encoding="utf-8").split("\n"), JA_SEC)
            nl = paragraphs(
                path.read_text(encoding="utf-8").split("\n"), TR_SEC)
            if len(ja) != len(nl):
                print(f"{path.relative_to(ROOT)}: 段落数が違うため照合できない"
                      f"（原文 {len(ja)} / 訳文 {len(nl)}）")
                bad += 1
                continue
            for n, (jp, np_) in enumerate(zip(ja, nl), start=1):
                if jp.startswith("\u3000\u300c") and "\u201c" not in np_:
                    print(f"{path.relative_to(ROOT)}: 第{n}段落は原文が"
                          f"発話だが引用符がない")
                    bad += 1
            t = path.read_text(encoding="utf-8")
            op, cl = t.count("\u201c"), t.count("\u201d")
            if op != cl:
                print(f"{path.relative_to(ROOT)}: 引用符の数が合わない"
                      f"（開き “ {op} / 閉じ ” {cl}）")
                bad += 1
    return bad


def check_pt_dashes() -> int:
    """葡語版の発話段落が travessão で始まっているかを、原文と段落で突き合わせる。

    西語版・仏語版にはこの検査がない。会話も書類からの引用も行頭のダッシュで
    組むので、ダッシュの有無だけでは区別できないからである。

    段落で突き合わせれば区別できる。原文の段落が 　「 で始まるもの（丸ごと
    発話）だけを見て、対応する葡語の段落が 　— で始まることを確かめる。
    書類からの一文は原文で 　―― で始まるので、この検査の対象に入らない。
    """
    bad = 0
    DASH = "\u3000\u2014"
    for tr_vol, ja_vol in (("pt1", "vol1"), ("pt2", "vol2")):
        for path in sorted((ROOT / tr_vol / "stories")
                           .glob("[0-9][0-9]_*.txt")):
            ja_hits = sorted((ROOT / ja_vol / "stories")
                             .glob(f"{path.name[:2]}_*.txt"))
            if not ja_hits:
                continue
            ja = paragraphs(
                ja_hits[0].read_text(encoding="utf-8").split("\n"), JA_SEC)
            pt = paragraphs(
                path.read_text(encoding="utf-8").split("\n"), TR_SEC)
            if len(ja) != len(pt):
                print(f"{path.relative_to(ROOT)}: 段落数が違うため照合できない"
                      f"（原文 {len(ja)} / 訳文 {len(pt)}）")
                bad += 1
                continue
            for n, (jp, pp) in enumerate(zip(ja, pt), start=1):
                if jp.startswith("\u3000\u300c") and not pp.startswith(DASH):
                    print(f"{path.relative_to(ROOT)}: 第{n}段落は原文が"
                          f"発話だが travess\u00e3o で始まっていない")
                    bad += 1
    return bad


def check_de_quotes() -> int:
    """ドイツ語版の引用符が開きと閉じで同数かを見る。

    „ と “ は別の文字なので、片方だけ打ち間違えても文としては読める。
    行ごとの正規表現では数えられないので、ファイル単位で突き合わせる。
    """
    bad = 0
    for path in STORIES:
        if path.parts[-3][:2] != "de":
            continue
        t = path.read_text(encoding="utf-8")
        op, cl = t.count("\u201e"), t.count("\u201c")
        if op != cl:
            print(f"{path.relative_to(ROOT)}: 引用符の数が合わない"
                  f"（開き „ {op} / 閉じ \u201c {cl}）")
            bad += 1
    return bad


def main() -> int:
    hits = (check_names() + check_de_quotes() + check_it_quotes()
            + check_nl_quotes() + check_pt_dashes())
    for path in STORIES:
        lang = path.parts[-3][:2]          # en1/de2 などの先頭2字
        checks = CHECKS.get(lang)
        if checks is None:
            print(f"{path}: 検査の定義がない言語 {lang!r}")
            hits += 1
            continue
        text = path.read_text(encoding="utf-8")
        lines = text.split("\n")
        for label, pattern in checks:
            rx = re.compile(pattern, re.MULTILINE)
            for i, line in enumerate(lines, start=1):
                for m in rx.finditer(line):
                    word = m.group(0)
                    if any(word.lower() in a for a in ALLOWED.get(pattern, [])):
                        continue
                    rel = path.relative_to(ROOT)
                    print(f"{rel}:{i}  {label}  → {word!r}")
                    hits += 1

    print()
    print(f"対象 {len(STORIES)}ファイル")
    print(f"要対応 {hits} 件" if hits else "用語ゆれなし")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
