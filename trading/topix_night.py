#!/usr/bin/env python3
"""TOPIX先物「日中安 → 夜間買い」のシグナル判定とバックテスト。

ルール:
    日中終値が日中始値より THRESHOLD pt以上安い日だけ、
    夜間寄付で買い、夜間引けで手仕舞う(持ち越さない)。
    保険の損切り逆指値は 夜間寄付 − STOP pt。

データは trading/topix.tsv(タブ区切り、証券会社の表をそのまま貼れる形式):
    日付  日中始値 高値 安値 終値  夜間始値 高値 安値 終値
当日の判定は日中4列だけの行でよい(夜間は後から埋める)。行の順序は問わない。

    python trading/topix_night.py                 # 最新日の判定(今夜買うか)
    python trading/topix_night.py add "2026/9/25	4080	4100	4050	4060"
    python trading/topix_night.py add < rows.txt   # 複数行をまとめて追加・上書き
    python trading/topix_night.py backtest         # 成績と直近の劣化チェック
"""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

DATA = Path(__file__).with_name("topix.tsv")
THRESHOLD = 10.0  # 日中の下落幅(pt)
STOP = 60.0       # 保険の損切り幅(pt)
COST = 1.0        # 1往復の手数料+スリッページ(pt)
RECENT = 20       # 劣化チェックに使う直近トレード数

Row = tuple[date, list[float]]


def parse_line(line: str) -> Row | None:
    parts = line.replace(",", "\t").split()
    if len(parts) not in (5, 9):
        return None
    try:
        y, m, d = map(int, parts[0].replace("-", "/").split("/"))
        return date(y, m, d), [float(p) for p in parts[1:]]
    except ValueError:
        return None


def load() -> dict[date, list[float]]:
    rows: dict[date, list[float]] = {}
    if DATA.exists():
        for line in DATA.read_text(encoding="utf-8").splitlines():
            r = parse_line(line)
            if r:
                rows[r[0]] = r[1]
    return rows


def save(rows: dict[date, list[float]]) -> None:
    def fmt(v: float) -> str:
        return f"{v:g}"
    lines = [
        "\t".join([f"{d.year}/{d.month}/{d.day}", *map(fmt, v)])
        for d, v in sorted(rows.items(), reverse=True)
    ]
    DATA.write_text("\n".join(lines) + "\n", encoding="utf-8")


def is_signal(v: list[float]) -> bool:
    return v[0] - v[3] >= THRESHOLD


def trades(rows: dict[date, list[float]]) -> list[tuple[date, float]]:
    out = []
    for d, v in sorted(rows.items()):
        if len(v) != 8 or not is_signal(v):
            continue
        entry, low, close = v[4], v[6], v[7]
        exit_ = entry - STOP if low <= entry - STOP else close
        out.append((d, exit_ - entry - COST))
    return out


def summary(pnl: list[float]) -> str:
    if not pnl:
        return "取引なし"
    eq = peak = dd = 0.0
    for p in pnl:
        eq += p
        peak = max(peak, eq)
        dd = max(dd, peak - eq)
    wins = sum(1 for p in pnl if p > 0)
    return (f"損益 {sum(pnl):+.1f}pt / {len(pnl)}回 / 勝率 {wins / len(pnl):.0%}"
            f" / 平均 {sum(pnl) / len(pnl):+.1f}pt / 最大DD {dd:.1f}pt")


def health(ts: list[tuple[date, float]]) -> str:
    recent = [p for _, p in ts[-RECENT:]]
    if len(recent) < RECENT:
        return f"劣化チェック: トレード{len(recent)}回(判定には{RECENT}回必要)"
    avg = sum(recent) / len(recent)
    state = "継続OK" if avg > 0 else "停止推奨(直近の平均がマイナス)"
    return f"劣化チェック: 直近{RECENT}回の平均 {avg:+.1f}pt → {state}"


def cmd_signal(rows: dict[date, list[float]]) -> None:
    if not rows:
        sys.exit(f"データがありません: {DATA}")
    d = max(rows)
    v = rows[d]
    o, c = v[0], v[3]
    print(f"{d:%Y/%m/%d} 日中 始値 {o:g} → 終値 {c:g}({c - o:+g}pt、条件は −{THRESHOLD:g}pt以下)")
    if is_signal(v):
        print("▶ 今夜は【買い】")
        print("   夜間寄付で成行買い → 夜間引けで成行決済(持ち越さない)")
        print(f"   損切り逆指値: 夜間寄付 − {STOP:g}pt(目安 {c - STOP:g})")
    else:
        print("▶ 今夜は【見送り】")
    if len(v) == 8:
        print(f"   ※この日の夜間は記録済み(夜間 {v[4]:g} → {v[7]:g})。最新の日中データを add してください。")
    print(health(trades(rows)))


def cmd_add(rows: dict[date, list[float]], text: str) -> None:
    added = bad = 0
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith(("日付", "始値")):
            continue
        r = parse_line(line)
        if r is None:
            bad += 1
            print(f"読めない行: {line!r}", file=sys.stderr)
            continue
        rows[r[0]] = r[1]
        added += 1
    save(rows)
    print(f"{added}行を追加・上書きしました({bad}行スキップ)")
    cmd_signal(rows)


def cmd_backtest(rows: dict[date, list[float]]) -> None:
    ts = trades(rows)
    print(f"ルール: 日中 −{THRESHOLD:g}pt以下 → 夜間買い / 損切り {STOP:g}pt / コスト {COST:g}pt")
    print("全期間  ", summary([p for _, p in ts]))
    half = len(ts) // 2
    if half:
        print("前半    ", summary([p for _, p in ts[:half]]))
        print("後半    ", summary([p for _, p in ts[half:]]))
    print(health(ts))
    print("\n直近のトレード:")
    for d, p in ts[-10:]:
        print(f"  {d:%Y/%m/%d}  {p:+.1f}pt")


def main() -> None:
    args = sys.argv[1:]
    rows = load()
    cmd = args[0] if args else "signal"
    if cmd == "signal":
        cmd_signal(rows)
    elif cmd == "add":
        cmd_add(rows, "\n".join(args[1:]) if len(args) > 1 else sys.stdin.read())
    elif cmd == "backtest":
        cmd_backtest(rows)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
