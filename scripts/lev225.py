#!/usr/bin/env python3
"""日経平均レバレッジ(2倍)を対象にした、シグナル生成とバックテストのCLI。

個別株の流動性を避けて日経225のレバレッジ商品(1570 など)だけを売買する、
という前提で作ってある。中心にあるのは「2倍の日次リバランスは横ばい相場で減価する」
という一点で、このスクリプトはその減価を隠さずに明示的に計算する。

    python scripts/lev225.py selftest                      # 計算式の自己検証(ネット不要)
    python scripts/lev225.py backtest --csv n225.csv       # 全戦略を比較
    python scripts/lev225.py signal   --csv n225.csv       # 今日の目標ポジション
    python scripts/lev225.py fetch    --out n225.csv       # 日経平均の日足を取得

入力は「日経平均株価そのもの」の日足CSV。レバレッジETFの値動きは、その指数から
日次リバランスを再現して合成する(`synth_leveraged`)。ETFの実際の価格ではなく
指数から合成するのは、減価と信託報酬がどこから来ているかを分離して見るため。

重要な前提と限界は README の「日経225レバレッジ」節に書いてある。
このスクリプトは発注しない。`signal` が出す目標ポジションが、発注系との境界。
"""

import argparse
import csv
import io
import json
import math
import statistics
import sys
import urllib.request
from datetime import date, datetime
from pathlib import Path

# 日本株の年間営業日数。年率換算はすべてこれを使う。
TRADING_DAYS = 245

# 1570(NEXT FUNDS 日経平均レバレッジ)の信託報酬は年0.80%程度。
# 日次に均して、合成ETFの毎日のリターンから引く。
DEFAULT_EXPENSE_RATIO = 0.0080

DEFAULT_LEVERAGE = 2.0

# 往復の売買コスト(bps)。手数料とスプレッドと滑りをまとめた概算。
DEFAULT_COST_BPS = 10.0

# リバランス幅。目標ポジションとの差がこれ未満なら建て替えない。
DEFAULT_REBALANCE_BAND = 0.10

# 日経平均の日足。stooq は認証なしでCSVを返す。
N225_CSV_URL = "https://stooq.com/q/d/l/?s=^nkx&i=d"

# CSVの列名のゆれを吸収する。
COLUMN_ALIASES = {
    "date": ("date", "日付", "年月日", "datetime"),
    "open": ("open", "始値", "寄値"),
    "high": ("high", "高値"),
    "low": ("low", "安値"),
    "close": ("close", "adj close", "adjclose", "終値", "調整後終値"),
}

DATE_FORMATS = ("%Y-%m-%d", "%Y/%m/%d", "%Y%m%d", "%Y-%m-%d %H:%M:%S")


# --------------------------------------------------------------------------- 入力


class DataError(Exception):
    """入力データが戦略を回すのに足りていない。"""


def _normalize_header(name):
    return name.strip().lstrip("﻿").lower()


def _resolve_columns(header):
    """ヘッダ行から、必要な列がCSVの何番目にあるかを引く。"""
    normalized = [_normalize_header(h) for h in header]
    index = {}
    for key, aliases in COLUMN_ALIASES.items():
        for alias in aliases:
            if alias in normalized:
                index[key] = normalized.index(alias)
                break
    for required in ("date", "close"):
        if required not in index:
            raise DataError(
                f"CSVに '{required}' に相当する列が無い(ヘッダ: {', '.join(header)})。"
                f" 使える列名: {', '.join(COLUMN_ALIASES[required])}"
            )
    return index


def _parse_date(text):
    text = text.strip()
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue
    raise DataError(f"日付として読めない: {text!r}")


def _parse_number(text):
    """'38,123.45' のような桁区切りつきの数値を読む。空欄は None。"""
    cleaned = text.strip().replace(",", "").replace("　", "")
    if cleaned in ("", "-", "null", "N/A"):
        return None
    try:
        return float(cleaned)
    except ValueError:
        raise DataError(f"数値として読めない: {text!r}")


def parse_ohlc_csv(text):
    """日足CSVを [{date, open, high, low, close}, ...] に読む(日付の昇順)。

    列名・日付書式・桁区切り・並び順のゆれは吸収する。終値が欠けている行は捨てる。
    """
    reader = csv.reader(io.StringIO(text))
    try:
        header = next(reader)
    except StopIteration:
        raise DataError("CSVが空。")
    index = _resolve_columns(header)

    rows = []
    for lineno, raw in enumerate(reader, start=2):
        if not raw or all(not cell.strip() for cell in raw):
            continue
        if len(raw) <= index["close"]:
            raise DataError(f"{lineno}行目: 列が足りない: {raw!r}")
        try:
            close = _parse_number(raw[index["close"]])
            if close is None or close <= 0:
                continue
            row = {"date": _parse_date(raw[index["date"]]), "close": close}
            for key in ("open", "high", "low"):
                pos = index.get(key)
                row[key] = _parse_number(raw[pos]) if pos is not None and pos < len(raw) else None
        except DataError as exc:
            raise DataError(f"{lineno}行目: {exc}")
        rows.append(row)

    if len(rows) < 2:
        raise DataError("日足が2行未満。バックテストできない。")

    rows.sort(key=lambda r: r["date"])
    seen = set()
    deduped = []
    for row in rows:  # 同じ日が二重に入っているCSVがあるので、後勝ちで潰す
        if row["date"] in seen:
            deduped[-1] = row
            continue
        seen.add(row["date"])
        deduped.append(row)
    return deduped


def load_csv(path):
    return parse_ohlc_csv(Path(path).read_text(encoding="utf-8-sig"))


def fetch_n225(url=N225_CSV_URL, timeout=30):
    """日経平均の日足CSVを取得して文字列で返す。

    注意: この関数は開発セッションからは検証できていない(外部への接続が塞がれていた)。
    落ちたときは URL を直接ブラウザで開いて、CSVが返るかを先に確かめること。
    """
    request = urllib.request.Request(url, headers={"User-Agent": "x-auto-poster/lev225"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        body = response.read().decode("utf-8", errors="replace")
    lines = body.splitlines()
    if not lines or "," not in lines[0]:
        raise DataError(f"CSVらしくない応答が返った(先頭200字): {body[:200]!r}")
    return body


# --------------------------------------------------------------------------- 合成


def pct_returns(values):
    """[v0, v1, ...] から日次リターンを返す。先頭は 0.0 で長さを揃える。"""
    out = [0.0]
    for prev, cur in zip(values, values[1:]):
        out.append(cur / prev - 1.0)
    return out


def synth_leveraged(index_returns, leverage=DEFAULT_LEVERAGE,
                    expense_ratio=DEFAULT_EXPENSE_RATIO):
    """指数の日次リターンから、日次リバランス型レバレッジETFのリターンを合成する。

    毎日 `leverage` 倍の指数リターンを取りに行き、信託報酬を日割りで引く。
    これがレバレッジETFの定義そのもので、横ばい相場での減価はここから自動的に出る
    (指数が +10% → -9.09% で元値に戻っても、2倍側は戻らない)。

    再現しないもの: 信託財産留保額、先物の限月ロールコスト、金利、
    ETFの市場価格と基準価額の乖離(プレミアム/ディスカウント)。
    """
    daily_cost = expense_ratio / TRADING_DAYS
    out = [0.0]
    for r in index_returns[1:]:
        out.append(leverage * r - daily_cost)
    return out


def compound(returns, initial=1.0):
    """リターン列を複利で積む。長さは returns と同じ(先頭が initial)。"""
    equity = [initial]
    for r in returns[1:]:
        equity.append(equity[-1] * (1.0 + r))
    return equity


# --------------------------------------------------------------------------- 戦略

# 戦略は「i日目の終値までの情報だけを見て、i日目に決めた目標ポジション」を返す。
# そのポジションが実際に効くのは i+1 日目以降(run_backtest がずらす)。
# ここで未来を見ないことが、バックテストが嘘をつかないための唯一の条件。


def _sma(values, end, window):
    """values[end-window+1 .. end] の単純移動平均。足りなければ None。"""
    if end + 1 < window:
        return None
    return sum(values[end - window + 1 : end + 1]) / window


def _realized_vol(returns, end, window):
    """returns[end-window+1 .. end] の年率換算ボラティリティ。足りなければ None。"""
    if end + 1 < window or window < 2:
        return None
    sample = returns[end - window + 1 : end + 1]
    return statistics.pstdev(sample) * math.sqrt(TRADING_DAYS)


def strategy_buyhold(closes, lev_returns, **_):
    """常にフルポジション。レバレッジETFを買って持ち続けた場合の基準線。"""
    return [1.0] * len(closes)


def strategy_flat(closes, lev_returns, **_):
    """常にノーポジション。コスト計算が壊れていないかを見るための対照。"""
    return [0.0] * len(closes)


def strategy_sma(closes, lev_returns, sma_window=200, **_):
    """指数が移動平均より上のときだけ持つ、素朴なトレンドフィルタ。

    レバレッジ商品で下落局面を避けることの効果は、リターンよりドローダウンに出る。
    """
    positions = []
    for i in range(len(closes)):
        average = _sma(closes, i, sma_window)
        positions.append(0.0 if average is None else (1.0 if closes[i] >= average else 0.0))
    return positions


def strategy_voltarget(closes, lev_returns, target_vol=0.25, vol_window=20, **_):
    """実現ボラが目標を超えたらポジションを落とす(上限はフルポジション)。

    レバレッジETFの減価はボラの2乗で効くので、ボラが高い時期を避けること自体が
    減価対策になる、という考え方。
    """
    positions = []
    for i in range(len(closes)):
        vol = _realized_vol(lev_returns, i, vol_window)
        if vol is None or vol <= 0:
            positions.append(0.0)
        else:
            positions.append(min(1.0, target_vol / vol))
    return positions


def strategy_sma_vol(closes, lev_returns, sma_window=200, target_vol=0.25,
                     vol_window=20, **_):
    """トレンドフィルタで方向を決め、ボラターゲットで大きさを決める。"""
    gate = strategy_sma(closes, lev_returns, sma_window=sma_window)
    size = strategy_voltarget(closes, lev_returns, target_vol=target_vol, vol_window=vol_window)
    return [g * s for g, s in zip(gate, size)]


STRATEGIES = {
    "buyhold": strategy_buyhold,
    "flat": strategy_flat,
    "sma": strategy_sma,
    "voltarget": strategy_voltarget,
    "sma_vol": strategy_sma_vol,
}


# --------------------------------------------------------------------------- 評価


def apply_band(target, held, band):
    """目標との差が `band` 未満なら動かさない(リバランス幅)。

    ボラターゲットのような連続値の戦略は、幅を入れないと毎日わずかに建て替えて
    しまい、実際には執行できない売買回数になる。幅は現実の制約であって、
    成績を良く見せるための調整ではない。
    """
    return held if abs(target - held) < band else target


def run_backtest(returns, positions, cost_bps=DEFAULT_COST_BPS, exec_lag=0,
                 rebalance_band=DEFAULT_REBALANCE_BAND):
    """ポジション列をリターン列に当てて、資産曲線を作る。

    `positions[i]` は i日目の終値時点で決めたもの。これが効くのは i+1 日目の
    リターンからで、`exec_lag` を足すとさらに約定を遅らせられる(終値で建てられず
    翌日の寄りになる、という現実に対する感度を見るため)。

    売買コストはポジションの変化量に比例してかかる。
    """
    if len(returns) != len(positions):
        raise ValueError("returns と positions の長さが違う")
    cost_rate = cost_bps / 10000.0

    equity = [1.0]
    applied = [0.0]  # その日に実際に効いていたポジション
    held = 0.0
    trades = 0
    turnover = 0.0

    for t in range(1, len(returns)):
        source = t - 1 - exec_lag
        desired = positions[source] if source >= 0 else 0.0
        target = apply_band(desired, held, rebalance_band)
        change = abs(target - held)
        if change > 1e-12:
            trades += 1
            turnover += change
        equity.append(equity[-1] * (1.0 + target * returns[t] - change * cost_rate))
        applied.append(target)
        held = target

    return {"equity": equity, "positions": applied, "trades": trades, "turnover": turnover}


def max_drawdown(equity):
    """最大ドローダウン(負の値)を返す。"""
    peak = equity[0]
    worst = 0.0
    for value in equity:
        peak = max(peak, value)
        worst = min(worst, value / peak - 1.0)
    return worst


def metrics(equity, positions=None, trades=0, dates=None):
    """資産曲線から成績を出す。"""
    days = len(equity) - 1
    if days <= 0:
        raise DataError("評価できる日数が無い。")
    total = equity[-1] / equity[0]
    daily = [b / a - 1.0 for a, b in zip(equity, equity[1:])]

    years = days / TRADING_DAYS
    cagr = total ** (1.0 / years) - 1.0 if years > 0 and total > 0 else float("nan")
    vol = statistics.pstdev(daily) * math.sqrt(TRADING_DAYS) if len(daily) > 1 else 0.0
    mean = statistics.fmean(daily) if daily else 0.0
    sharpe = (mean / statistics.pstdev(daily) * math.sqrt(TRADING_DAYS)) if len(daily) > 1 and statistics.pstdev(daily) > 0 else float("nan")
    mdd = max_drawdown(equity)

    out = {
        "days": days,
        "years": years,
        "total_return": total - 1.0,
        "cagr": cagr,
        "vol": vol,
        "sharpe": sharpe,
        "max_drawdown": mdd,
        "calmar": (cagr / abs(mdd)) if mdd < 0 and not math.isnan(cagr) else float("nan"),
        "trades": trades,
    }
    if positions is not None and positions:
        out["exposure"] = statistics.fmean(positions)
    if dates:
        out["start"] = dates[0].isoformat()
        out["end"] = dates[-1].isoformat()
    return out


def evaluate(rows, strategy_name, leverage=DEFAULT_LEVERAGE,
             expense_ratio=DEFAULT_EXPENSE_RATIO, cost_bps=DEFAULT_COST_BPS,
             exec_lag=0, params=None, rebalance_band=DEFAULT_REBALANCE_BAND):
    """1つの戦略を通しで評価する。"""
    if strategy_name not in STRATEGIES:
        raise DataError(f"知らない戦略: {strategy_name}(使えるのは {', '.join(STRATEGIES)})")
    closes = [r["close"] for r in rows]
    index_returns = pct_returns(closes)
    lev_returns = synth_leveraged(index_returns, leverage, expense_ratio)
    positions = STRATEGIES[strategy_name](closes, lev_returns, **(params or {}))
    result = run_backtest(lev_returns, positions, cost_bps=cost_bps, exec_lag=exec_lag,
                          rebalance_band=rebalance_band)
    stats = metrics(result["equity"], result["positions"], result["trades"],
                    [r["date"] for r in rows])
    stats["strategy"] = strategy_name
    return stats, result, lev_returns, index_returns


# --------------------------------------------------------------------------- 表示


def _pct(value):
    return "n/a" if value is None or math.isnan(value) else f"{value * 100:>7.2f}%"


def _num(value):
    return "n/a" if value is None or math.isnan(value) else f"{value:>7.2f}"


def print_table(rows_of_stats, title):
    print(f"\n{title}")
    print("-" * 104)
    print(f"{'戦略':<12}{'年率':>9}{'累積':>11}{'ボラ':>9}{'Sharpe':>9}"
          f"{'最大DD':>10}{'Calmar':>9}{'建玉率':>9}{'売買回数':>10}")
    print("-" * 104)
    for s in rows_of_stats:
        print(f"{s['strategy']:<12}{_pct(s['cagr']):>9}{_pct(s['total_return']):>11}"
              f"{_pct(s['vol']):>9}{_num(s['sharpe']):>9}{_pct(s['max_drawdown']):>10}"
              f"{_num(s['calmar']):>9}{_pct(s.get('exposure', float('nan'))):>9}"
              f"{s['trades']:>10}")
    print("-" * 104)


# --------------------------------------------------------------------------- 自己検証


def _close(a, b, tol=1e-9):
    return abs(a - b) < tol


def selftest():
    """外部データなしで、計算式が意図どおりかを確かめる。

    バックテストのコードで怖いのは「動くが間違っている」こと。ここで検証するのは
    (1)レバレッジの減価、(2)ポジションを未来に漏らしていないか、(3)ドローダウン。
    """
    failures = []

    def check(name, condition, detail=""):
        print(f"  {'ok  ' if condition else 'FAIL'}  {name}{('  — ' + detail) if detail else ''}")
        if not condition:
            failures.append(name)

    print("1. レバレッジの減価")
    # 指数が +10% → -9.0909% で元の水準にちょうど戻る往復。
    prices = [100.0, 110.0, 100.0]
    idx = pct_returns(prices)
    lev = synth_leveraged(idx, leverage=2.0, expense_ratio=0.0)
    eq = compound(lev)
    check("指数は元の水準に戻る", _close(prices[-1], prices[0]))
    check("2倍側は戻らない(減価する)", eq[-1] < 1.0, f"最終 {eq[-1]:.6f}")
    # 手計算: 1 * 1.20 * (1 - 2*0.0909090909...) = 1.2 * 0.8181818... = 0.98181818...
    check("減価量が手計算と一致", _close(eq[-1], 0.9818181818181818, 1e-12), f"{eq[-1]:.12f}")

    # 同じ往復を100回。指数は横ばいのまま、2倍側だけが削れていく。
    long_prices = [100.0]
    for _ in range(100):
        long_prices.extend([long_prices[-1] * 1.10, long_prices[-1]])
    long_eq = compound(synth_leveraged(pct_returns(long_prices), 2.0, 0.0))
    check("往復100回で指数は横ばい", _close(long_prices[-1], 100.0, 1e-6))
    check("往復100回で2倍側は大きく減価", long_eq[-1] < 0.2, f"最終 {long_eq[-1]:.4f}")

    print("2. ポジションを未来に漏らしていないか")
    # リターンは [_, +10%, +10%, +10%]。ポジションは初日だけ0。
    rets = [0.0, 0.10, 0.10, 0.10]
    pos = [0.0, 1.0, 1.0, 1.0]
    res = run_backtest(rets, pos, cost_bps=0.0, exec_lag=0)
    # 1日目は positions[0]=0 なので取れない。2日目と3日目だけ +10%。
    check("i日目のシグナルが効くのは i+1 日目から",
          _close(res["equity"][-1], 1.21, 1e-12), f"最終 {res['equity'][-1]:.12f}")
    res_lag = run_backtest(rets, pos, cost_bps=0.0, exec_lag=1)
    check("exec_lag=1 でさらに1日遅れる",
          _close(res_lag["equity"][-1], 1.10, 1e-12), f"最終 {res_lag['equity'][-1]:.12f}")
    # 未来を見る戦略は、未来を見ない戦略より必ず良くなる(検出力の確認)。
    cheat = run_backtest(rets, [1.0, 1.0, 1.0, 1.0], cost_bps=0.0)
    check("フルポジションのほうが成績が良い", cheat["equity"][-1] > res["equity"][-1])

    print("3. コストとドローダウン")
    flat = run_backtest([0.0, 0.0, 0.0], [1.0, 1.0, 1.0], cost_bps=100.0)
    # 1日目に0→1へ建てる。往復100bps=1%を1回だけ払う。
    check("建てたときだけコストがかかる", _close(flat["equity"][-1], 0.99, 1e-12),
          f"最終 {flat['equity'][-1]:.12f}")
    check("最大DDが正しい", _close(max_drawdown([1.0, 1.5, 0.75]), -0.5, 1e-12))
    check("リバランス幅: 幅未満は動かさない", _close(apply_band(0.55, 0.50, 0.10), 0.50))
    check("リバランス幅: 幅以上は目標まで動かす", _close(apply_band(0.65, 0.50, 0.10), 0.65))
    # 0.5 に建てたあと、0.55(幅未満・無視)→ 0.72(幅以上・建て替え)の2回だけ動く。
    banded = run_backtest([0.0] * 5, [0.0, 0.5, 0.55, 0.72, 0.75], cost_bps=0.0,
                          rebalance_band=0.10)
    check("リバランス幅で無駄な建て替えが消える", banded["trades"] == 2,
          f"売買回数 {banded['trades']}")
    unbanded = run_backtest([0.0] * 5, [0.0, 0.5, 0.55, 0.72, 0.75], cost_bps=0.0,
                            rebalance_band=0.0)
    check("幅0なら毎回建て替える", unbanded["trades"] == 3,
          f"売買回数 {unbanded['trades']}")
    check("上がり続ければDDは0", _close(max_drawdown([1.0, 1.1, 1.2]), 0.0, 1e-12))

    print("4. CSVの読み込み")
    # 桁区切りを含むCSVは、フィールドが引用されている(そうでないと列がずれる)。
    sample = 'Date,Open,High,Low,Close\n"2026-01-05","38,000.0","38,500.0","37,900.0","38,400.0"\n'
    sample += "2026-01-06,38400,38900,38200,38800\n"
    parsed = parse_ohlc_csv(sample)
    check("桁区切りと列名を読める", len(parsed) == 2 and _close(parsed[0]["close"], 38400.0),
          f"1行目終値 {parsed[0]['close'] if parsed else 'n/a'}")
    reversed_csv = "日付,終値\n2026/01/06,38800\n2026/01/05,38400\n"
    parsed_rev = parse_ohlc_csv(reversed_csv)
    check("降順のCSVを昇順に直す", parsed_rev[0]["date"] < parsed_rev[1]["date"])

    print("5. 戦略が未来を見ていないか(構造チェック)")
    # 途中を書き換えても、それより前のポジションは変わってはいけない。
    base = [100.0 + i for i in range(300)]
    tampered = base[:250] + [v * 3 for v in base[250:]]
    for name, fn in STRATEGIES.items():
        p_base = fn(base, synth_leveraged(pct_returns(base)), )
        p_tamp = fn(tampered, synth_leveraged(pct_returns(tampered)))
        same = all(_close(a, b, 1e-12) for a, b in zip(p_base[:250], p_tamp[:250]))
        check(f"{name}: 250日目以降を変えても前半のポジションは不変", same)

    print()
    if failures:
        print(f"FAILED: {len(failures)} 件 — {', '.join(failures)}")
        return 1
    print("すべて通過。")
    return 0


# --------------------------------------------------------------------------- CLI


def _strategy_params(args):
    return {
        "sma_window": args.sma_window,
        "target_vol": args.target_vol,
        "vol_window": args.vol_window,
    }


def cmd_backtest(args):
    rows = load_csv(args.csv)
    params = _strategy_params(args)
    names = [args.strategy] if args.strategy else list(STRATEGIES)

    def evaluate_slice(subset, title):
        stats_list = []
        for name in names:
            stats, _, _, _ = evaluate(subset, name, args.leverage, args.expense_ratio,
                                      args.cost_bps, args.exec_lag, params,
                                      args.rebalance_band)
            stats_list.append(stats)
        print_table(stats_list, title)
        return stats_list

    span = f"{rows[0]['date']} 〜 {rows[-1]['date']}  ({len(rows)}営業日)"
    print(f"日経平均: {span}")
    print(f"レバレッジ {args.leverage}倍 / 信託報酬 {args.expense_ratio * 100:.2f}%/年 "
          f"/ 往復コスト {args.cost_bps}bps / 約定遅延 {args.exec_lag}日 "
          f"/ リバランス幅 {args.rebalance_band}")

    # 指数そのものの成績も出す。レバレッジが効いているのかを見るため。
    closes = [r["close"] for r in rows]
    idx_eq = compound(pct_returns(closes))
    idx_stats = metrics(idx_eq, dates=[r["date"] for r in rows])
    idx_stats["strategy"] = "指数(1倍)"

    all_stats = evaluate_slice(rows, "全期間")
    print_table([idx_stats], "参考: 日経平均そのもの(レバレッジなし・コストなし)")

    if args.split and 0.0 < args.split < 1.0:
        cut = int(len(rows) * args.split)
        if cut > TRADING_DAYS and len(rows) - cut > TRADING_DAYS:
            # 期間を分けて、前半で良く見えた戦略が後半でも通用するかを見る。
            # ここが割れる戦略は、過去に合わせ込んだだけ。
            evaluate_slice(rows[:cut], f"前半 in-sample ({rows[0]['date']} 〜 {rows[cut - 1]['date']})")
            evaluate_slice(rows[cut:], f"後半 out-of-sample ({rows[cut]['date']} 〜 {rows[-1]['date']})")
        else:
            print("\n(期間が短いので in/out 分割は省略)")

    if args.json:
        Path(args.json).write_text(json.dumps(all_stats, ensure_ascii=False, indent=2),
                                   encoding="utf-8")
        print(f"\n{args.json} に書き出した。")
    return 0


def cmd_signal(args):
    rows = load_csv(args.csv)
    name = args.strategy or "sma_vol"
    stats, result, lev_returns, _ = evaluate(rows, name, args.leverage, args.expense_ratio,
                                             args.cost_bps, args.exec_lag,
                                             _strategy_params(args), args.rebalance_band)
    closes = [r["close"] for r in rows]
    positions = STRATEGIES[name](closes, lev_returns, **_strategy_params(args))

    latest = rows[-1]
    # いま実際に建っている量は、リバランス幅を通したあとの値。生のシグナルではない。
    held = result["positions"][-1]
    desired = positions[-1]
    order_to = apply_band(desired, held, args.rebalance_band)
    delta = order_to - held
    average = _sma(closes, len(closes) - 1, args.sma_window)
    vol = _realized_vol(lev_returns, len(lev_returns) - 1, args.vol_window)

    payload = {
        "as_of": latest["date"].isoformat(),
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "strategy": name,
        "close": latest["close"],
        f"sma{args.sma_window}": average,
        "realized_vol_2x": vol,
        "held_position": round(held, 4),
        "raw_signal": round(desired, 4),
        "target_position": round(order_to, 4),
        "delta": round(delta, 4),
        "action": ("hold" if abs(delta) < 1e-9 else ("buy" if delta > 0 else "sell")),
        "stale": latest["date"] < date.today(),
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"基準日        : {payload['as_of']}")
        print(f"日経平均終値  : {latest['close']:,.2f}")
        print(f"SMA{args.sma_window}        : " + (f"{average:,.2f}" if average else "n/a"))
        print(f"実現ボラ(2x)  : " + (f"{vol * 100:.1f}%" if vol else "n/a"))
        print(f"戦略          : {name}  (リバランス幅 {args.rebalance_band})")
        print(f"現在の建玉    : {held:.2f}")
        print(f"生のシグナル  : {desired:.2f}")
        print(f"目標ポジション: {order_to:.2f}  →  {payload['action']} {abs(delta):.2f}")
        print()
        print("※ これは目標ポジションであって注文ではない。発注は別系統で行うこと。")
        print("※ 建玉は「初日からこの戦略を回していたら」の値。実際の残高とは別に管理すること。")
    if latest["date"] < date.today():
        stale = (date.today() - latest["date"]).days
        print(f"\n警告: データが {stale} 日古い。最新の日足で再計算すること。", file=sys.stderr)
    return 0


def cmd_fetch(args):
    body = fetch_n225(args.url, args.timeout)
    rows = parse_ohlc_csv(body)  # 壊れたCSVを保存しないよう、先に読めるか確かめる
    Path(args.out).write_text(body, encoding="utf-8")
    print(f"{args.out} に {len(rows)} 営業日分を書き出した "
          f"({rows[0]['date']} 〜 {rows[-1]['date']})。")
    return 0


def build_parser():
    parser = argparse.ArgumentParser(
        description="日経平均レバレッジのシグナル生成とバックテスト",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    def add_common(p):
        p.add_argument("--csv", required=True, help="日経平均の日足CSV")
        p.add_argument("--strategy", choices=sorted(STRATEGIES), help="戦略(省略時は全比較)")
        p.add_argument("--leverage", type=float, default=DEFAULT_LEVERAGE)
        p.add_argument("--expense-ratio", type=float, default=DEFAULT_EXPENSE_RATIO,
                       help="信託報酬(年率、既定 0.008 = 0.80%%)")
        p.add_argument("--cost-bps", type=float, default=DEFAULT_COST_BPS,
                       help="往復の売買コスト(bps)")
        p.add_argument("--exec-lag", type=int, default=0,
                       help="約定をさらに遅らせる日数(既定0=翌日)")
        p.add_argument("--sma-window", type=int, default=200)
        p.add_argument("--target-vol", type=float, default=0.25)
        p.add_argument("--vol-window", type=int, default=20)
        p.add_argument("--rebalance-band", type=float, default=DEFAULT_REBALANCE_BAND,
                       help="この幅未満のポジション変更は行わない(既定0.10)")

    p_bt = sub.add_parser("backtest", help="戦略を過去データで比較する")
    add_common(p_bt)
    p_bt.add_argument("--split", type=float, default=0.6,
                      help="in-sample の比率(0で分割しない、既定0.6)")
    p_bt.add_argument("--json", help="結果をJSONで書き出す先")
    p_bt.set_defaults(func=cmd_backtest)

    p_sig = sub.add_parser("signal", help="最新日の目標ポジションを出す")
    add_common(p_sig)
    p_sig.add_argument("--json", action="store_true", help="JSONで出す")
    p_sig.set_defaults(func=cmd_signal)

    p_fetch = sub.add_parser("fetch", help="日経平均の日足CSVを取得する")
    p_fetch.add_argument("--out", default="n225.csv")
    p_fetch.add_argument("--url", default=N225_CSV_URL)
    p_fetch.add_argument("--timeout", type=int, default=30)
    p_fetch.set_defaults(func=cmd_fetch)

    p_self = sub.add_parser("selftest", help="計算式の自己検証(外部データ不要)")
    p_self.set_defaults(func=lambda args: selftest())

    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except DataError as exc:
        print(f"エラー: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
