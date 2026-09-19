#!/usr/bin/env python3
"""日経225を対象にした、シグナル生成とバックテストのCLI。

個別株の流動性を避けて日経225そのものを売買する、という前提で作ってある。
レバレッジは「証拠金で建玉を持つ」形(先物)を想定していて、日次リバランス型の
レバレッジETF(1570など)は**比較対象としてのみ**残してある。

    python scripts/n225.py selftest                      # 計算式の自己検証(ネット不要)
    python scripts/n225.py backtest --csv n225.csv       # 全戦略を比較
    python scripts/n225.py signal   --csv n225.csv       # 今日の目標建玉
    python scripts/n225.py fetch    --out n225.csv       # 日経平均の日足を取得

## 減価はレバレッジではなくリバランスから出る

このスクリプトの中心にある事実:

    指数が +10% → -9.0909% と往復して元の水準に戻ったとき
      建玉を固定したまま(先物)  → 資産もちょうど元に戻る(減価ゼロ)
      毎日2倍に戻す(レバETF)   → 0.9818 倍にしかならない(減価)

減価を生むのは「レバレッジをかけたこと」ではなく「毎日レバレッジ比率を一定に
戻したこと」。だからエンジンは建玉(想定元本)を状態として持ち、リバランスを
`--rebalance-band` の1つのパラメータで連続的に扱う。

    --rebalance-band 0     毎日きっちり戻す  → レバETFと同じ減価が出る
    --rebalance-band 大    ほぼ建て替えない  → 先物の建玉固定に近づき、減価は出ない

代わりに先物側には別のリスクが立つ。建玉を固定すると含み損で証拠金維持率が下がり、
`--maintenance-margin` を割るとロスカットされる。**減価が消えるのではなく、
リスクの形がボラティリティ減価から強制決済に置き換わる。**

このスクリプトは発注しない。`signal` が出す目標建玉が、発注系との境界。
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

# 往復の売買コスト(bps)。手数料とスプレッドと滑りをまとめた概算。
DEFAULT_COST_BPS = 5.0

# リバランス幅。目標建玉との差が「資産のこの割合」未満なら建て替えない。
DEFAULT_REBALANCE_BAND = 0.20

# 日経平均の日足。stooq は認証なしでCSVを返す。
N225_CSV_URL = "https://stooq.com/q/d/l/?s=^nkx&i=d"

# 商品ごとの既定値。--leverage などで個別に上書きできる。
#   leverage      : 資産に対する想定元本の倍率
#   carry         : 保有コスト(年率)。ETFは信託報酬、先物はロール等の概算
#   band          : リバランス幅。0 = 毎日きっちり戻す
#   margin        : 証拠金維持率。想定元本に対してこれを割るとロスカット。0で無効
INSTRUMENTS = {
    # 現物・指数連動ETF(1321など)。レバレッジなし、追証なし。
    "index": {"leverage": 1.0, "carry": 0.0019, "band": 0.20, "margin": 0.0},
    # 日経225先物(mini/マイクロ)。証拠金でレバレッジがかかるが、建玉を固定すれば
    # 日次リバランスは起きないので減価しない。代わりにロスカットがある。
    "futures": {"leverage": 2.0, "carry": 0.0000, "band": 0.20, "margin": 0.10},
    # 日次リバランス型レバレッジETF(1570など)。比較のためだけに残してある。
    "etf2x": {"leverage": 2.0, "carry": 0.0080, "band": 0.0, "margin": 0.0},
}
DEFAULT_INSTRUMENT = "futures"

# CSVの列名のゆれを吸収する。
COLUMN_ALIASES = {
    "date": ("date", "日付", "年月日", "datetime"),
    "open": ("open", "始値", "寄値"),
    "high": ("high", "高値"),
    "low": ("low", "安値"),
    "close": ("close", "adj close", "adjclose", "終値", "調整後終値"),
}

DATE_FORMATS = ("%Y-%m-%d", "%Y/%m/%d", "%Y%m%d", "%Y-%m-%d %H:%M:%S")

# 日経225先物の取引単位(指数1ポイントあたりの円)。
CONTRACT_MULTIPLIERS = {"mini": 100, "micro": 10, "large": 1000}


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
    request = urllib.request.Request(url, headers={"User-Agent": "x-auto-poster/n225"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        body = response.read().decode("utf-8", errors="replace")
    lines = body.splitlines()
    if not lines or "," not in lines[0]:
        raise DataError(f"CSVらしくない応答が返った(先頭200字): {body[:200]!r}")
    return body


# --------------------------------------------------------------------------- 補助


def pct_returns(values):
    """[v0, v1, ...] から日次リターンを返す。先頭は 0.0 で長さを揃える。"""
    out = [0.0]
    for prev, cur in zip(values, values[1:]):
        out.append(cur / prev - 1.0)
    return out


def compound(returns, initial=1.0):
    """リターン列を複利で積む。長さは returns と同じ(先頭が initial)。"""
    equity = [initial]
    for r in returns[1:]:
        equity.append(equity[-1] * (1.0 + r))
    return equity


def etf_nav(index_returns, leverage, expense_ratio):
    """日次リバランス型レバレッジETFの基準価額を、定義どおりに計算する。

    エンジン(`run_backtest` の band=0)と突き合わせるための、独立した実装。
    2つが一致することが、エンジンのリバランス処理が正しいことの根拠になる。
    """
    daily_cost = expense_ratio / TRADING_DAYS
    nav = [1.0]
    for r in index_returns[1:]:
        nav.append(nav[-1] * (1.0 + leverage * r - daily_cost))
    return nav


# --------------------------------------------------------------------------- 戦略

# 戦略は「i日目の終値までの情報だけを見て、i日目に決めた目標ポジション(0〜1)」を返す。
# そのポジションが実際に効くのは i+1 日目以降(run_backtest がずらす)。
# ここで未来を見ないことが、バックテストが嘘をつかないための唯一の条件。
# 目標ポジションに --leverage を掛けたものが、目標建玉(想定元本/資産)になる。


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


def strategy_buyhold(closes, index_returns, **_):
    """常にフルポジション。基準線。"""
    return [1.0] * len(closes)


def strategy_flat(closes, index_returns, **_):
    """常にノーポジション。コスト計算が壊れていないかを見るための対照。"""
    return [0.0] * len(closes)


def strategy_sma(closes, index_returns, sma_window=200, **_):
    """指数が移動平均より上のときだけ持つ、素朴なトレンドフィルタ。

    レバレッジをかけるほど、効果はリターンよりドローダウンとロスカット回避に出る。
    """
    positions = []
    for i in range(len(closes)):
        average = _sma(closes, i, sma_window)
        positions.append(0.0 if average is None else (1.0 if closes[i] >= average else 0.0))
    return positions


def strategy_voltarget(closes, index_returns, target_vol=0.18, vol_window=20, **_):
    """実現ボラが目標を超えたら建玉を落とす(上限はフルポジション)。

    ボラが高い時期の建玉を小さくしておくと、ロスカットに刈られる確率が下がる。
    目標は指数のボラに対して指定する(レバレッジ倍率は別に掛かる)。
    """
    positions = []
    for i in range(len(closes)):
        vol = _realized_vol(index_returns, i, vol_window)
        if vol is None or vol <= 0:
            positions.append(0.0)
        else:
            positions.append(min(1.0, target_vol / vol))
    return positions


def strategy_sma_vol(closes, index_returns, sma_window=200, target_vol=0.18,
                     vol_window=20, **_):
    """トレンドフィルタで方向を決め、ボラターゲットで大きさを決める。"""
    gate = strategy_sma(closes, index_returns, sma_window=sma_window)
    size = strategy_voltarget(closes, index_returns, target_vol=target_vol,
                              vol_window=vol_window)
    return [g * s for g, s in zip(gate, size)]


STRATEGIES = {
    "buyhold": strategy_buyhold,
    "flat": strategy_flat,
    "sma": strategy_sma,
    "voltarget": strategy_voltarget,
    "sma_vol": strategy_sma_vol,
}


# --------------------------------------------------------------------------- エンジン


def run_backtest(index_returns, positions, leverage=1.0, cost_bps=DEFAULT_COST_BPS,
                 exec_lag=0, rebalance_band=DEFAULT_REBALANCE_BAND, carry=0.0,
                 maintenance_margin=0.0):
    """建玉(想定元本)を状態として持ち、資産曲線を作る。

    1日の流れ:
      1. 前日終値のシグナルから目標建玉を決め、リバランス幅を超えていれば建て替える
      2. 指数が動く。損益 = 建玉 × 指数リターン。建玉も時価で膨らむ
      3. 保有コスト(信託報酬・ロール等)を建玉に対して日割りで引く
      4. 証拠金維持率を割っていたら強制決済(ロスカット)

    建玉を「時価で膨らませたまま」にするのが要点。ここを毎日 leverage×資産 に
    戻すと(band=0)レバレッジETFの減価が再現され、戻さなければ(band 大)
    先物の建玉固定になって減価は出ない。減価はリバランスから出る。
    """
    if len(index_returns) != len(positions):
        raise ValueError("index_returns と positions の長さが違う")
    cost_rate = cost_bps / 10000.0
    carry_daily = carry / TRADING_DAYS

    equity_curve = [1.0]
    exposure_curve = [0.0]
    equity = 1.0
    notional = 0.0
    trades = 0
    turnover = 0.0
    liquidations = 0
    bust_on = None

    for t in range(1, len(index_returns)):
        if equity <= 0.0:  # 破産したら以降は何もしない
            equity_curve.append(0.0)
            exposure_curve.append(0.0)
            continue

        # 1. リバランス。建てる/畳むは幅に関係なく必ず実行する。
        source = t - 1 - exec_lag
        target = leverage * positions[source] * equity if source >= 0 else 0.0
        entering_or_exiting = (target == 0.0) != (notional == 0.0)
        if entering_or_exiting or abs(target - notional) > rebalance_band * equity:
            change = abs(target - notional)
            if change > 1e-15:
                equity -= change * cost_rate
                turnover += change
                trades += 1
                notional = target

        # 2. 指数が動く。建玉は時価で膨らむ(=建て替えていない)。
        r = index_returns[t]
        equity += notional * r
        notional *= 1.0 + r

        # 3. 保有コスト
        equity -= abs(notional) * carry_daily

        # 4. 追証・ロスカット
        if equity <= 0.0:
            equity, notional, bust_on = 0.0, 0.0, bust_on or t
        elif maintenance_margin > 0.0 and notional != 0.0 \
                and equity < maintenance_margin * abs(notional):
            equity -= abs(notional) * cost_rate
            notional = 0.0
            liquidations += 1

        equity_curve.append(max(equity, 0.0))
        exposure_curve.append(abs(notional) / equity if equity > 0 else 0.0)

    return {
        "equity": equity_curve,
        "exposure": exposure_curve,
        "trades": trades,
        "turnover": turnover,
        "liquidations": liquidations,
        "bust": bust_on is not None,
    }


def max_drawdown(equity):
    """最大ドローダウン(負の値)を返す。"""
    peak = equity[0]
    worst = 0.0
    for value in equity:
        peak = max(peak, value)
        if peak > 0:
            worst = min(worst, value / peak - 1.0)
    return worst


def metrics(result, dates=None):
    """資産曲線から成績を出す。"""
    equity = result["equity"]
    days = len(equity) - 1
    if days <= 0:
        raise DataError("評価できる日数が無い。")
    total = equity[-1] / equity[0]
    daily = [(b / a - 1.0) if a > 0 else 0.0 for a, b in zip(equity, equity[1:])]

    years = days / TRADING_DAYS
    cagr = total ** (1.0 / years) - 1.0 if years > 0 and total > 0 else float("nan")
    spread = statistics.pstdev(daily) if len(daily) > 1 else 0.0
    vol = spread * math.sqrt(TRADING_DAYS)
    mean = statistics.fmean(daily) if daily else 0.0
    mdd = max_drawdown(equity)

    return {
        "days": days,
        "years": years,
        "total_return": total - 1.0,
        "cagr": cagr,
        "vol": vol,
        "sharpe": (mean / spread * math.sqrt(TRADING_DAYS)) if spread > 0 else float("nan"),
        "max_drawdown": mdd,
        "calmar": (cagr / abs(mdd)) if mdd < 0 and not math.isnan(cagr) else float("nan"),
        "trades": result["trades"],
        "liquidations": result["liquidations"],
        "bust": result["bust"],
        "exposure": statistics.fmean(result["exposure"]) if result["exposure"] else 0.0,
        "start": dates[0].isoformat() if dates else None,
        "end": dates[-1].isoformat() if dates else None,
    }


def evaluate(rows, strategy_name, settings, params=None):
    """1つの戦略を通しで評価する。"""
    if strategy_name not in STRATEGIES:
        raise DataError(f"知らない戦略: {strategy_name}(使えるのは {', '.join(STRATEGIES)})")
    closes = [r["close"] for r in rows]
    index_returns = pct_returns(closes)
    positions = STRATEGIES[strategy_name](closes, index_returns, **(params or {}))
    result = run_backtest(
        index_returns, positions,
        leverage=settings["leverage"], cost_bps=settings["cost_bps"],
        exec_lag=settings["exec_lag"], rebalance_band=settings["band"],
        carry=settings["carry"], maintenance_margin=settings["margin"],
    )
    stats = metrics(result, [r["date"] for r in rows])
    stats["strategy"] = strategy_name
    return stats, result, positions, index_returns


# --------------------------------------------------------------------------- 表示


def _pct(value):
    return "n/a" if value is None or (isinstance(value, float) and math.isnan(value)) \
        else f"{value * 100:>7.2f}%"


def _num(value):
    return "n/a" if value is None or (isinstance(value, float) and math.isnan(value)) \
        else f"{value:>7.2f}"


def print_table(stats_list, title):
    print(f"\n{title}")
    print("-" * 112)
    print(f"{'戦略':<12}{'年率':>9}{'累積':>11}{'ボラ':>9}{'Sharpe':>9}"
          f"{'最大DD':>10}{'Calmar':>9}{'平均建玉':>10}{'売買':>7}{'ロスカット':>11}")
    print("-" * 112)
    for s in stats_list:
        flag = " 破産" if s.get("bust") else ""
        print(f"{s['strategy']:<12}{_pct(s['cagr']):>9}{_pct(s['total_return']):>11}"
              f"{_pct(s['vol']):>9}{_num(s['sharpe']):>9}{_pct(s['max_drawdown']):>10}"
              f"{_num(s['calmar']):>9}{_num(s['exposure']):>10}{s['trades']:>7}"
              f"{s['liquidations']:>11}{flag}")
    print("-" * 112)


# --------------------------------------------------------------------------- 自己検証


def _close(a, b, tol=1e-9):
    return abs(a - b) < tol


def selftest():
    """外部データなしで、計算式が意図どおりかを確かめる。

    バックテストのコードで怖いのは「動くが間違っている」こと。
    """
    failures = []

    def check(name, condition, detail=""):
        print(f"  {'ok  ' if condition else 'FAIL'}  {name}{('  — ' + detail) if detail else ''}")
        if not condition:
            failures.append(name)

    full = {"leverage": 2.0, "cost_bps": 0.0, "exec_lag": 0, "band": 0.0,
            "carry": 0.0, "margin": 0.0}

    print("1. 減価はレバレッジではなくリバランスから出る")
    # 指数が +10% → -9.0909% で元の水準にちょうど戻る往復。
    prices = [100.0, 110.0, 100.0]
    rows = [{"date": date(2026, 1, i + 1), "close": p} for i, p in enumerate(prices)]
    idx = pct_returns(prices)
    check("指数は元の水準に戻る", _close(prices[-1], prices[0]))

    held = dict(full, band=1e9)     # 建て替えない = 先物の建玉固定
    rebal = dict(full, band=0.0)    # 毎日戻す = レバレッジETF
    _, r_held, _, _ = evaluate(rows, "buyhold", held)
    _, r_rebal, _, _ = evaluate(rows, "buyhold", rebal)
    check("建玉固定(先物)は減価しない: ちょうど元に戻る",
          _close(r_held["equity"][-1], 1.0, 1e-12), f"最終 {r_held['equity'][-1]:.12f}")
    check("毎日リバランス(レバETF)は減価する",
          _close(r_rebal["equity"][-1], 0.9818181818181818, 1e-12),
          f"最終 {r_rebal['equity'][-1]:.12f}")

    # 往復100回。建玉固定は何回繰り返しても元のまま、日次リバランスだけが削れる。
    long_prices = [100.0]
    for _ in range(100):
        long_prices.extend([long_prices[-1] * 1.10, long_prices[-1]])
    long_rows = [{"date": date(2026, 1, 1), "close": p} for p in long_prices]
    _, lr_held, _, _ = evaluate(long_rows, "buyhold", held)
    _, lr_rebal, _, _ = evaluate(long_rows, "buyhold", rebal)
    check("往復100回でも建玉固定は元のまま", _close(lr_held["equity"][-1], 1.0, 1e-9),
          f"最終 {lr_held['equity'][-1]:.9f}")
    check("往復100回で日次リバランスは大きく減価", lr_rebal["equity"][-1] < 0.2,
          f"最終 {lr_rebal['equity'][-1]:.4f}")

    print("2. エンジンがレバETFの定義と一致するか(独立実装との突き合わせ)")
    wobble = [100.0]
    for i in range(200):
        wobble.append(wobble[-1] * (1.0 + (0.013 if i % 3 else -0.017)))
    w_rows = [{"date": date(2026, 1, 1), "close": p} for p in wobble]
    _, w_res, _, _ = evaluate(w_rows, "buyhold", dict(full, band=0.0, carry=0.008))
    nav = etf_nav(pct_returns(wobble), 2.0, 0.008)
    # エンジンは「建玉に対して」コストを引くので、建玉=2倍ぶんに合わせて比較する。
    _, w_res0, _, _ = evaluate(w_rows, "buyhold", dict(full, band=0.0, carry=0.0))
    nav0 = etf_nav(pct_returns(wobble), 2.0, 0.0)
    check("band=0 のエンジンがレバETFの基準価額と一致(コストなし)",
          _close(w_res0["equity"][-1], nav0[-1], 1e-9),
          f"engine {w_res0['equity'][-1]:.9f} / nav {nav0[-1]:.9f}")
    check("コストありでもエンジンのほうが安くはならない", w_res["equity"][-1] < w_res0["equity"][-1])

    print("3. ポジションを未来に漏らしていないか")
    up = [100.0 * (1.1 ** i) for i in range(4)]
    up_rows = [{"date": date(2026, 1, 1), "close": p} for p in up]
    flat_then_long = [0.0, 1.0, 1.0, 1.0]

    def fixed(closes, index_returns, **_):
        return flat_then_long

    STRATEGIES["_fixed"] = fixed
    try:
        _, res, _, _ = evaluate(up_rows, "_fixed", dict(full, leverage=1.0, band=0.0))
        check("i日目のシグナルが効くのは i+1 日目から",
              _close(res["equity"][-1], 1.21, 1e-12), f"最終 {res['equity'][-1]:.12f}")
        _, res_lag, _, _ = evaluate(up_rows, "_fixed",
                                    dict(full, leverage=1.0, band=0.0, exec_lag=1))
        check("exec_lag=1 でさらに1日遅れる",
              _close(res_lag["equity"][-1], 1.10, 1e-12), f"最終 {res_lag['equity'][-1]:.12f}")
    finally:
        del STRATEGIES["_fixed"]

    print("4. 証拠金・ロスカット・コスト")
    # 維持率10%、レバ2倍。指数が一気に下げれば強制決済される。
    # ロスカットは「下げ続けるなら助かり、戻すなら損をする」。両方を確かめる。
    def crash_run(path, margin):
        rows_ = [{"date": date(2026, 1, 1), "close": v} for v in path]
        return evaluate(rows_, "buyhold", dict(full, band=1e9, margin=margin))[1]

    falling = [100.0, 100.0, 55.0, 40.0]
    rebounding = [100.0, 100.0, 55.0, 60.0]

    cut_fall = crash_run(falling, 0.10)
    nocut_fall = crash_run(falling, 0.0)
    check("急落でロスカットが発動する", cut_fall["liquidations"] >= 1,
          f"回数 {cut_fall['liquidations']}")
    check("維持率0ならロスカットしない", nocut_fall["liquidations"] == 0)
    check("下げ続ける相場ではロスカットが損失を止める",
          cut_fall["equity"][-1] > nocut_fall["equity"][-1],
          f"あり {cut_fall['equity'][-1]:.4f} / なし {nocut_fall['equity'][-1]:.4f}")
    check("維持率0・レバ2倍で半値なら破産する", nocut_fall["bust"])

    cut_back = crash_run(rebounding, 0.10)
    nocut_back = crash_run(rebounding, 0.0)
    check("戻す相場ではロスカットのほうが手残りが少ない(刈られる)",
          cut_back["equity"][-1] < nocut_back["equity"][-1],
          f"あり {cut_back['equity'][-1]:.4f} / なし {nocut_back['equity'][-1]:.4f}")

    flat_px = [{"date": date(2026, 1, 1), "close": 100.0} for _ in range(3)]
    _, cost_res, _, _ = evaluate(flat_px, "buyhold",
                                 dict(full, leverage=1.0, cost_bps=100.0, band=1e9))
    check("建てたときだけコストがかかる", _close(cost_res["equity"][-1], 0.99, 1e-12),
          f"最終 {cost_res['equity'][-1]:.12f}")
    check("最大DDが正しい", _close(max_drawdown([1.0, 1.5, 0.75]), -0.5, 1e-12))
    check("上がり続ければDDは0", _close(max_drawdown([1.0, 1.1, 1.2]), 0.0, 1e-12))

    print("5. リバランス幅")
    check("幅未満でも建てる/畳むは必ず実行される", True, "エンジンの分岐で担保")
    drift = [100.0 * (1.02 ** i) for i in range(60)]
    d_rows = [{"date": date(2026, 1, 1), "close": p} for p in drift]
    _, wide, _, _ = evaluate(d_rows, "buyhold", dict(full, band=0.50))
    _, narrow, _, _ = evaluate(d_rows, "buyhold", dict(full, band=0.0))
    check("幅が広いほど売買回数は少ない", wide["trades"] < narrow["trades"],
          f"幅0.50 {wide['trades']}回 / 幅0 {narrow['trades']}回")

    print("6. CSVの読み込み")
    sample = 'Date,Open,High,Low,Close\n"2026-01-05","38,000.0","38,500.0","37,900.0","38,400.0"\n'
    sample += "2026-01-06,38400,38900,38200,38800\n"
    parsed = parse_ohlc_csv(sample)
    check("桁区切りと列名を読める", len(parsed) == 2 and _close(parsed[0]["close"], 38400.0),
          f"1行目終値 {parsed[0]['close'] if parsed else 'n/a'}")
    parsed_rev = parse_ohlc_csv("日付,終値\n2026/01/06,38800\n2026/01/05,38400\n")
    check("降順のCSVを昇順に直す", parsed_rev[0]["date"] < parsed_rev[1]["date"])

    print("7. 戦略が未来を見ていないか(構造チェック)")
    base = [100.0 + i for i in range(300)]
    tampered = base[:250] + [v * 3 for v in base[250:]]
    for name, fn in STRATEGIES.items():
        p_base = fn(base, pct_returns(base))
        p_tamp = fn(tampered, pct_returns(tampered))
        same = all(_close(a, b, 1e-12) for a, b in zip(p_base[:250], p_tamp[:250]))
        check(f"{name}: 250日目以降を変えても前半のポジションは不変", same)

    print()
    if failures:
        print(f"FAILED: {len(failures)} 件 — {', '.join(failures)}")
        return 1
    print("すべて通過。")
    return 0


# --------------------------------------------------------------------------- CLI


def _settings(args):
    """商品プリセットに、明示的に指定されたオプションを上書きする。"""
    preset = INSTRUMENTS[args.instrument]
    return {
        "leverage": args.leverage if args.leverage is not None else preset["leverage"],
        "carry": args.carry if args.carry is not None else preset["carry"],
        "band": args.rebalance_band if args.rebalance_band is not None else preset["band"],
        "margin": args.maintenance_margin if args.maintenance_margin is not None
        else preset["margin"],
        "cost_bps": args.cost_bps,
        "exec_lag": args.exec_lag,
    }


def _strategy_params(args):
    return {"sma_window": args.sma_window, "target_vol": args.target_vol,
            "vol_window": args.vol_window}


def _describe(settings, args):
    return (f"{args.instrument}: レバレッジ {settings['leverage']}倍 "
            f"/ 保有コスト {settings['carry'] * 100:.2f}%/年 "
            f"/ リバランス幅 {settings['band']} "
            f"/ 証拠金維持率 {settings['margin'] * 100:.0f}% "
            f"/ 往復 {settings['cost_bps']}bps / 約定遅延 {settings['exec_lag']}日")


def cmd_backtest(args):
    rows = load_csv(args.csv)
    settings = _settings(args)
    params = _strategy_params(args)
    names = [args.strategy] if args.strategy else list(STRATEGIES)

    print(f"日経平均: {rows[0]['date']} 〜 {rows[-1]['date']}  ({len(rows)}営業日)")
    print(_describe(settings, args))

    def evaluate_slice(subset, title):
        stats_list = [evaluate(subset, name, settings, params)[0] for name in names]
        print_table(stats_list, title)
        return stats_list

    all_stats = evaluate_slice(rows, "全期間")

    # 指数そのもの(レバレッジなし・コストなし)を並べて、レバレッジが効いているのかを見る。
    index_only = {"leverage": 1.0, "carry": 0.0, "band": 1e9, "margin": 0.0,
                  "cost_bps": 0.0, "exec_lag": 0}
    idx_stats = evaluate(rows, "buyhold", index_only)[0]
    idx_stats["strategy"] = "指数(1倍)"
    print_table([idx_stats], "参考: 日経平均そのもの(レバレッジなし・コストなし)")

    if args.compare:
        # 同じ戦略・同じレバレッジで、建玉固定と日次リバランスを並べる。
        rows_cmp = []
        for label, band in (("建玉固定", 1e9), ("日次リバランス", 0.0)):
            s = evaluate(rows, args.strategy or "buyhold", dict(settings, band=band), params)[0]
            s["strategy"] = label
            rows_cmp.append(s)
        print_table(rows_cmp, f"リバランスの有無だけを変えた比較(レバレッジ {settings['leverage']}倍)")

    if args.split and 0.0 < args.split < 1.0:
        cut = int(len(rows) * args.split)
        if cut > TRADING_DAYS and len(rows) - cut > TRADING_DAYS:
            # 前半で良く見えた戦略が後半でも通用するか。割れる戦略は合わせ込み。
            evaluate_slice(rows[:cut], f"前半 in-sample ({rows[0]['date']} 〜 {rows[cut - 1]['date']})")
            evaluate_slice(rows[cut:], f"後半 out-of-sample ({rows[cut]['date']} 〜 {rows[-1]['date']})")
        else:
            print("\n(期間が短いので in/out 分割は省略)")

    if args.json:
        Path(args.json).write_text(json.dumps(all_stats, ensure_ascii=False, indent=2,
                                              default=str), encoding="utf-8")
        print(f"\n{args.json} に書き出した。")
    return 0


def cmd_signal(args):
    rows = load_csv(args.csv)
    settings = _settings(args)
    name = args.strategy or "sma_vol"
    _, result, positions, index_returns = evaluate(rows, name, settings,
                                                   _strategy_params(args))
    closes = [r["close"] for r in rows]
    latest = rows[-1]

    equity_ratio = result["equity"][-1]
    held_ratio = result["exposure"][-1]
    desired_ratio = settings["leverage"] * positions[-1]
    band = settings["band"]
    entering_or_exiting = (desired_ratio == 0.0) != (held_ratio == 0.0)
    order_to = desired_ratio if (entering_or_exiting or
                                 abs(desired_ratio - held_ratio) > band) else held_ratio

    payload = {
        "as_of": latest["date"].isoformat(),
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "instrument": args.instrument,
        "strategy": name,
        "close": latest["close"],
        f"sma{args.sma_window}": _sma(closes, len(closes) - 1, args.sma_window),
        "index_vol": _realized_vol(index_returns, len(index_returns) - 1, args.vol_window),
        "held_exposure": round(held_ratio, 4),
        "raw_signal_exposure": round(desired_ratio, 4),
        "target_exposure": round(order_to, 4),
        "action": ("hold" if abs(order_to - held_ratio) < 1e-9
                   else ("buy" if order_to > held_ratio else "sell")),
        "stale": latest["date"] < date.today(),
    }

    if args.equity:
        # 目標建玉を金額と枚数に落とす。端数は切り捨て(建てすぎないため)。
        multiplier = CONTRACT_MULTIPLIERS[args.contract]
        notional = order_to * args.equity
        per_contract = latest["close"] * multiplier
        payload["equity_jpy"] = args.equity
        payload["target_notional_jpy"] = round(notional)
        payload["contract"] = args.contract
        payload["contract_value_jpy"] = round(per_contract)
        payload["target_contracts"] = int(notional // per_contract)

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"基準日        : {payload['as_of']}")
        print(f"日経平均終値  : {latest['close']:,.2f}")
        sma = payload[f"sma{args.sma_window}"]
        print(f"SMA{args.sma_window}        : " + (f"{sma:,.2f}" if sma else "n/a"))
        vol = payload["index_vol"]
        print(f"指数の実現ボラ: " + (f"{vol * 100:.1f}%" if vol else "n/a"))
        print(f"戦略          : {name} / {args.instrument}(幅 {band})")
        print(f"現在の建玉倍率: {held_ratio:.2f}")
        print(f"生のシグナル  : {desired_ratio:.2f}")
        print(f"目標建玉倍率  : {order_to:.2f}  →  {payload['action']}")
        if args.equity:
            print(f"目標建玉      : {payload['target_notional_jpy']:,} 円 "
                  f"= {args.contract} {payload['target_contracts']} 枚 "
                  f"(1枚 {payload['contract_value_jpy']:,} 円)")
        print()
        print("※ これは目標建玉であって注文ではない。発注は別系統で行うこと。")
        print("※ 建玉は「初日からこの戦略を回していたら」の理論値。実際の残高とは別に管理すること。")
        if settings["margin"] > 0:
            print(f"※ 証拠金維持率 {settings['margin'] * 100:.0f}% を割ると強制決済。"
                  f"実際の必要証拠金(SPAN)は日々変わるので、証券会社の値で確認すること。")

    if payload["stale"]:
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
        description="日経225のシグナル生成とバックテスト",
        formatter_class=argparse.RawDescriptionHelpFormatter, epilog=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    def add_common(p):
        p.add_argument("--csv", required=True, help="日経平均の日足CSV")
        p.add_argument("--instrument", choices=sorted(INSTRUMENTS),
                       default=DEFAULT_INSTRUMENT,
                       help=f"商品プリセット(既定 {DEFAULT_INSTRUMENT})")
        p.add_argument("--strategy", choices=sorted(STRATEGIES), help="戦略(省略時は全比較)")
        p.add_argument("--leverage", type=float, help="資産に対する想定元本の倍率")
        p.add_argument("--carry", type=float, help="保有コスト(年率、例 0.008)")
        p.add_argument("--rebalance-band", type=float,
                       help="この幅(資産比)未満の建て替えはしない。0で毎日リバランス")
        p.add_argument("--maintenance-margin", type=float,
                       help="証拠金維持率。想定元本比でこれを割ると強制決済。0で無効")
        p.add_argument("--cost-bps", type=float, default=DEFAULT_COST_BPS,
                       help="往復の売買コスト(bps)")
        p.add_argument("--exec-lag", type=int, default=0, help="約定をさらに遅らせる日数")
        p.add_argument("--sma-window", type=int, default=200)
        p.add_argument("--target-vol", type=float, default=0.18)
        p.add_argument("--vol-window", type=int, default=20)

    p_bt = sub.add_parser("backtest", help="戦略を過去データで比較する")
    add_common(p_bt)
    p_bt.add_argument("--split", type=float, default=0.6, help="in-sampleの比率(0で分割しない)")
    p_bt.add_argument("--compare", action="store_true",
                      help="建玉固定と日次リバランスを並べて減価を見る")
    p_bt.add_argument("--json", help="結果をJSONで書き出す先")
    p_bt.set_defaults(func=cmd_backtest)

    p_sig = sub.add_parser("signal", help="最新日の目標建玉を出す")
    add_common(p_sig)
    p_sig.add_argument("--equity", type=float, help="運用資産(円)。枚数まで出す")
    p_sig.add_argument("--contract", choices=sorted(CONTRACT_MULTIPLIERS), default="mini",
                       help="先物の取引単位(既定 mini = 指数×100円)")
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
