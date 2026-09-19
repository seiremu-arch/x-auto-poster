#!/usr/bin/env python3
"""うねり取りエンジンの検証。ネットワークは使わない。

    python -m unittest discover -s tools/uneri/tests -v
"""

import contextlib
import io
import os
import random
import sys
import tempfile
import unittest
from dataclasses import replace

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import uneri  # noqa: E402


def bars_from_closes(closes, start_day=1):
    """終値の列からバーを作る。始値=前日終値(ギャップなし)として扱う。"""
    bars = []
    for i, close in enumerate(closes):
        day = "2020-%02d-%02d" % (1 + (start_day + i) // 28, 1 + (start_day + i) % 28)
        open_ = closes[i - 1] if i else close
        bars.append(uneri.Bar(day, open_, max(open_, close), min(open_, close), close))
    return bars


def flat_then(level, n, tail):
    """n日フラットで移動平均を作ってから、tailの値動きを繋ぐ。"""
    return [level] * n + list(tail)


def sustained_decline(days, rate=0.975, level=100.0, flat=10):
    """毎日一定率で下げ続ける系列。

    段が埋まるのは「急落一発」ではなく「下げが続くとき」だけ。移動平均は下げを
    追いかけて数日で追いつくので、一度下げて横ばいになると乖離はすぐ0に戻る。
    段数を深く取るほど、この性質が効いてくる。
    """
    return [level] * flat + [level * (rate ** i) for i in range(1, days + 1)]


class TestIndicators(unittest.TestCase):
    def test_sma_warmup_and_value(self):
        values = [1, 2, 3, 4, 5]
        got = uneri.sma(values, 3)
        self.assertEqual(got[:2], [None, None])
        self.assertAlmostEqual(got[2], 2.0)
        self.assertAlmostEqual(got[4], 4.0)

    def test_sma_window_one_is_identity(self):
        self.assertEqual(uneri.sma([3.0, 1.0, 2.0], 1), [3.0, 1.0, 2.0])

    def test_deviation(self):
        self.assertAlmostEqual(uneri.deviation_pct(97.0, 100.0), -3.0)
        self.assertIsNone(uneri.deviation_pct(97.0, None))

    def test_floor_lot(self):
        self.assertEqual(uneri._floor_lot(123, 10), 120)
        self.assertEqual(uneri._floor_lot(9, 10), 0)
        self.assertEqual(uneri._floor_lot(123, 1), 123)


class TestCsv(unittest.TestCase):
    def _write(self, text, encoding="utf-8"):
        fh = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False,
                                         encoding=encoding, newline="")
        fh.write(text)
        fh.close()
        self.addCleanup(os.unlink, fh.name)
        return fh.name

    def test_japanese_headers_and_cp932(self):
        path = self._write(
            "日付,始値,高値,安値,終値,出来高\n"
            "2026/09/17,\"2,800.0\",2830,2790,2810,1000\n"
            "2026/09/18,2810,2850,2800,2840,900\n",
            encoding="cp932",
        )
        bars = uneri.load_csv(path)
        self.assertEqual(len(bars), 2)
        self.assertEqual(bars[0].date, "2026-09-17")
        self.assertAlmostEqual(bars[0].open, 2800.0)   # カンマ区切りが読めている
        self.assertAlmostEqual(bars[1].close, 2840.0)

    def test_adjusted_close_preferred(self):
        path = self._write("Date,Close,Adj Close\n2026-01-05,100,90\n2026-01-06,101,91\n")
        self.assertAlmostEqual(uneri.load_csv(path)[0].close, 90.0)
        self.assertAlmostEqual(uneri.load_csv(path, use_adjusted=False)[0].close, 100.0)

    def test_close_only_csv_uses_close_as_open(self):
        path = self._write("Date,Close\n2026-01-06,100\n2026-01-07,110\n")
        bars = uneri.load_csv(path)
        self.assertAlmostEqual(bars[1].open, bars[1].close)

    def test_sorted_and_deduped(self):
        path = self._write("Date,Close\n2026-01-07,110\n2026-01-06,100\n2026-01-07,111\n")
        bars = uneri.load_csv(path)
        self.assertEqual([b.date for b in bars], ["2026-01-06", "2026-01-07"])
        self.assertAlmostEqual(bars[-1].close, 111.0)

    def test_missing_close_column_raises(self):
        path = self._write("Date,Volume\n2026-01-06,100\n")
        with self.assertRaises(SystemExit):
            uneri.load_csv(path)


class TestLadder(unittest.TestCase):
    """買い下がりの段が、順番に・1日1段だけ・上限までしか出ないこと。"""

    def setUp(self):
        self.p = Params = replace(
            uneri.Params(),
            ma_short=5,
            ma_long=5,
            buy_levels=(-3.0, -5.0, -7.0),
            unit_yen=100_000.0,
            lot_size=1,
            cooldown_days=3,
            exec_at="close",
            tax_rate=0.0,
            exit_on_ma_long=False,
            stop_loss_pct=None,
        )

    def _run(self, closes):
        return uneri.Backtest(bars_from_closes(closes), self.p).run()

    def test_first_level_fires_once(self):
        # 100で平らにしてから96(-4%)へ。1段目だけが出る。
        res = self._run(flat_then(100.0, 10, [96.0] * 3))
        buys = [t for t in res.trades if t.side == "BUY"]
        self.assertEqual(len(buys), 1)
        self.assertIn("買い1段", buys[0].reason)

    def test_cooldown_blocks_consecutive_days(self):
        # 一気に-15%まで落ちても、その日に建つのは1段だけ。
        res = self._run(flat_then(100.0, 10, [85.0] * 2))
        self.assertEqual(len([t for t in res.trades if t.side == "BUY"]), 1)

    def test_cooldown_spaces_out_the_ladder(self):
        self.p = replace(self.p, buy_levels=(-1.0, -2.0, -3.0))
        res = self._run(sustained_decline(20))
        buys = [t for t in res.trades if t.side == "BUY"]
        self.assertEqual(len(buys), 3)
        days = [uneri._daydiff(buys[0].date, b.date) for b in buys]
        for before, after in zip(days, days[1:]):
            self.assertGreaterEqual(after - before, self.p.cooldown_days)

    def test_ladder_climbs_only_while_price_keeps_falling(self):
        self.p = replace(self.p, buy_levels=(-1.0, -2.0, -3.0))
        res = self._run(sustained_decline(20))
        buys = [t for t in res.trades if t.side == "BUY"]
        self.assertEqual([b.reason[:4] for b in buys], ["買い1段", "買い2段", "買い3段"])

    def test_one_shot_crash_does_not_fill_the_ladder(self):
        """一度落ちて横ばいだと、移動平均が追いついて乖離が消え、段は埋まらない。

        これは仕様。うねり取りの段は「下げが続く」ことに対する備えであって、
        「一発の急落」に対する備えではない。
        """
        res = self._run(flat_then(100.0, 10, [40.0] * 200))
        buys = [t for t in res.trades if t.side == "BUY"]
        self.assertLess(len(buys), 3)
        self.assertGreaterEqual(len(buys), 1)

    def test_never_exceeds_max_units(self):
        # 下げが何年続いても、段数(=3)を超えて買わない。これが破産しない理由。
        self.p = replace(self.p, buy_levels=(-1.0, -2.0, -3.0))
        res = self._run(sustained_decline(200))
        self.assertEqual(len([t for t in res.trades if t.side == "BUY"]), 3)

    def test_levels_are_sequential_not_absolute(self):
        # -4%で1段建てたあと、-4%のままでは2段目(-5%)は出ない。
        res = self._run(flat_then(100.0, 10, [96.0] * 30))
        self.assertEqual(len([t for t in res.trades if t.side == "BUY"]), 1)


class TestExits(unittest.TestCase):
    def setUp(self):
        self.p = replace(
            uneri.Params(),
            ma_short=5,
            ma_long=5,
            buy_levels=(-3.0, -5.0, -7.0),
            unit_yen=100_000.0,
            lot_size=1,
            cooldown_days=1,
            take_profit=((3.0, 1.0 / 3.0), (6.0, 0.5)),
            exit_deviation=100.0,      # 乖離での全利食いは無効化して段だけ見る
            exit_on_ma_long=False,
            stop_loss_pct=None,
            exec_at="close",
            tax_rate=0.0,
        )

    def _run(self, closes, params=None):
        return uneri.Backtest(bars_from_closes(closes), params or self.p).run()

    def test_partial_take_profit_sizing(self):
        # 1段(1000株相当)建てて+4%。建玉の1/3を落とす。
        res = self._run(flat_then(100.0, 10, [96.0, 96.0, 104.0, 104.0]))
        sells = [t for t in res.trades if t.side == "SELL"]
        self.assertTrue(sells)
        buy = [t for t in res.trades if t.side == "BUY"][0]
        self.assertEqual(sells[0].shares, uneri._floor_lot(buy.shares / 3.0, 1))
        self.assertIn("利食い1段", sells[0].reason)

    def test_take_profit_stages_are_ordered_and_once(self):
        res = self._run(flat_then(100.0, 10, [96.0, 96.0, 104.0, 104.0, 110.0, 110.0]))
        reasons = [t.reason[:5] for t in res.trades if t.side == "SELL"]
        self.assertEqual(reasons[:2], ["利食い1段", "利食い2段"])
        self.assertEqual(reasons.count("利食い1段"), 1)

    def test_full_exit_on_deviation(self):
        p = replace(self.p, exit_deviation=4.0)
        res = self._run(flat_then(100.0, 10, [96.0, 96.0, 130.0, 130.0]), p)
        self.assertTrue(res.trades[-1].reason.startswith("全利食い"))
        self.assertEqual(sum(t.shares for t in res.trades if t.side == "SELL"),
                         sum(t.shares for t in res.trades if t.side == "BUY"))

    def test_stop_loss_only_at_full_position_and_once(self):
        p = replace(self.p, stop_loss_pct=-18.0, stop_loss_fraction=0.5,
                    buy_levels=(-1.0, -2.0, -3.0))
        # 3段建て切ってから、さらに下げ続ける。
        res = self._run(sustained_decline(8) + [60.0] * 40, p)
        stops = [t for t in res.trades if "撤退" in t.reason]
        self.assertEqual(len(stops), 1, "撤退は1サイクル1回だけ")
        self.assertEqual(res.stop_count, 1)

    def test_no_stop_when_disabled(self):
        p = replace(self.p, buy_levels=(-1.0, -2.0, -3.0))
        res = self._run(sustained_decline(8) + [60.0] * 40, p)
        self.assertEqual(res.stop_count, 0)

    def test_stop_needs_full_position(self):
        # 1段しか建っていない状態では、どれだけ下げても撤退は出ない。
        p = replace(self.p, stop_loss_pct=-18.0, buy_levels=(-3.0, -50.0, -60.0))
        res = self._run(flat_then(100.0, 10, [96.0] + [70.0] * 30), p)
        self.assertEqual(res.stop_count, 0)


class TestAccounting(unittest.TestCase):
    def setUp(self):
        self.p = replace(
            uneri.Params(),
            ma_short=5,
            ma_long=5,
            buy_levels=(-3.0, -6.0),
            unit_yen=100_000.0,
            lot_size=1,
            cooldown_days=1,
            exit_deviation=4.0,
            exit_on_ma_long=False,
            stop_loss_pct=None,
            exec_at="close",
        )

    def test_average_cost_basis(self):
        p = replace(self.p, tax_rate=0.0)
        res = uneri.Backtest(
            bars_from_closes(flat_then(100.0, 10, [96.0, 88.0, 88.0])), p
        ).run()
        buys = [t for t in res.trades if t.side == "BUY"]
        self.assertEqual(len(buys), 2)
        total_cost = sum(t.price * t.shares for t in buys)
        total_shares = sum(t.shares for t in buys)
        self.assertAlmostEqual(buys[-1].avg_cost, total_cost / total_shares, places=6)

    def test_equity_is_cash_plus_position(self):
        """最終資産 = 元本 + 実現損益 - 納税額。帳尻が合うことを確認する。"""
        p = replace(self.p, tax_rate=0.20315)
        res = uneri.Backtest(
            bars_from_closes(flat_then(100.0, 10, [96.0] * 3 + [130.0] * 3)), p
        ).run()
        self.assertAlmostEqual(
            res.final_equity, p.capital + res.realized - res.tax_paid, places=4
        )

    def test_loss_carryforward_offsets_later_gain(self):
        """損を出したあとの利益は、繰越損失と相殺されてから課税される。"""
        p = replace(
            self.p, buy_levels=(-1.0, -2.0, -3.0), cooldown_days=3,
            stop_loss_pct=-18.0, stop_loss_fraction=0.5, tax_rate=0.20315,
        )
        bottom = 100.0 * (0.975 ** 15)
        closes = sustained_decline(15) + [bottom * 0.75] * 6 + [bottom * 1.6] * 6
        res = uneri.Backtest(bars_from_closes(closes), p).run()

        self.assertEqual(res.stop_count, 1, "撤退で損が確定している前提")
        gross_gain = sum(t.realized for t in res.trades if t.realized > 0)
        gross_loss = -sum(t.realized for t in res.trades if t.realized < 0)
        self.assertGreater(gross_gain, 0)
        self.assertGreater(gross_loss, 0)
        # 税は「利益 - 繰越損失」に対してかかる。素の利益に対する税より必ず安い。
        self.assertAlmostEqual(res.tax_paid, (gross_gain - gross_loss) * 0.20315,
                               places=4)
        self.assertLess(res.tax_paid, gross_gain * 0.20315)

    def test_no_tax_when_net_loss(self):
        closes = flat_then(100.0, 10, [96.0] * 3 + [60.0] * 20)
        res = uneri.Backtest(
            bars_from_closes(closes), replace(self.p, tax_rate=0.20315)
        ).run()
        self.assertLess(res.realized, 0)
        self.assertAlmostEqual(res.tax_paid, 0.0)

    def test_position_is_forced_closed_at_end(self):
        """終端で含み玉を残さない。残すと成績が実態より良く見えるため。"""
        closes = flat_then(100.0, 10, [96.0] * 5)
        res = uneri.Backtest(bars_from_closes(closes), self.p).run()
        self.assertTrue(res.trades)
        self.assertEqual(res.trades[-1].side, "SELL")
        self.assertIn("強制決済", res.trades[-1].reason)
        self.assertTrue(res.cycles[-1].forced)

    def test_one_cycle_never_spends_more_than_capital(self):
        """1サイクルで投じる額は上限を超えない。資金は決済のたびに戻って再利用される。"""
        p = replace(
            self.p, buy_levels=(-1.0, -2.0, -3.0, -4.0, -4.5),
            cooldown_days=3, tax_rate=0.0, exit_deviation=4.0,
        )
        closes = sustained_decline(40) + [100.0 * (0.975 ** 40) * 1.5] * 20
        res = uneri.Backtest(bars_from_closes(closes), p).run()

        spent = 0.0
        held = 0
        for trade in res.trades:
            if trade.side == "BUY":
                spent += trade.amount
                held += trade.shares
                self.assertLessEqual(spent, p.capital + 1e-6)
            else:
                held -= trade.shares
                if held == 0:
                    spent = 0.0
        self.assertTrue(all(value >= -1e-6 for _, value in res.equity))


class TestExecution(unittest.TestCase):
    def test_next_open_uses_following_bar_open(self):
        p = replace(
            uneri.Params(), ma_short=5, ma_long=5, buy_levels=(-3.0,),
            unit_yen=100_000.0, lot_size=1, exec_at="next_open",
            exit_on_ma_long=False, stop_loss_pct=None, tax_rate=0.0,
        )
        closes = flat_then(100.0, 10, [96.0, 96.0, 96.0])
        bars = bars_from_closes(closes)
        res = uneri.Backtest(bars, p).run()
        buy = [t for t in res.trades if t.side == "BUY"][0]
        signal_index = [b.date for b in bars].index(buy.date) - 1
        self.assertAlmostEqual(buy.price, bars[signal_index + 1].open)

    def test_close_execution_uses_signal_bar_close(self):
        p = replace(
            uneri.Params(), ma_short=5, ma_long=5, buy_levels=(-3.0,),
            unit_yen=100_000.0, lot_size=1, exec_at="close",
            exit_on_ma_long=False, stop_loss_pct=None, tax_rate=0.0,
        )
        res = uneri.Backtest(bars_from_closes(flat_then(100.0, 10, [96.0] * 3)), p).run()
        self.assertAlmostEqual([t for t in res.trades if t.side == "BUY"][0].price, 96.0)

    def test_lot_size_is_respected(self):
        p = replace(
            uneri.Params(), ma_short=5, ma_long=5, buy_levels=(-3.0,),
            unit_yen=100_000.0, lot_size=10, exec_at="close",
            exit_on_ma_long=False, stop_loss_pct=None, tax_rate=0.0,
        )
        res = uneri.Backtest(bars_from_closes(flat_then(100.0, 10, [96.0] * 3)), p).run()
        for trade in res.trades:
            self.assertEqual(trade.shares % 10, 0)


class TestNoTradeCases(unittest.TestCase):
    def test_rising_market_never_buys(self):
        """一方通行の上げでは乖離が-3%に届かず、1回も買えない。うねり取りの弱点。"""
        p = replace(uneri.Params(), ma_short=5, ma_long=5, exec_at="close")
        closes = [100.0 * (1.004 ** i) for i in range(200)]
        res = uneri.Backtest(bars_from_closes(closes), p).run()
        self.assertEqual(res.trades, [])
        self.assertAlmostEqual(res.final_equity, p.capital)
        self.assertLess(res.final_equity, res.buyhold_final_after_tax,
                        "上げ相場ではバイ&ホールドに負ける")

    def test_report_renders_without_cycles(self):
        p = replace(uneri.Params(), ma_short=5, ma_long=5, exec_at="close")
        closes = [100.0 * (1.004 ** i) for i in range(200)]
        res = uneri.Backtest(bars_from_closes(closes), p).run()
        text = uneri.format_report(res)
        self.assertIn("1サイクルも成立しなかった", text)


class TestMetrics(unittest.TestCase):
    def test_max_drawdown(self):
        equity = [("d1", 100.0), ("d2", 120.0), ("d3", 60.0), ("d4", 90.0)]
        rate, amount = uneri.max_drawdown(equity)
        self.assertAlmostEqual(rate, 0.5)
        self.assertAlmostEqual(amount, 60.0)

    def test_max_drawdown_monotonic_is_zero(self):
        rate, amount = uneri.max_drawdown([("d1", 1.0), ("d2", 2.0), ("d3", 3.0)])
        self.assertAlmostEqual(rate, 0.0)
        self.assertAlmostEqual(amount, 0.0)

    def test_daydiff(self):
        self.assertEqual(uneri._daydiff("2026-01-01", "2026-12-31"), 364)


class TestRollingExtreme(unittest.TestCase):
    def test_max_and_min(self):
        values = [3.0, 1.0, 4.0, 1.0, 5.0, 9.0, 2.0]
        self.assertEqual(uneri.rolling_extreme(values, 3, "max"),
                         [None, None, 4.0, 4.0, 5.0, 9.0, 9.0])
        self.assertEqual(uneri.rolling_extreme(values, 3, "min"),
                         [None, None, 1.0, 1.0, 1.0, 1.0, 2.0])

    def test_matches_naive_on_random_data(self):
        """単調デックの実装が素朴なmin/maxと一致すること。"""
        rng = random.Random(1234)
        values = [rng.uniform(1.0, 100.0) for _ in range(400)]
        for window in (2, 7, 60, 252):
            fast_max = uneri.rolling_extreme(values, window, "max")
            fast_min = uneri.rolling_extreme(values, window, "min")
            for i in range(len(values)):
                if i < window - 1:
                    self.assertIsNone(fast_max[i])
                    self.assertIsNone(fast_min[i])
                else:
                    chunk = values[i - window + 1:i + 1]
                    self.assertAlmostEqual(fast_max[i], max(chunk))
                    self.assertAlmostEqual(fast_min[i], min(chunk))

    def test_window_larger_than_data(self):
        self.assertEqual(uneri.rolling_extreme([1.0, 2.0], 5, "max"), [None, None])


class TestRangePosition(unittest.TestCase):
    def test_endpoints_and_middle(self):
        self.assertAlmostEqual(uneri.range_position(100.0, 100.0, 50.0), 100.0)
        self.assertAlmostEqual(uneri.range_position(50.0, 100.0, 50.0), 0.0)
        self.assertAlmostEqual(uneri.range_position(75.0, 100.0, 50.0), 50.0)

    def test_flat_range_is_neutral(self):
        self.assertAlmostEqual(uneri.range_position(10.0, 10.0, 10.0), 50.0)

    def test_none_when_window_not_filled(self):
        self.assertIsNone(uneri.range_position(10.0, None, 5.0))
        self.assertIsNone(uneri.range_position(10.0, 15.0, None))


class TestLowGate(unittest.TestCase):
    """52週安値圏では買い下がりを止める。"""

    def setUp(self):
        self.p = replace(
            uneri.Params(), ma_short=5, ma_long=5, range_window=20,
            buy_levels=(-1.0, -2.0, -3.0), unit_yen=100_000.0, lot_size=1,
            cooldown_days=3, exec_at="close", tax_rate=0.0,
            exit_on_ma_long=False, stop_loss_pct=None, exit_deviation=100.0,
        )

    def _buys(self, params, closes):
        res = uneri.Backtest(bars_from_closes(closes), params).run()
        return [t for t in res.trades if t.side == "BUY"], res

    def test_gate_blocks_buying_into_new_lows(self):
        closes = sustained_decline(30, flat=30)
        plain, _ = self._buys(self.p, closes)
        gated, res = self._buys(replace(self.p, low_gate=20.0), closes)
        self.assertGreater(len(plain), 0)
        self.assertEqual(len(gated), 0, "安値更新中は1段も建てない")
        self.assertGreater(res.blocked_by_low_gate, 0)

    def test_gate_allows_buying_high_in_the_range(self):
        # 高値圏まで上げたあとの押し目なら、レンジ内位置は高いので買える。
        closes = [100.0] * 30 + [100.0 + i for i in range(30)] + [124.0] * 3
        gated, _ = self._buys(replace(self.p, low_gate=20.0), closes)
        self.assertGreater(len(gated), 0)

    def test_block_after_new_low(self):
        closes = sustained_decline(30, flat=30)
        blocked, res = self._buys(replace(self.p, block_after_new_low=10), closes)
        self.assertEqual(len(blocked), 0)
        self.assertGreater(res.blocked_by_low_gate, 0)

    def test_filters_are_inactive_during_warmup(self):
        """52週の窓が埋まるまでは判定できないので、素のうねり取りとして動く。"""
        p = replace(self.p, range_window=500, low_gate=20.0)
        closes = sustained_decline(30, flat=30)
        buys, res = self._buys(p, closes)
        self.assertGreater(len(buys), 0)
        self.assertEqual(res.blocked_by_low_gate, 0)

    def test_gate_reduces_capital_deployed(self):
        """ゲートは資金の遊びを増やす。これは相場付きによらない構造的なコスト。"""
        closes = sustained_decline(30, flat=30) + [50.0] * 40
        plain = uneri.Backtest(bars_from_closes(closes), self.p).run()
        gated = uneri.Backtest(
            bars_from_closes(closes), replace(self.p, low_gate=20.0)
        ).run()
        self.assertLess(gated.mean_exposure, plain.mean_exposure)


class TestHighTrail(unittest.TestCase):
    """52週高値圏では刻まずに引っ張る。"""

    def setUp(self):
        self.p = replace(
            uneri.Params(), ma_short=5, ma_long=5, range_window=20,
            buy_levels=(-3.0,), unit_yen=100_000.0, lot_size=1,
            cooldown_days=3, exec_at="close", tax_rate=0.0,
            exit_on_ma_long=False, stop_loss_pct=None, exit_deviation=4.0,
            take_profit=((3.0, 1.0 / 3.0), (6.0, 0.5)),
        )
        # 30日フラット → 押し目で建玉 → 52週高値を更新しながら上昇
        self.rally = [100.0] * 30 + [96.0] * 2 + [104.0, 112.0, 120.0, 128.0]

    def test_trailing_suppresses_the_staged_take_profit(self):
        plain = uneri.Backtest(bars_from_closes(self.rally), self.p).run()
        trailed = uneri.Backtest(
            bars_from_closes(self.rally), replace(self.p, high_trail=90.0)
        ).run()
        self.assertGreater(len([t for t in plain.trades if "利食い" in t.reason]), 0)
        self.assertEqual(trailed.trail_engaged, 1)
        self.assertEqual(
            len([t for t in trailed.trades if "利食い" in t.reason]), 0,
            "高値圏では刻まない",
        )

    def test_trailing_exits_on_the_pullback(self):
        closes = self.rally + [128.0 * 0.90] * 3
        res = uneri.Backtest(
            bars_from_closes(closes), replace(self.p, high_trail=90.0, trail_pct=5.0)
        ).run()
        exits = [t for t in res.trades if "引っ張り" in t.reason]
        self.assertEqual(len(exits), 1)
        self.assertEqual(res.trail_exits, 1)
        self.assertEqual(exits[0].shares,
                         sum(t.shares for t in res.trades if t.side == "BUY"))

    def test_trailing_needs_both_profit_and_high_range(self):
        # 高値圏でも含み益が利食い水準に届かなければ引っ張りには入らない。
        p = replace(self.p, high_trail=90.0, take_profit=((50.0, 1.0),))
        res = uneri.Backtest(bars_from_closes(self.rally), p).run()
        self.assertEqual(res.trail_engaged, 0)

    def test_trailing_does_not_disable_the_stop(self):
        """引っ張りは含み益のある場面だけ。撤退ルールとは干渉しない。"""
        p = replace(
            self.p, high_trail=90.0, buy_levels=(-1.0, -2.0, -3.0),
            stop_loss_pct=-18.0, stop_loss_fraction=0.5, exit_deviation=100.0,
        )
        closes = sustained_decline(10, flat=30) + [55.0] * 40
        res = uneri.Backtest(bars_from_closes(closes), p).run()
        self.assertEqual(res.stop_count, 1)
        self.assertEqual(res.trail_engaged, 0)


class TestDefaultsUnchanged(unittest.TestCase):
    def test_52week_features_are_off_by_default(self):
        p = uneri.Params()
        self.assertIsNone(p.low_gate)
        self.assertIsNone(p.high_trail)
        self.assertEqual(p.block_after_new_low, 0)

    def test_default_run_ignores_the_range_entirely(self):
        """既定値では52週は結果に一切影響しない(素のうねり取りと同一)。"""
        closes = sustained_decline(40, flat=30) + [80.0] * 40
        base = replace(uneri.Params(), ma_short=5, ma_long=5, lot_size=1,
                       exec_at="close")
        wide = uneri.Backtest(bars_from_closes(closes),
                              replace(base, range_window=10)).run()
        narrow = uneri.Backtest(bars_from_closes(closes),
                                replace(base, range_window=999)).run()
        self.assertAlmostEqual(wide.final_equity, narrow.final_equity, places=6)
        self.assertEqual(len(wide.trades), len(narrow.trades))


class TestEndToEnd(unittest.TestCase):
    def test_synth_then_backtest(self):
        out = tempfile.NamedTemporaryFile(suffix=".csv", delete=False)
        out.close()
        self.addCleanup(os.unlink, out.name)
        with contextlib.redirect_stdout(io.StringIO()):
            rc = uneri.main(["synth", "--out", out.name, "--years", "8", "--seed", "7"])
        self.assertEqual(rc, 0)

        bars = uneri.load_csv(out.name)
        self.assertGreater(len(bars), 1500)
        res = uneri.Backtest(bars, uneri.Params()).run()

        # 会計の恒等式が成り立っていること。
        self.assertAlmostEqual(
            res.final_equity,
            res.params.capital + res.realized - res.tax_paid,
            places=3,
        )
        # 買った口数と売った口数が一致すること(玉が消えたり湧いたりしない)。
        self.assertEqual(sum(t.shares for t in res.trades if t.side == "BUY"),
                         sum(t.shares for t in res.trades if t.side == "SELL"))
        self.assertLessEqual(res.max_units_hit, res.params.max_units)
        self.assertIn("うねり取り バックテスト", uneri.format_report(res))


if __name__ == "__main__":
    unittest.main(verbosity=2)
