#!/usr/bin/env python3
"""縦書き版のために、算用数字を漢数字へ戻す。

manuscript/ は算用数字を正とし、ここでは build/vertical/ に変換結果を書き出す。
帳簿の最新の一行（宗一郎が青いボールペンで書いた行）だけは算用数字のまま残す。
"""
import pathlib, re, sys, collections

ROOT = pathlib.Path(__file__).parent
SRC  = ROOT / "manuscript"
DST  = ROOT / "build" / "vertical"

D = "〇一二三四五六七八九"

# 帳簿の一行と、そこだけ算用数字のままにする語
PROTECT = [
    "2026年2月10日　三つに分けた　もう一つ　分けられなかったものがある",
    "この帳面で唯一、算用数字だった",
    "A4", "B5", "LED", "T-4", "2026.1.20", "PDF", "NISA", "ATM", "Arclight Capital",
]


def digits(n: str) -> str:
    """位取りなしで一桁ずつ（年号用）。"""
    return "".join(D[int(c)] for c in n)


def under_man(n: int, lead_one_sen: bool = False) -> str:
    """1〜9999 を漢数字に。lead_one_sen=True なら千の位が1でも「一千」と書く。"""
    if n == 0:
        return ""
    out = ""
    for v, u in ((1000, "千"), (100, "百"), (10, "十")):
        q, n = divmod(n, v)
        if q:
            keep = (q != 1) or (v == 1000 and lead_one_sen)
            out += (D[q] if keep else "") + u
    if n:
        out += D[n]
    return out


def kansuji(n: int) -> str:
    """整数を漢数字に（万・億つき）。"""
    if n == 0:
        return "〇"
    out = ""
    for v, u in ((10 ** 8, "億"), (10 ** 4, "万")):
        q, n = divmod(n, v)
        if q:
            # 「千万」「億千万」は避け、「一千万」「一億一千万」と書く
            out += under_man(q, lead_one_sen=(q == 1000 or bool(out))) + u
    out += under_man(n)
    return out


DOCUMENT_FORMS = [
    ("2025-08-06　　　外国送金　　　　　　　28,000,000",
     "二〇二五年八月六日　　外国送金　　　　二八、〇〇〇、〇〇〇"),
    ("72,043,518", "七二、〇四三、五一八"),
    ("9,800平方メートル", "九、八〇〇平方メートル"),
    # 帳票の行だけ帳票の書き方にする。地の文の金額は「八万円」のままでよい
    ("　　　振込　　　　　　　　　　　　　　　　80,000", "　　　振込　　　　　　　　　　　　　　　　八〇、〇〇〇"),
    ("1,180,000円", "一、一八〇、〇〇〇円"),
]


def convert(text: str) -> tuple[str, list]:
    log = []
    for a, b in sorted(DOCUMENT_FORMS, key=lambda x: -len(x[0])):  # 長い順。短い方が部分一致するのを防ぐ
        if a in text:
            text = text.replace(a, b)
            log.append((a, b))
    ph = {}
    for i, p in enumerate(PROTECT):
        k = "%d" % i
        if p in text:
            text = text.replace(p, k)
            ph[k] = p

    def rec(m, new):
        log.append((m.group(0), new))
        return new

    # 年（西暦は一桁ずつ）
    text = re.sub(r'(\d{4})年', lambda m: rec(m, digits(m.group(1)) + "年"), text)
    # 月・日・時・分・秒・歳・段目・番目・代目・回・本・枚・台・人・軒・通・社・箱・冊・行・部・脚・基・羽・件・か月・週間・年間・年
    def unit(u):
        return lambda m: rec(m, kansuji(int(m.group(1))) + u)
    for pat, u in [
        (r'(\d+)月',   "月"), (r'(\d+)日',  "日"), (r'(\d+)時', "時"), (r'(\d+)分', "分"),
        (r'(\d+)歳',   "歳"), (r'(\d+)段目',"段目"),(r'(\d+)番目',"番目"),(r'(\d+)代目',"代目"),
        (r'(\d+)回',   "回"), (r'(\d+)本',  "本"), (r'(\d+)枚', "枚"), (r'(\d+)台', "台"),
        (r'(\d+)人',   "人"), (r'(\d+)軒',  "軒"), (r'(\d+)通', "通"), (r'(\d+)社', "社"),
        (r'(\d+)箱',   "箱"), (r'(\d+)冊',  "冊"), (r'(\d+)行', "行"), (r'(\d+)部', "部"),
        (r'(\d+)脚',   "脚"), (r'(\d+)基',  "基"), (r'(\d+)羽', "羽"), (r'(\d+)件', "件"),
        (r'(\d+)名',   "名"), (r'(\d+)階',  "階"), (r'(\d+)畳', "畳"), (r'(\d+)坪', "坪"),
        (r'(\d+)割',   "割"), (r'(\d+)か所',"か所"),(r'(\d+)種類',"種類"),(r'(\d+)か月',"か月"),
        (r'(\d+)週間', "週間"),(r'(\d+)年間',"年間"),(r'(\d+)日間',"日間"),(r'(\d+)行目',"行目"),
        (r'(\d+)通目', "通目"),(r'(\d+)枚目',"枚目"),(r'(\d+)回目',"回目"),(r'(\d+)人目',"人目"),
        (r'(\d+)センチ',"センチ"),(r'(\d+)メートル',"メートル"),(r'(\d+)キロ',"キロ"),
        (r'(\d+)ワット',"ワット"),(r'(\d+)平方メートル',"平方メートル"),
    ]:
        text = re.sub(pat, unit(u), text)
    # 金額・数量（億・万つき、カンマあり）
    text = re.sub(r'(\d+)億(\d[\d,]*)万',
                  lambda m: rec(m, kansuji(int(m.group(1)) * 10 ** 8
                                           + int(m.group(2).replace(",", "")) * 10 ** 4)), text)
    text = re.sub(r'(\d+)億', lambda m: rec(m, kansuji(int(m.group(1))) + "億"), text)
    text = re.sub(r'(\d[\d,]*)万', lambda m: rec(m, kansuji(int(m.group(1).replace(",", ""))) + "万"), text)
    text = re.sub(r'(\d[\d,]*)円', lambda m: rec(m, kansuji(int(m.group(1).replace(",", ""))) + "円"), text)
    # 小数（4.5% など）
    text = re.sub(r'(\d+)\.(\d+)%',
                  lambda m: rec(m, kansuji(int(m.group(1))) + "・" + digits(m.group(2)) + "パーセント"), text)
    text = re.sub(r'(\d+)%', lambda m: rec(m, kansuji(int(m.group(1))) + "パーセント"), text)
    # 残った裸の数字
    text = re.sub(r'(?<![-\d])(\d[\d,]*)(?![-\d])',
                  lambda m: rec(m, kansuji(int(m.group(1).replace(",", "")))), text)

    for k, p in ph.items():
        text = text.replace(k, p)
    return text, log


def main():
    DST.mkdir(parents=True, exist_ok=True)
    allog = collections.Counter()
    for f in sorted(SRC.glob("*.md")):
        out, log = convert(f.read_text(encoding="utf-8"))
        (DST / f.name).write_text(out, encoding="utf-8")
        for a, b in log:
            allog[(a, b)] += 1
    rest = []
    for f in sorted(DST.glob("*.md")):
        for i, line in enumerate(f.read_text(encoding="utf-8").split("\n"), 1):
            for m in re.finditer(r'\d', line):
                rest.append((f.name, i, line[max(0, m.start()-18):m.start()+18]))
    if "--log" in sys.argv:
        for (a, b), c in sorted(allog.items(), key=lambda x: -x[1]):
            print("  %-18s → %-22s ×%d" % (a, b, c))
    print("変換パターン:", len(allog), "種")
    print("変換後に残った算用数字:", len(rest), "件")
    for r in rest:
        print("   ", r[0], r[1], r[2])


if __name__ == "__main__":
    main()
