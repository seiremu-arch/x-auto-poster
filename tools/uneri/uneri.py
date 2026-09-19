#!/usr/bin/env python3
"""ETF「うねり取り」(分割売買)のバックテストと日次シグナル。

うねり取りは、同じ銘柄を長く追い、平均回帰する波に対して買い下がり・売り上がりを
分割で行う手法。このスクリプトは判断を次の3つに固定して検証可能にする。

  1. 波の位置は25日移動平均からの乖離率で測る(終値ベースのみ、ザラ場は見ない)
  2. 買いは決めた段数(既定5段)まで。それ以上は何があっても買わない
  3. 売りは平均建値からの上昇率で分割して落とす

これに52週(252営業日)レンジの位置を重ねて、局面ごとに振る舞いを変えられる。
25日乖離が「波のどこにいるか」だけを見るのに対し、52週レンジは「その波が
年間のどのへんで起きているか」を見る。同じ乖離-5%でも、高値圏の押し目と
安値更新中の崩落は別物で、それを区別するための2本目のものさし。

依存は標準ライブラリのみ。取得(fetch)だけがネットワークを使う。

    python tools/uneri/uneri.py synth    --out /tmp/synth.csv --years 12
    python tools/uneri/uneri.py fetch    --ticker 1306.T --out data/1306.csv
    python tools/uneri/uneri.py backtest --csv data/1306.csv
    python tools/uneri/uneri.py sweep    --csv data/1306.csv
    python tools/uneri/uneri.py compare  --csv data/1306.csv
    python tools/uneri/uneri.py signal   --csv data/1306.csv --units 2 --avg-cost 2810
"""

import argparse
import csv
import io
import json
import math
import random
import sys
from collections import deque
from dataclasses import dataclass, field, replace
from datetime import date as Date
from datetime import timedelta

# ---------------------------------------------------------------- データ ----

# 証券会社のCSVは日本語ヘッダでShift_JISのことがある。よくある綴りを全部受ける。
COLUMN_ALIASES = {
    "date": ("date", "日付", "年月日", "timestamp", "time", "datetime"),
    "open": ("open", "始値", "寄付", "寄値", "始値(円)"),
    "high": ("high", "高値", "高値(円)"),
    "low": ("low", "安値", "安値(円)"),
    "close": ("close", "終値", "引値", "終値(円)"),
    "adjclose": ("adj close", "adjclose", "adj_close", "調整後終値", "調整済終値"),
    "volume": ("volume", "出来高", "売買高"),
}

ENCODINGS = ("utf-8-sig", "utf-8", "cp932", "shift_jis")


@dataclass(frozen=True)
class Bar:
    date: str
    open: float
    high: float
    low: float
    close: float


def _norm_header(name):
    return name.strip().strip('"').lower().replace(" ", "").replace("　", "")


def _resolve_columns(header):
    """ヘッダ行 → {論理名: 列インデックス}。見つからない論理名は入らない。"""
    normed = [_norm_header(h) for h in header]
    resolved = {}
    for logical, aliases in COLUMN_ALIASES.items():
        for alias in aliases:
            key = _norm_header(alias)
            if key in normed:
                resolved[logical] = normed.index(key)
                break
    return resolved


def _parse_number(text):
    if text is None:
        return None
    text = text.strip().strip('"').replace(",", "").replace("¥", "")
    if text in ("", "-", "--", "N/A", "null", "None"):
        return None
    try:
        return float(text)
    except ValueError:
        return None


def _parse_date(text):
    text = text.strip().strip('"')
    if "T" in text:  # ISO8601のタイムスタンプ
        text = text.split("T", 1)[0]
    if " " in text:
        text = text.split(" ", 1)[0]
    for sep in ("-", "/"):
        if sep in text:
            parts = text.split(sep)
            if len(parts) == 3:
                y, m, d = parts
                if len(y) == 4:
                    return "%04d-%02d-%02d" % (int(y), int(m), int(d))
    if len(text) == 8 and text.isdigit():  # 20260919
        return "%s-%s-%s" % (text[:4], text[4:6], text[6:])
    raise ValueError("日付として読めない: %r" % text)


def load_csv(path, use_adjusted=True):
    """日足CSVを読む。列名は英語/日本語のどちらでもよい。昇順に並べ直して返す。

    始値が無いCSV(終値だけのもの)は、始値=終値として扱う。この場合は翌日始値での
    執行が翌日終値での執行になるので、バックテストの結果はやや甘くなる。
    """
    raw = None
    for encoding in ENCODINGS:
        try:
            with open(path, "r", encoding=encoding, newline="") as fh:
                raw = fh.read()
            break
        except UnicodeDecodeError:
            continue
    if raw is None:
        raise SystemExit("CSVの文字コードが判別できない: %s" % path)

    reader = csv.reader(io.StringIO(raw))
    rows = [r for r in reader if any(cell.strip() for cell in r)]
    if not rows:
        raise SystemExit("CSVが空: %s" % path)

    cols = _resolve_columns(rows[0])
    if "date" not in cols or ("close" not in cols and "adjclose" not in cols):
        raise SystemExit(
            "日付と終値の列が見つからない。ヘッダ: %s" % ", ".join(rows[0][:10])
        )

    close_key = "adjclose" if (use_adjusted and "adjclose" in cols) else "close"
    if close_key not in cols:
        close_key = "close" if "close" in cols else "adjclose"

    bars = []
    for row in rows[1:]:
        if len(row) <= cols["date"]:
            continue
        try:
            day = _parse_date(row[cols["date"]])
        except ValueError:
            continue  # ヘッダの繰り返しや注記行
        close = _parse_number(row[cols[close_key]]) if cols[close_key] < len(row) else None
        if close is None or close <= 0:
            continue

        def pick(name, fallback):
            idx = cols.get(name)
            if idx is None or idx >= len(row):
                return fallback
            value = _parse_number(row[idx])
            return fallback if value is None or value <= 0 else value

        bars.append(
            Bar(
                date=day,
                open=pick("open", close),
                high=pick("high", close),
                low=pick("low", close),
                close=close,
            )
        )

    if not bars:
        raise SystemExit("有効な行が1本も無い: %s" % path)

    bars.sort(key=lambda b: b.date)
    deduped = [bars[0]]
    for bar in bars[1:]:
        if bar.date == deduped[-1].date:
            deduped[-1] = bar
        else:
            deduped.append(bar)
    return deduped


# ------------------------------------------------------------ 指標 --------


def sma(values, window):
    """単純移動平均。ウォームアップ期間はNone。"""
    out = [None] * len(values)
    total = 0.0
    for i, value in enumerate(values):
        total += value
        if i >= window:
            total -= values[i - window]
        if i >= window - 1:
            out[i] = total / window
    return out


def deviation_pct(price, mean):
    """移動平均からの乖離率(%)。"""
    if mean is None or mean == 0:
        return None
    return (price - mean) / mean * 100.0


def rolling_extreme(values, window, kind="max"):
    """窓内の最大(または最小)。窓が埋まるまではNone。

    単調デックでO(n)。52週(252営業日)を毎回なめ直すと sweep が遅くなるため。
    """
    out = [None] * len(values)
    queue = deque()
    if kind == "max":
        drop = lambda new, old: new >= old   # noqa: E731
    else:
        drop = lambda new, old: new <= old   # noqa: E731
    for i, value in enumerate(values):
        while queue and drop(value, values[queue[-1]]):
            queue.pop()
        queue.append(i)
        if queue[0] <= i - window:
            queue.popleft()
        if i >= window - 1:
            out[i] = values[queue[0]]
    return out


def range_position(price, high, low):
    """52週レンジの中での位置(0%=安値、100%=高値)。

    25日乖離が「波のどこか」なら、こちらは「その波が年間のどこで起きているか」。
    """
    if high is None or low is None:
        return None
    span = high - low
    if span <= 0:
        return 50.0
    return (price - low) / span * 100.0


# ------------------------------------------------------------ 戦略 --------


@dataclass
class Params:
    """うねり取りのルール一式。ここに書いてある値が、相場中に迷わないための約束。"""

    ma_short: int = 25          # 波の位置を測るものさし
    ma_long: int = 200          # 地合い(上昇相場か下降相場か)

    # 買い下がりの段。乖離率(%)がこの値以下になったら1段建てる。上から順に使う。
    buy_levels: tuple = (-3.0, -5.0, -7.0, -10.0, -13.0)
    unit_yen: float = 200_000.0   # 1段あたりの金額
    cooldown_days: int = 3        # 前の建玉から最低これだけ空ける(暴落日の一気買い防止)

    # 売り上がり。(平均建値からの上昇率%, その時点の建玉に対して落とす割合)
    take_profit: tuple = ((3.0, 1.0 / 3.0), (6.0, 0.5))
    exit_deviation: float = 4.0   # 25日乖離がこの値以上なら全部落とす
    exit_on_ma_long: bool = True  # 200日線を下から上抜いたら全部落とす

    # 撤退。満玉のときだけ発動する。Noneで無効(古典的うねり取りは損切りしない)。
    stop_loss_pct: float = -18.0
    stop_loss_fraction: float = 0.5

    # 52週(252営業日)レンジ。25日乖離とは別の時間軸で、局面を切り分けるために使う。
    # どちらもNoneなら52週は一切使わず、素のうねり取りになる。
    range_window: int = 252
    low_gate: float = None        # レンジ内位置がこの%以下なら新しい段を建てない
    block_after_new_low: int = 0  # 直近N営業日に52週安値を更新していたら建てない
    high_trail: float = None      # レンジ内位置がこの%以上なら刻まずに引っ張る
    trail_pct: float = 5.0        # 引っ張るときの、建玉後の高値からの許容下落幅

    lot_size: int = 10            # 売買単位(1306は10口、1321は1口)
    tax_rate: float = 0.20315     # 特定口座の申告分離課税
    fee_per_trade: float = 0.0    # ネット証券の現物ゼロコース前提
    exec_at: str = "next_open"    # "next_open" | "close"

    @property
    def max_units(self):
        return len(self.buy_levels)

    @property
    def capital(self):
        return self.unit_yen * self.max_units


@dataclass
class Trade:
    date: str
    side: str          # "BUY" / "SELL"
    price: float
    shares: int
    amount: float
    reason: str
    dev: float = None
    avg_cost: float = None
    realized: float = 0.0
    tax: float = 0.0


@dataclass
class Cycle:
    start: str
    end: str = None
    days: int = 0
    units: int = 0
    avg_cost: float = 0.0
    realized: float = 0.0
    realized_after_tax: float = 0.0
    peak_exposure: float = 0.0
    forced: bool = False   # データ終端での強制決済


@dataclass
class Result:
    params: Params
    start: str
    end: str
    years: float
    trades: list = field(default_factory=list)
    cycles: list = field(default_factory=list)
    equity: list = field(default_factory=list)      # (date, equity)
    realized: float = 0.0
    tax_paid: float = 0.0
    final_equity: float = 0.0
    days_in_market: int = 0
    total_days: int = 0
    mean_exposure: float = 0.0
    max_units_hit: int = 0
    stop_count: int = 0
    buyhold_final: float = 0.0
    buyhold_final_after_tax: float = 0.0
    skipped_units: int = 0
    blocked_by_low_gate: int = 0   # 52週安値圏で見送った段
    trail_engaged: int = 0         # 刻むのをやめて引っ張りに入ったサイクル数
    trail_exits: int = 0           # 引っ張りの下落幅に触れて手仕舞った回数


def _floor_lot(shares, lot):
    return int(shares // lot) * lot


class Backtest:
    """1銘柄・買い専のうねり取りを1本の価格系列に対して回す。

    建玉の原価は総平均法(特定口座と同じ)で管理する。税金は売却のたびに源泉され、
    損失は繰越して将来の利益と相殺する。
    """

    def __init__(self, bars, params):
        self.bars = bars
        self.p = params
        closes = [b.close for b in bars]
        self.ma_s = sma(closes, params.ma_short)
        self.ma_l = sma(closes, params.ma_long)
        self.dev = [deviation_pct(c, m) for c, m in zip(closes, self.ma_s)]

        window = params.range_window
        self.high52 = rolling_extreme(closes, window, "max")
        self.low52 = rolling_extreme(closes, window, "min")
        self.pos52 = [range_position(c, h, l)
                      for c, h, l in zip(closes, self.high52, self.low52)]
        # 窓が埋まるまで(最初の252本)は52週の判定ができない。そこでは素のうねり取り。
        self.new_low = [l is not None and c <= l + 1e-9
                        for c, l in zip(closes, self.low52)]
        self.new_high = [h is not None and c >= h - 1e-9
                         for c, h in zip(closes, self.high52)]

    # -- 建玉の状態 --------------------------------------------------------
    def _reset_cycle_state(self):
        self.units_built = 0
        self.tp_stage = 0
        self.stop_fired = False
        self.last_entry_i = None
        self.peak_since_entry = 0.0   # トレーリングの基準
        self.trail_seen = False       # このサイクルで引っ張りに入ったか
        self.cycle = None

    def run(self):
        p = self.p
        bars = self.bars
        cash = p.capital
        shares = 0
        cost_total = 0.0
        loss_pool = 0.0
        self._reset_cycle_state()

        res = Result(
            params=p,
            start=bars[0].date,
            end=bars[-1].date,
            years=self._years(),
            total_days=len(bars),
        )
        pending = None
        exposure_sum = 0.0

        def avg_cost():
            return cost_total / shares if shares else None

        def execute(order, price, day, dev):
            nonlocal cash, shares, cost_total, loss_pool
            side, qty, reason = order
            if side == "BUY":
                amount = price * qty + p.fee_per_trade
                if amount > cash + 1e-9:
                    qty = _floor_lot((cash - p.fee_per_trade) / price, p.lot_size)
                    if qty <= 0:
                        res.skipped_units += 1
                        return
                    amount = price * qty + p.fee_per_trade
                cash -= amount
                shares += qty
                cost_total += price * qty + p.fee_per_trade
                self.units_built += 1
                if self.cycle is None:
                    self.cycle = Cycle(start=day)
                self.cycle.units = self.units_built
                res.max_units_hit = max(res.max_units_hit, self.units_built)
                res.trades.append(
                    Trade(day, "BUY", price, qty, amount, reason, dev, avg_cost())
                )
            else:
                qty = min(qty, shares)
                if qty <= 0:
                    return
                basis = cost_total / shares * qty
                proceeds = price * qty - p.fee_per_trade
                gain = proceeds - basis
                tax = 0.0
                if gain > 0:
                    offset = min(loss_pool, gain)
                    loss_pool -= offset
                    tax = (gain - offset) * p.tax_rate
                else:
                    loss_pool += -gain
                cash += proceeds - tax
                cost_total -= basis
                shares -= qty
                res.realized += gain
                res.tax_paid += tax
                if self.cycle:
                    self.cycle.realized += gain
                    self.cycle.realized_after_tax += gain - tax
                res.trades.append(
                    Trade(day, "SELL", price, qty, proceeds, reason, dev,
                          avg_cost(), gain, tax)
                )
                if "撤退" in reason:
                    res.stop_count += 1
                if "引っ張り" in reason:
                    res.trail_exits += 1
                if shares == 0 and self.cycle:
                    self.cycle.end = day
                    self.cycle.days = _daydiff(self.cycle.start, day)
                    self.cycle.forced = "強制" in reason
                    res.cycles.append(self.cycle)
                    self._reset_cycle_state()

        self.res = res
        for i, bar in enumerate(bars):
            if pending is not None:
                execute(pending[0], bar.open, bar.date, pending[1])
                pending = None

            position_value = shares * bar.close
            equity = cash + position_value
            res.equity.append((bar.date, equity))
            exposure_sum += position_value
            if shares:
                res.days_in_market += 1
                self.peak_since_entry = max(self.peak_since_entry, bar.close)
                if self.cycle:
                    self.cycle.peak_exposure = max(
                        self.cycle.peak_exposure, position_value
                    )
                    self.cycle.avg_cost = avg_cost()

            if i == len(bars) - 1:
                break

            order = self._decide(i, shares, avg_cost())
            if order is None:
                continue
            if order[0] == "BUY":
                self.last_entry_i = i
            if p.exec_at == "close":
                execute(order, bar.close, bar.date, self.dev[i])
                res.equity[-1] = (bar.date, cash + shares * bar.close)
            else:
                pending = (order, self.dev[i])

        # データ終端で建玉が残っていたら最終終値で強制決済する。
        # ここを「含み益のまま」にすると成績が実態より良く見えるので必ず閉じる。
        if shares > 0:
            last = bars[-1]
            execute(("SELL", shares, "強制決済(データ終端)"), last.close,
                    last.date, self.dev[-1])
            res.equity[-1] = (last.date, cash)

        res.final_equity = cash + shares * bars[-1].close
        res.mean_exposure = exposure_sum / len(bars)
        res.buyhold_final, res.buyhold_final_after_tax = self._buyhold()
        return res

    # -- 判断 --------------------------------------------------------------
    def _decide(self, i, shares, avg):
        """バーiの終値を見て、出す注文を1つだけ決める。売りを買いより先に見る。"""
        p = self.p
        dev = self.dev[i]
        if dev is None:
            return None
        close = self.bars[i].close
        pos = self.pos52[i]

        if shares > 0 and avg:
            gain = (close - avg) / avg * 100.0

            # 高値圏では刻まない。
            # +3%で1/3ずつ落とすルールは、上げ相場で伸びを取り逃がす最大の原因。
            # 52週高値圏に出たら、分割利食いをやめて建玉後の高値からの下落で手仕舞う。
            if self._trailing(pos, gain):
                if not self.trail_seen:
                    self.trail_seen = True
                    self.res.trail_engaged += 1
                limit = self.peak_since_entry * (1.0 - p.trail_pct / 100.0)
                if close <= limit:
                    return ("SELL", shares, "引っ張り手仕舞い(高値から-%.1f%%)"
                            % p.trail_pct)
                return None   # 高値を更新している間は何もしない

            # 全部落とす: 乖離が伸びきった、または200日線を下から上抜いた
            if dev >= p.exit_deviation:
                return ("SELL", shares, "全利食い(乖離+%.1f%%)" % dev)
            if p.exit_on_ma_long and self._crossed_up_ma_long(i):
                return ("SELL", shares, "全利食い(200日線上抜け)")

            # 売り上がり(分割利食い)
            if self.tp_stage < len(p.take_profit):
                threshold, fraction = p.take_profit[self.tp_stage]
                if gain >= threshold:
                    qty = _floor_lot(shares * fraction, p.lot_size)
                    self.tp_stage += 1
                    if qty > 0:
                        return ("SELL", qty, "利食い%d段(+%.1f%%)" % (self.tp_stage, gain))
                    return None

            # 撤退: 満玉のときだけ、1サイクルに1回だけ
            if (
                p.stop_loss_pct is not None
                and not self.stop_fired
                and self.units_built >= p.max_units
                and gain <= p.stop_loss_pct
            ):
                qty = _floor_lot(shares * p.stop_loss_fraction, p.lot_size)
                self.stop_fired = True
                if qty > 0:
                    return ("SELL", qty, "撤退(%.1f%%)" % gain)
                return None

        # 買い下がり。段は上から順に1つずつ。同じ日に2段は建てない。
        if self.units_built < p.max_units:
            if self.last_entry_i is not None and i - self.last_entry_i < p.cooldown_days:
                return None
            level = p.buy_levels[self.units_built]
            if dev <= level:
                blocked = self._low_gate_blocks(i, pos)
                if blocked:
                    self.res.blocked_by_low_gate += 1
                    return None
                return ("BUY", self._unit_shares(i), "買い%d段(乖離%.1f%%%s)"
                        % (self.units_built + 1, dev,
                           "" if pos is None else ", 52週%.0f%%" % pos))
        return None

    def _trailing(self, pos, gain):
        """刻まずに引っ張る局面かどうか。

        入る条件は、利食いを始める水準まで含み益が乗っていて、かつ52週高値圏に
        いること。含み損の場面では発動しないので、撤退ルールとは干渉しない。

        一度入ったら、そのサイクルが終わるまで引っ張り続ける。押し目を付けた
        瞬間にレンジ内位置は下がるので、都度判定にすると「引っ張ると決めた直後に
        引っ張るのをやめる」という無意味な動きになる。乗ると決めたら降りるのは
        高値からの下落幅だけ、にしてある。
        """
        p = self.p
        if p.high_trail is None or not p.take_profit:
            return False
        if self.trail_seen:
            return True
        if pos is None:
            return False
        return pos >= p.high_trail and gain >= p.take_profit[0][0]

    def _low_gate_blocks(self, i, pos):
        """52週安値圏で買い下がりを止めるかどうか。

        乖離はトレンド下落でも常にマイナスになるので、25日線だけを見ていると
        崩落の途中で段が次々埋まる。52週の位置は、それが「波の底」なのか
        「年間で最も安い場所を更新し続けている最中」なのかを切り分ける。
        """
        p = self.p
        if p.low_gate is not None and pos is not None and pos <= p.low_gate:
            return True
        if p.block_after_new_low > 0:
            start = max(0, i - p.block_after_new_low + 1)
            if any(self.new_low[start:i + 1]):
                return True
        return False

    def _unit_shares(self, i):
        price = self.bars[i + 1].open if self.p.exec_at == "next_open" else self.bars[i].close
        qty = _floor_lot(self.p.unit_yen / price, self.p.lot_size)
        return max(qty, 0)

    def _crossed_up_ma_long(self, i):
        if i == 0:
            return False
        now, prev = self.ma_l[i], self.ma_l[i - 1]
        if now is None or prev is None:
            return False
        return self.bars[i].close >= now and self.bars[i - 1].close < prev

    # -- 比較対象 ----------------------------------------------------------
    def _buyhold(self):
        """同じ資金で初日に買って最後まで持った場合。うねり取りはこれに勝つ必要がある。"""
        p = self.p
        price = self.bars[0].open
        qty = _floor_lot(p.capital / price, p.lot_size)
        if qty <= 0:
            return p.capital, p.capital
        cash = p.capital - price * qty
        final = cash + qty * self.bars[-1].close
        gain = final - p.capital
        after = final - max(gain, 0.0) * p.tax_rate
        return final, after

    def _years(self):
        return max(_daydiff(self.bars[0].date, self.bars[-1].date) / 365.25, 1e-9)


def _daydiff(a, b):
    ay, am, ad = (int(x) for x in a.split("-"))
    by, bm, bd = (int(x) for x in b.split("-"))
    return (Date(by, bm, bd) - Date(ay, am, ad)).days


def max_drawdown(equity):
    """エクイティカーブの最大ドローダウン(率, 金額)。"""
    peak = -float("inf")
    worst_rate = 0.0
    worst_amount = 0.0
    for _, value in equity:
        peak = max(peak, value)
        if peak > 0:
            drop = peak - value
            if drop / peak > worst_rate:
                worst_rate = drop / peak
                worst_amount = drop
    return worst_rate, worst_amount


# ------------------------------------------------------------ 出力 --------


def _yen(value):
    return "%s%s円" % ("-" if value < 0 else "", format(int(round(abs(value))), ","))


def _cagr(final, initial, years):
    if initial <= 0 or final <= 0:
        return float("nan")
    return (final / initial) ** (1.0 / years) - 1.0


def format_report(res, show_trades=0):
    p = res.params
    out = []
    add = out.append

    add("=" * 62)
    add("うねり取り バックテスト")
    add("=" * 62)
    add("期間            : %s 〜 %s (%.1f年, %d営業日)"
        % (res.start, res.end, res.years, res.total_days))
    add("投入上限        : %s (%s × %d段)"
        % (_yen(p.capital), _yen(p.unit_yen), p.max_units))
    add("買い下がりの段  : %s" % ", ".join("%.1f%%" % x for x in p.buy_levels))
    add("売り上がり      : %s / 乖離+%.1f%%で全利食い"
        % (", ".join("+%.1f%%で%.0f%%" % (t, f * 100) for t, f in p.take_profit),
           p.exit_deviation))
    add("撤退            : %s"
        % ("なし" if p.stop_loss_pct is None
           else "満玉かつ平均建値%.1f%%で建玉の%.0f%%"
                % (p.stop_loss_pct, p.stop_loss_fraction * 100)))
    add("執行            : %s / 売買単位%d口 / 税率%.3f%%"
        % ("翌日始値" if p.exec_at == "next_open" else "当日終値",
           p.lot_size, p.tax_rate * 100))
    uses52 = p.low_gate is not None or p.block_after_new_low or p.high_trail is not None
    if uses52:
        parts = []
        if p.low_gate is not None:
            parts.append("レンジ内位置%.0f%%以下では買わない" % p.low_gate)
        if p.block_after_new_low:
            parts.append("52週安値更新から%d営業日は買わない" % p.block_after_new_low)
        if p.high_trail is not None:
            parts.append("レンジ内位置%.0f%%以上では刻まず高値から-%.1f%%で手仕舞い"
                         % (p.high_trail, p.trail_pct))
        add("52週(%d日)      : %s" % (p.range_window, " / ".join(parts)))
    else:
        add("52週            : 使わない(素のうねり取り)")
    add("")

    profit = res.final_equity - p.capital
    add("-" * 62)
    add("【成績】")
    add("  最終資産      : %s (元本 %s)" % (_yen(res.final_equity), _yen(p.capital)))
    add("  税引後損益    : %s (%.2f%%)" % (_yen(profit), profit / p.capital * 100))
    add("  年率(税引後)  : %.2f%%" % (_cagr(res.final_equity, p.capital, res.years) * 100))
    add("  実現損益(税前): %s   納税額: %s" % (_yen(res.realized), _yen(res.tax_paid)))
    dd_rate, dd_amount = max_drawdown(res.equity)
    add("  最大DD        : %.2f%% (%s)" % (dd_rate * 100, _yen(dd_amount)))
    add("")

    add("【バイ&ホールドとの比較】同じ%sを初日に投入した場合" % _yen(p.capital))
    bh_profit = res.buyhold_final_after_tax - p.capital
    add("  最終資産      : %s (税引後)" % _yen(res.buyhold_final_after_tax))
    add("  税引後損益    : %s (%.2f%%)" % (_yen(bh_profit), bh_profit / p.capital * 100))
    add("  年率(税引後)  : %.2f%%"
        % (_cagr(res.buyhold_final_after_tax, p.capital, res.years) * 100))
    add("  → うねり取りの差 : %s" % _yen(profit - bh_profit))
    add("")

    add("【資金の使われ方】うねり取りは資金を遊ばせる。ここが勝敗の前提条件になる。")
    add("  建玉していた日 : %d / %d日 (%.1f%%)"
        % (res.days_in_market, res.total_days,
           res.days_in_market / res.total_days * 100))
    add("  平均建玉率     : %.1f%% (平均 %s を投下)"
        % (res.mean_exposure / p.capital * 100, _yen(res.mean_exposure)))
    if res.mean_exposure > 0:
        add("  投下資本あたり : 年率換算 %.2f%%"
            % (res.realized / res.mean_exposure / res.years * 100))
    add("")

    add("【サイクル】")
    closed = res.cycles
    if not closed:
        add("  1サイクルも成立しなかった。段が深すぎるか、期間が短い。")
    else:
        wins = [c for c in closed if c.realized > 0]
        add("  回数          : %d回 (年%.1f回)" % (len(closed), len(closed) / res.years))
        add("  勝率          : %.1f%% (%d勝%d敗)"
            % (len(wins) / len(closed) * 100, len(wins), len(closed) - len(wins)))
        add("  平均保有日数  : %.0f日"
            % (sum(c.days for c in closed) / len(closed)))
        add("  平均損益      : %s (勝ち平均 %s / 負け平均 %s)"
            % (_yen(sum(c.realized for c in closed) / len(closed)),
               _yen(sum(c.realized for c in wins) / len(wins)) if wins else "—",
               _yen(sum(c.realized for c in closed if c.realized <= 0)
                    / max(len(closed) - len(wins), 1))))
        histogram = {}
        for cycle in closed:
            histogram[cycle.units] = histogram.get(cycle.units, 0) + 1
        add("  到達段数の分布: %s"
            % ", ".join("%d段:%d回" % (k, histogram[k]) for k in sorted(histogram)))
        add("  満玉到達      : %d回 / 撤退発動 %d回"
            % (histogram.get(p.max_units, 0), res.stop_count))
        forced = [c for c in closed if c.forced]
        if forced:
            add("  ※ 最後の1回はデータ終端での強制決済(実運用では継続中の建玉)")
    if res.skipped_units:
        add("  ※ 資金不足で見送った段: %d回" % res.skipped_units)
    if uses52:
        add("")
        add("【52週フィルタの効き方】")
        add("  安値圏で見送った段 : %d回" % res.blocked_by_low_gate)
        add("  引っ張りに入った   : %d回 / 全%d決済サイクル"
            % (res.trail_engaged, len(closed)))
        add("  引っ張りで手仕舞い : %d回 (残りは高値圏を外れて通常の利食いに戻った)"
            % res.trail_exits)
        if res.blocked_by_low_gate == 0 and res.trail_engaged == 0:
            add("  → 一度も発動していない。閾値が厳しすぎる。")

    if show_trades:
        add("")
        add("【直近の売買 %d件】" % show_trades)
        add("  %-10s %-4s %9s %7s %12s  %s"
            % ("日付", "売買", "単価", "口数", "実現損益", "理由"))
        for trade in res.trades[-show_trades:]:
            add("  %-10s %-4s %9.1f %7d %12s  %s"
                % (trade.date, trade.side, trade.price, trade.shares,
                   _yen(trade.realized) if trade.side == "SELL" else "—", trade.reason))
    add("=" * 62)
    return "\n".join(out)


# ------------------------------------------------------------ CLI ---------


def _params_from_args(args):
    p = Params()
    if args.levels:
        p = replace(p, buy_levels=tuple(float(x) for x in args.levels.split(",")))
    if args.unit is not None:
        p = replace(p, unit_yen=float(args.unit))
    if args.lot is not None:
        p = replace(p, lot_size=int(args.lot))
    if args.ma is not None:
        p = replace(p, ma_short=int(args.ma))
    if args.cooldown is not None:
        p = replace(p, cooldown_days=int(args.cooldown))
    if args.tp:
        stages = []
        for chunk in args.tp.split(","):
            threshold, fraction = chunk.split(":")
            stages.append((float(threshold), float(fraction)))
        p = replace(p, take_profit=tuple(stages))
    if args.exit_dev is not None:
        p = replace(p, exit_deviation=float(args.exit_dev))
    if args.no_stop:
        p = replace(p, stop_loss_pct=None)
    elif args.stop is not None:
        p = replace(p, stop_loss_pct=float(args.stop))
    if args.exec_at:
        p = replace(p, exec_at=args.exec_at)
    if args.fee is not None:
        p = replace(p, fee_per_trade=float(args.fee))
    if args.range_window is not None:
        p = replace(p, range_window=int(args.range_window))
    if args.low_gate is not None:
        p = replace(p, low_gate=float(args.low_gate))
    if args.block_after_new_low is not None:
        p = replace(p, block_after_new_low=int(args.block_after_new_low))
    if args.high_trail is not None:
        p = replace(p, high_trail=float(args.high_trail))
    if args.trail_pct is not None:
        p = replace(p, trail_pct=float(args.trail_pct))
    return p


def cmd_backtest(args):
    bars = load_csv(args.csv, use_adjusted=not args.raw_close)
    params = _params_from_args(args)
    if len(bars) < params.ma_long + 20:
        print("警告: %d本しかない。200日線が効くまでの期間が足りない。" % len(bars),
              file=sys.stderr)
    res = Backtest(bars, params).run()
    print(format_report(res, show_trades=args.trades))
    if args.out_trades:
        with open(args.out_trades, "w", encoding="utf-8", newline="") as fh:
            writer = csv.writer(fh)
            writer.writerow(["日付", "売買", "単価", "口数", "約定額",
                             "平均建値", "乖離率", "実現損益", "税", "理由"])
            for t in res.trades:
                writer.writerow([t.date, t.side, "%.2f" % t.price, t.shares,
                                 "%.0f" % t.amount,
                                 "" if t.avg_cost is None else "%.2f" % t.avg_cost,
                                 "" if t.dev is None else "%.2f" % t.dev,
                                 "%.0f" % t.realized, "%.0f" % t.tax, t.reason])
        print("玉帳を書き出した: %s" % args.out_trades)
    if args.out_equity:
        with open(args.out_equity, "w", encoding="utf-8", newline="") as fh:
            writer = csv.writer(fh)
            writer.writerow(["日付", "資産"])
            for day, value in res.equity:
                writer.writerow([day, "%.0f" % value])
        print("エクイティカーブを書き出した: %s" % args.out_equity)
    return 0


def cmd_sweep(args):
    """段の設計を総当たりで比べる。最適値を拾う道具ではなく、感度を見る道具。"""
    bars = load_csv(args.csv, use_adjusted=not args.raw_close)
    base = _params_from_args(args)
    firsts = [float(x) for x in args.first.split(",")]
    spacings = [float(x) for x in args.spacing.split(",")]
    tp1s = [float(x) for x in args.tp1.split(",")]

    rows = []
    for first in firsts:
        for spacing in spacings:
            levels = tuple(first - spacing * i for i in range(args.units))
            for tp1 in tp1s:
                params = replace(
                    base,
                    buy_levels=levels,
                    unit_yen=base.capital / args.units,
                    take_profit=((tp1, 1.0 / 3.0), (tp1 * 2, 0.5)),
                )
                res = Backtest(bars, params).run()
                dd, _ = max_drawdown(res.equity)
                rows.append({
                    "first": first, "spacing": spacing, "tp1": tp1,
                    "profit": res.final_equity - params.capital,
                    "cagr": _cagr(res.final_equity, params.capital, res.years) * 100,
                    "dd": dd * 100,
                    "cycles": len(res.cycles),
                    "exposure": res.mean_exposure / params.capital * 100,
                })

    rows.sort(key=lambda r: r["profit"], reverse=True)
    bh = Backtest(bars, base).run()
    print("期間 %s 〜 %s / バイ&ホールド(税引後)の年率 %.2f%%"
          % (bars[0].date, bars[-1].date,
             _cagr(bh.buyhold_final_after_tax, base.capital, bh.years) * 100))
    print()
    print("%7s %8s %6s %14s %8s %8s %7s %9s"
          % ("1段目", "段の間隔", "利食い", "税引後損益", "年率", "最大DD", "回数", "平均建玉率"))
    print("-" * 78)
    for row in rows[: args.top]:
        print("%6.1f%% %7.1f%% %5.1f%% %14s %7.2f%% %7.2f%% %7d %8.1f%%"
              % (row["first"], row["spacing"], row["tp1"], _yen(row["profit"]),
                 row["cagr"], row["dd"], row["cycles"], row["exposure"]))
    print()
    print("※ 上位が「正しい」わけではない。過去に最も合った形は、たいてい過剰適合。")
    print("   見るべきは、パラメータを少し動かしたときに成績が崩れないかどうか。")
    return 0


def cmd_compare(args):
    """52週フィルタを入れた場合と入れない場合を並べる。

    「効く/効かない」は相場付きに強く依存する。1本の系列で出た差を
    そのまま信じないこと。上げ相場と横ばい相場の両方で見る。
    """
    bars = load_csv(args.csv, use_adjusted=not args.raw_close)
    base = _params_from_args(args)
    base = replace(base, low_gate=None, block_after_new_low=0, high_trail=None)

    variants = [
        ("素のうねり取り", {}),
        ("安値圏で買わない", {"low_gate": args.low_gate_at}),
        ("新安値後は買わない", {"block_after_new_low": args.block_days}),
        ("高値圏で引っ張る", {"high_trail": args.high_trail_at,
                              "trail_pct": args.trail}),
        ("安値ゲート＋引っ張り", {"low_gate": args.low_gate_at,
                                  "high_trail": args.high_trail_at,
                                  "trail_pct": args.trail}),
    ]

    reference = None
    rows = []
    for label, overrides in variants:
        params = replace(base, **overrides)
        res = Backtest(bars, params).run()
        dd, _ = max_drawdown(res.equity)
        profit = res.final_equity - params.capital
        if reference is None:
            reference = profit
        rows.append((label, profit, _cagr(res.final_equity, params.capital,
                                          res.years) * 100, dd * 100,
                     len(res.cycles), res.mean_exposure / params.capital * 100,
                     res.blocked_by_low_gate, res.trail_engaged, profit - reference))

    bh = Backtest(bars, base).run()
    print("期間 %s 〜 %s (%.1f年)" % (bars[0].date, bars[-1].date, bh.years))
    print("バイ&ホールド(税引後): %s / 年率 %.2f%%"
          % (_yen(bh.buyhold_final_after_tax - base.capital),
             _cagr(bh.buyhold_final_after_tax, base.capital, bh.years) * 100))
    print()
    print("%-22s %13s %7s %7s %6s %8s %6s %6s %12s"
          % ("形", "税引後損益", "年率", "最大DD", "回数", "平均建玉率",
             "見送り", "引張り", "素との差"))
    print("-" * 100)
    for label, profit, cagr, dd, cycles, exposure, blocked, trails, diff in rows:
        print("%-22s %13s %6.2f%% %6.2f%% %6d %7.1f%% %6d %6d %12s"
              % (label, _yen(profit), cagr, dd, cycles, exposure,
                 blocked, trails, "—" if diff == 0 else _yen(diff)))
    print()
    print("※ 「見送り」は52週安値圏で建てなかった段の数、「引張り」は刻むのを")
    print("   やめたサイクル数。どちらも0なら、そのフィルタは発動していない。")
    return 0


def cmd_signal(args):
    """今日どうするかを1画面で出す。毎晩これを見て玉帳に書く。"""
    bars = load_csv(args.csv, use_adjusted=not args.raw_close)
    params = _params_from_args(args)
    closes = [b.close for b in bars]
    ma_s = sma(closes, params.ma_short)
    ma_l = sma(closes, params.ma_long)
    i = len(bars) - 1
    bar = bars[i]
    dev = deviation_pct(bar.close, ma_s[i])

    print("=" * 56)
    print("%s 終値 %.1f" % (bar.date, bar.close))
    print("=" * 56)
    if ma_s[i] is None:
        print("%d日線がまだ出ない(データ不足)" % params.ma_short)
        return 1
    print("  %d日線 %.1f / 乖離 %+.2f%%" % (params.ma_short, ma_s[i], dev))
    high52 = rolling_extreme(closes, params.range_window, "max")[i]
    low52 = rolling_extreme(closes, params.range_window, "min")[i]
    pos = range_position(bar.close, high52, low52)
    if pos is None:
        print("  52週レンジ まだ出ない(%d本必要、現在%d本)"
              % (params.range_window, len(bars)))
    else:
        print("  52週高値 %.1f / 安値 %.1f / レンジ内位置 %.0f%%%s"
              % (high52, low52, pos,
                 "  ★52週高値を更新中" if bar.close >= high52 - 1e-9 else
                 "  ★52週安値を更新中" if bar.close <= low52 + 1e-9 else ""))
    if ma_l[i] is not None:
        side = "上" if bar.close >= ma_l[i] else "下"
        print("  %d日線 %.1f / 終値はその%s → 地合いは%s"
              % (params.ma_long, ma_l[i], side, "上昇" if side == "上" else "下降"))
    else:
        print("  %d日線 まだ出ない" % params.ma_long)
    print()

    print("【買い下がり】現在 %d段建て" % args.units)
    for n, level in enumerate(params.buy_levels, start=1):
        if n <= args.units:
            mark, note = "済", ""
        elif n == args.units + 1:
            hit = dev <= level
            mark = "→" if hit else " "
            note = "  ★条件を満たしている" if hit else "  (あと%.2f%%)" % (dev - level)
        else:
            mark, note = " ", "  (待機)"
        print("  %s %d段目 乖離%.1f%%以下%s" % (mark, n, level, note))
    if args.units >= params.max_units:
        print("  満玉。これ以上は何があっても買わない。")
    if pos is not None and params.low_gate is not None and pos <= params.low_gate:
        print("  ✕ 52週安値圏(%.0f%% ≦ %.0f%%)のため、段の条件を満たしても買わない。"
              % (pos, params.low_gate))
    print()

    if args.units > 0 and args.avg_cost:
        gain = (bar.close - args.avg_cost) / args.avg_cost * 100
        print("【売り上がり】平均建値 %.1f / 現在 %+.2f%%" % (args.avg_cost, gain))
        for n, (threshold, fraction) in enumerate(params.take_profit, start=1):
            hit = gain >= threshold
            print("  %s 利食い%d段 +%.1f%%で建玉の%.0f%%%s"
                  % ("→" if hit else " ", n, threshold, fraction * 100,
                     "  ★条件を満たしている" if hit else ""))
        if (params.high_trail is not None and pos is not None
                and pos >= params.high_trail and gain >= params.take_profit[0][0]):
            print("  ※ 52週高値圏(%.0f%% ≧ %.0f%%)なので刻まない。"
                  % (pos, params.high_trail))
            print("     建玉後の高値から-%.1f%%まで引っ張る。" % params.trail_pct)
        print("  %s 全利食い  乖離+%.1f%%以上"
              % ("→" if dev >= params.exit_deviation else " ", params.exit_deviation))
        if params.stop_loss_pct is not None and args.units >= params.max_units:
            print("  %s 撤退      %.1f%%で建玉の%.0f%%"
                  % ("→" if gain <= params.stop_loss_pct else " ",
                     params.stop_loss_pct, params.stop_loss_fraction * 100))
    elif args.units > 0:
        print("【売り上がり】--avg-cost を渡すと判定する")
    print("=" * 56)
    return 0


def cmd_fetch(args):
    """Yahoo Financeの日足を取る。ネットワークが通らない環境では手動DLに切り替えること。"""
    import urllib.error
    import urllib.request

    url = (
        "https://query1.finance.yahoo.com/v8/finance/chart/%s"
        "?range=%s&interval=1d&events=div%%2Csplit" % (args.ticker, args.range)
    )
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
        print("取得に失敗: %s" % exc, file=sys.stderr)
        print(
            "\nネットワークが塞がれている環境ではここは通らない。手動で用意する:\n"
            "  1. Yahoo!ファイナンス等から日足CSVをダウンロード\n"
            "  2. 証券会社の履歴CSV(Shift_JIS・日本語ヘッダ)でもそのまま読める\n"
            "  3. 列は 日付 / 始値 / 高値 / 安値 / 終値 があればよい\n"
            "  4. 動作確認だけなら: uneri.py synth --out /tmp/synth.csv",
            file=sys.stderr,
        )
        return 1

    result = payload["chart"]["result"][0]
    stamps = result["timestamp"]
    quote = result["indicators"]["quote"][0]
    adj = result["indicators"].get("adjclose", [{}])[0].get("adjclose")

    rows = []
    for n, stamp in enumerate(stamps):
        close = quote["close"][n]
        if close is None:
            continue
        day = (Date(1970, 1, 1) + timedelta(seconds=int(stamp))).isoformat()
        rows.append([
            day,
            quote["open"][n] if quote["open"][n] is not None else close,
            quote["high"][n] if quote["high"][n] is not None else close,
            quote["low"][n] if quote["low"][n] is not None else close,
            close,
            adj[n] if adj and adj[n] is not None else close,
        ])

    with open(args.out, "w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["Date", "Open", "High", "Low", "Close", "Adj Close"])
        writer.writerows(rows)
    print("%d本を書き出した: %s (%s 〜 %s)"
          % (len(rows), args.out, rows[0][0], rows[-1][0]))
    return 0


def cmd_synth(args):
    """検証用の合成日足。トレンド+平均回帰+たまの暴落で、指数っぽい波を作る。

    実データの代わりにはならない。エンジンが正しく動くかの確認と、
    ルールの手触りを掴むためだけのもの。
    """
    rng = random.Random(args.seed)
    days = int(args.years * 252)
    drift = args.drift / 252.0
    vol = args.vol / math.sqrt(252.0)

    trend = math.log(args.start_price)
    gap = 0.0          # トレンドからの乖離(平均回帰する成分)
    phi = 0.97         # 乖離が戻る速さ
    shock_left = 0
    prev_close = args.start_price
    day = Date(2014, 1, 6)

    rows = []
    while len(rows) < days:
        if day.weekday() >= 5:
            day += timedelta(days=1)
            continue
        regime = 3.0 if shock_left > 0 else 1.0
        if shock_left > 0:
            shock_left -= 1
        elif rng.random() < 1.0 / 900.0:      # 数年に一度の暴落
            shock_left = 60
            gap -= rng.uniform(0.10, 0.22)

        trend += drift
        gap = gap * phi + rng.gauss(0.0, vol * regime * 0.6)
        close = math.exp(trend + gap)

        open_ = prev_close * math.exp(rng.gauss(0.0, vol * 0.3))
        span = abs(rng.gauss(0.0, vol * 0.5)) * close
        high = max(open_, close) + span
        low = min(open_, close) - span
        rows.append([day.isoformat(), round(open_, 1), round(high, 1),
                     round(low, 1), round(close, 1)])
        prev_close = close
        day += timedelta(days=1)

    with open(args.out, "w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["Date", "Open", "High", "Low", "Close"])
        writer.writerows(rows)
    print("合成データ %d本: %s (%s 〜 %s, 終値 %.1f → %.1f)"
          % (len(rows), args.out, rows[0][0], rows[-1][0],
             rows[0][4], rows[-1][4]))
    return 0


def _add_strategy_args(parser):
    parser.add_argument("--levels", help="買い下がりの段。例 -3,-5,-7,-10,-13")
    parser.add_argument("--unit", type=float, help="1段あたりの金額(円)")
    parser.add_argument("--lot", type=int, help="売買単位(1306は10、1321は1)")
    parser.add_argument("--ma", type=int, help="ものさしの移動平均日数(既定25)")
    parser.add_argument("--cooldown", type=int, help="建玉の最低間隔(営業日)")
    parser.add_argument("--tp", help="売り上がり。例 3:0.333,6:0.5")
    parser.add_argument("--exit-dev", type=float, help="全利食いの乖離率")
    parser.add_argument("--stop", type=float, help="撤退の水準(%%)")
    parser.add_argument("--no-stop", action="store_true", help="撤退ルールを使わない")
    parser.add_argument("--exec-at", choices=("next_open", "close"),
                        help="執行価格(既定は翌日始値)")
    parser.add_argument("--fee", type=float, help="1回あたり手数料(円)")
    parser.add_argument("--range-window", type=int,
                        help="52週レンジの営業日数(既定252)")
    parser.add_argument("--low-gate", type=float,
                        help="レンジ内位置がこの%%以下なら買わない(例 20)")
    parser.add_argument("--block-after-new-low", type=int,
                        help="52週安値更新からこの営業日数は買わない(例 20)")
    parser.add_argument("--high-trail", type=float,
                        help="レンジ内位置がこの%%以上なら刻まず引っ張る(例 90)")
    parser.add_argument("--trail-pct", type=float,
                        help="引っ張るときの高値からの許容下落幅(既定5.0)")
    parser.add_argument("--raw-close", action="store_true",
                        help="調整後終値ではなく素の終値を使う")


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="ETFうねり取りのバックテストと日次シグナル",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    bt = sub.add_parser("backtest", help="ルールを過去データで回す")
    bt.add_argument("--csv", required=True)
    bt.add_argument("--trades", type=int, default=0, help="直近N件の売買を表示")
    bt.add_argument("--out-trades", help="玉帳CSVの出力先")
    bt.add_argument("--out-equity", help="エクイティカーブCSVの出力先")
    _add_strategy_args(bt)
    bt.set_defaults(func=cmd_backtest)

    sw = sub.add_parser("sweep", help="段の設計を総当たりで比べる")
    sw.add_argument("--csv", required=True)
    sw.add_argument("--first", default="-2,-3,-4,-5", help="1段目の候補")
    sw.add_argument("--spacing", default="1.5,2,2.5,3", help="段の間隔の候補")
    sw.add_argument("--tp1", default="2,3,4,5", help="利食い1段目の候補")
    sw.add_argument("--units", type=int, default=5, help="段数")
    sw.add_argument("--top", type=int, default=15)
    _add_strategy_args(sw)
    sw.set_defaults(func=cmd_sweep)

    cp = sub.add_parser("compare", help="52週フィルタの有無を並べて比べる")
    cp.add_argument("--csv", required=True)
    cp.add_argument("--low-gate-at", type=float, default=20.0,
                    help="安値ゲートの閾値(既定20%%)")
    cp.add_argument("--high-trail-at", type=float, default=90.0,
                    help="引っ張りに切り替える閾値(既定90%%)")
    cp.add_argument("--trail", type=float, default=5.0,
                    help="引っ張るときの許容下落幅(既定5%%)")
    cp.add_argument("--block-days", type=int, default=20,
                    help="新安値更新後に買わない日数(既定20)")
    _add_strategy_args(cp)
    cp.set_defaults(func=cmd_compare)

    sg = sub.add_parser("signal", help="今日の位置とルールの判定")
    sg.add_argument("--csv", required=True)
    sg.add_argument("--units", type=int, default=0, help="今の建玉段数")
    sg.add_argument("--avg-cost", type=float, help="今の平均建値")
    _add_strategy_args(sg)
    sg.set_defaults(func=cmd_signal)

    ft = sub.add_parser("fetch", help="日足CSVを取得する(要ネットワーク)")
    ft.add_argument("--ticker", default="1306.T")
    ft.add_argument("--range", default="15y")
    ft.add_argument("--out", required=True)
    ft.set_defaults(func=cmd_fetch)

    sy = sub.add_parser("synth", help="検証用の合成日足を作る")
    sy.add_argument("--out", required=True)
    sy.add_argument("--years", type=float, default=12.0)
    sy.add_argument("--seed", type=int, default=42)
    sy.add_argument("--drift", type=float, default=0.05, help="年率ドリフト")
    sy.add_argument("--vol", type=float, default=0.18, help="年率ボラティリティ")
    sy.add_argument("--start-price", type=float, default=2000.0)
    sy.set_defaults(func=cmd_synth)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
