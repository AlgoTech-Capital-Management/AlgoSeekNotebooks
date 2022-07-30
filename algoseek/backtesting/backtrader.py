"""
Backtrader classes for AlgoSeek Data
"""
import backtrader as bt
import backtrader.feeds as btfeeds
import backtrader.analyzers as btanalyzers
from backtrader.feed import DataBase
from backtrader import date2num
from backtrader import TimeFrame
import os
import pytz
from pytz import timezone
import json
import itertools
import pandas as pd


class AlgoStrategy():

    def __init__(self, strategy):
        self.cerebro = bt.Cerebro()
        strategy.init_broker(self.cerebro.broker)

        data = strategy.add_data(self.cerebro)

        strategy.data = data

        self.cerebro.addstrategy(strategy)

        self.portfolioStartValue = self.cerebro.broker.getvalue()
        self.cerebro.addanalyzer(bt.analyzers.DrawDown, _name='dd')
        self.cerebro.addanalyzer(bt.analyzers.SharpeRatio_A, _name='sharpe')
        self.cerebro.addanalyzer(bt.analyzers.SQN, _name='sqn')
        self.cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='ta')
        self.cerebro.addanalyzer(bt.analyzers.PyFolio, _name="pyfolio")

    def performance(self):
        analyzer = self.thestrat.analyzers.ta.get_analysis()
        dd_analyzer = self.thestrat.analyzers.dd.get_analysis()

        # Get the results we are interested in
        total_open = analyzer.total.open
        total_closed = analyzer.total.closed
        total_won = analyzer.won.total
        total_lost = analyzer.lost.total
        win_streak = analyzer.streak.won.longest
        lose_streak = analyzer.streak.lost.longest
        pnl_net = analyzer.pnl.net.total
        strike_rate = 0
        if total_closed > 0:
            strike_rate = (total_won / total_closed) * 100
        # Designate the rows
        h1 = ['Total Open', 'Total Closed', 'Total Won', 'Total Lost']
        h2 = ['Strike Rate', 'Win Streak', 'Losing Streak', 'PnL Net']
        h3 = ['DrawDown Pct', 'MoneyDown', '', '']
        self.total_closed = total_closed
        self.strike_rate = strike_rate
        self.max_drawdown = dd_analyzer.max.drawdown
        r1 = [total_open, total_closed, total_won, total_lost]
        r2 = [('%.2f%%' % (strike_rate)), win_streak, lose_streak, pnl_net]
        r3 = [('%.2f%%' % (dd_analyzer.max.drawdown)), dd_analyzer.max.moneydown, '', '']
        # Check which set of headers is the longest.
        # header_length = np.maximum(len(h1),len(h2),len(h3))
        # Print the rows
        print_list = [h1, r1, h2, r2, h3, r3]
        row_format = "{:<15}" * (200 + 1)
        print("Trade Analysis Results:")
        for row in print_list:
            # print(row_format.format('',*row))
            print(row)
        analyzer = self.thestrat.analyzers.sqn.get_analysis()
        sharpe_analyzer = self.thestrat.analyzers.sharpe.get_analysis()
        self.sqn = analyzer.sqn
        self.sharpe_ratio = sharpe_analyzer['sharperatio']
        if self.sharpe_ratio is None:
            self.sharpe_ratio = 0
        self.pnl = self.cerebro.broker.getvalue() - self.portfolioStartValue
        print('[SQN:%.2f, Sharpe Ratio:%.2f, Final Portfolio:%.2f, Total PnL:%.2f]' % (
        self.sqn, self.sharpe_ratio, self.cerebro.broker.getvalue(), self.pnl))

    def run(self):
        thestrats = self.cerebro.run()
        self.thestrat = thestrats[0]
        self.performance()


class MyFeed(DataBase):
    # TODO: Adjust a second verison of this class to use pandas rather than spark
    def __init__(self):
        super(MyFeed, self).__init__()
        # self.list=testData.select("start", "open", "high", "low", "close", "volume", "vwap", "exponential_moving_average").collect()
        # self.list = multiTick.select('datetime', "FirstTradePrice", 'HighTradePrice', 'LowTradePrice', 'LastTradePrice',                           'Volume', 'UptickVolume', 'DowntickVolume', 'RepeatUptickVolume','RepeatDowntickVolume').collect()
        self.list = taq_min.sort_index()
        self.n = 0

        self.fromdate = self.list[0]['BarDateTime']
        self.todate = self.list[len(self.list) - 1]['BarDateTime']
        self.timeframe = bt.TimeFrame.Minutes
        print("from=%s,to=%s" % (self.fromdate, self.todate))

        self.m = {}

        # print(self.list)

    def start(self):
        # Nothing to do for this data feed type
        pass

    def stop(self):
        # Nothing to do for this data feed type
        pass

    def _load(self):
        if self.n >= len(self.list):
            return False

        r = self.list[self.n]
        self.lines.datetime[0] = date2num(r['datetime'])

        self.lines.open[0] = r['FirstTradePrice']
        self.lines.high[0] = r['HighTradePrice']
        self.lines.low[0] = r['LowTradePrice']
        self.lines.close[0] = r['LastTradePrice']
        self.lines.volume[0] = r['Volume']
        self.m[r['datetime']] = r

        self.n = self.n + 1
        return True


class StrategyTemplate(bt.Strategy):

    def __init__(self):
        self.lastDay = -1
        self.lastMonth = -1
        self.dataclose = self.datas[0].close

    @staticmethod
    def init_broker(broker):
        pass

    @staticmethod
    def add_data(cerebro):
        pass

    def next(self):
        dt = self.datas[0].datetime.datetime(0)
        print("[NEXT]:%s:close=%s" % (dt, self.dataclose[0]))

        # SOM
        if self.lastMonth != dt.month:
            if self.lastMonth != -1:
                chg = self.broker.getvalue() - self.monthCash
                print("[%s] SOM:chg=%.2f,cash=%.2f" % (dt, chg, self.broker.getvalue()))
            self.lastMonth = dt.month
            self.monthCash = self.broker.getvalue()

        # SOD
        if self.lastDay != dt.day:
            self.lastDay = dt.day
            print("[%s] SOD:cash=%.2f" % (dt, self.broker.getvalue()))


class MyStrategy(StrategyTemplate):

    def __init__(self):  # Initiation
        super(MyStrategy, self).__init__()

    def init_broker(broker):
        broker.setcash(1000000.0)
        broker.setcommission(commission=0.0)

    def add_data(cerebro):
        data = MyFeed()

        cerebro.adddata(data)
        return data

    def next(self):  # Processing
        super(MyStrategy, self).next()
        dt = self.datas[0].datetime.datetime(0)
        r = self.data.m[dt]
        # print(r)
        size = self.cerebro.strat_params['size']
        threshold_PctChg = self.cerebro.strat_params['pct_chg']

        # model=self.cerebro.strat_params['model']
        df = spark.createDataFrame([r])
        # VWAP=r['vwap']
        # predictedVWAP = model.transform(df).collect()[0]['prediction']
        # expectedPctChg=(predictedVWAP-VWAP)/VWAP*100.0
        # print(self.data[0])

        # goLong=self.datas[0].close>self.datas[0].open
        # goShort=self.datas[0].close< self.datas[0].open
        goLong = r['UptickVolume'] < r['DowntickVolume']
        goShort = r['UptickVolume'] > r['DowntickVolume']
        # print("expectedPctChg=%s,goLong=%s,goShort=%s" % (expectedPctChg,goLong,goShort))

        if not self.position:
            if goLong:
                print("%s:%s x BUY @ %.2f" % (dt, size, r['LastTradePrice']))
                self.buy(size=size)  # Go long
            else:
                print("%s:%s x SELL @ %.2f" % (dt, size, r['LastTradePrice']))
                self.sell(size=size)  # Go short
        elif self.position.size > 0 and goShort:
            print("%s:%s x SELL @ %.2f" % (dt, size * 2, r['LastTradePrice']))
            self.sell(size=size * 2)
        elif self.position.size < 0 and goLong:
            print("%s:%s x BUY @ %.2f" % (dt, size * 2, r['LastTradePrice']))
            self.buy(size=size * 2)


class MultiAlgoStrategy():

    def __init__(self, strategy):
        self.cerebro = bt.Cerebro()
        strategy.init_broker(self.cerebro.broker)

        data = strategy.add_data(self.cerebro, tick="MSFT")

        strategy.data = data

        self.cerebro.addstrategy(strategy)

        self.portfolioStartValue = self.cerebro.broker.getvalue()

        self.smaFast = bt.ind.SimpleMovingAverage(period=50)
        self.smaSlow = bt.ind.SimpleMovingAverage(period=200)

        self.cerebro.addanalyzer(bt.analyzers.DrawDown, _name='dd')
        self.cerebro.addanalyzer(bt.analyzers.SharpeRatio_A, _name='sharpe')
        self.cerebro.addanalyzer(bt.analyzers.SQN, _name='sqn')
        self.cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='ta')
        self.cerebro.addanalyzer(bt.analyzers.PyFolio, _name="pyfolio")

    def performance(self):
        analyzer = self.thestrat.analyzers.ta.get_analysis()
        dd_analyzer = self.thestrat.analyzers.dd.get_analysis()

        # Get the results we are interested in
        total_open = analyzer.total.open
        total_closed = analyzer.total.closed
        total_won = analyzer.won.total
        total_lost = analyzer.lost.total
        win_streak = analyzer.streak.won.longest
        lose_streak = analyzer.streak.lost.longest
        pnl_net = analyzer.pnl.net.total
        strike_rate = 0
        if total_closed > 0:
            strike_rate = (total_won / total_closed) * 100
        # Designate the rows
        h1 = ['Total Open', 'Total Closed', 'Total Won', 'Total Lost']
        h2 = ['Strike Rate', 'Win Streak', 'Losing Streak', 'PnL Net']
        h3 = ['DrawDown Pct', 'MoneyDown', '', '']
        self.total_closed = total_closed
        self.strike_rate = strike_rate
        self.max_drawdown = dd_analyzer.max.drawdown
        r1 = [total_open, total_closed, total_won, total_lost]
        r2 = [('%.2f%%' % (strike_rate)), win_streak, lose_streak, pnl_net]
        r3 = [('%.2f%%' % (dd_analyzer.max.drawdown)), dd_analyzer.max.moneydown, '', '']
        # Check which set of headers is the longest.
        # header_length = np.maximum(len(h1),len(h2),len(h3))
        # Print the rows
        print_list = [h1, r1, h2, r2, h3, r3]
        row_format = "{:<15}" * (200 + 1)
        print("Trade Analysis Results:")
        for row in print_list:
            # print(row_format.format('',*row))
            print(row)
        analyzer = self.thestrat.analyzers.sqn.get_analysis()
        sharpe_analyzer = self.thestrat.analyzers.sharpe.get_analysis()
        self.sqn = analyzer.sqn
        self.sharpe_ratio = sharpe_analyzer['sharperatio']
        if self.sharpe_ratio is None:
            self.sharpe_ratio = 0
        self.pnl = self.cerebro.broker.getvalue() - self.portfolioStartValue
        print('[SQN:%.2f, Sharpe Ratio:%.2f, Final Portfolio:%.2f, Total PnL:%.2f]' % (
        self.sqn, self.sharpe_ratio, self.cerebro.broker.getvalue(), self.pnl))

    def run(self):
        thestrats = self.cerebro.run()
        self.thestrat = thestrats[0]
        self.performance()


class MultiFeed(DataBase):
    def __init__(self):
        super(MultiFeed, self).__init__()
        # self.list=testData.select("start", "open", "high", "low", "close", "volume", "vwap", "exponential_moving_average").collect()

        self.list = multiTick.filter(multiTick.Ticker == self.p.dataname).select('datetime', "FirstTradePrice",
                                                                                 'HighTradePrice', 'LowTradePrice',
                                                                                 'LastTradePrice', 'Volume',
                                                                                 'UptickVolume', 'DowntickVolume',
                                                                                 'RepeatUptickVolume',
                                                                                 'RepeatDowntickVolume').collect()
        self.n = 0
        self.fromdate = self.list[0]['datetime']
        self.todate = self.list[len(self.list) - 1]['datetime']
        self.timeframe = bt.TimeFrame.Minutes
        print("from=%s,to=%s" % (self.fromdate, self.todate))

        self.m = {}

        # print(self.list)

    def start(self):
        # Nothing to do for this data feed type
        pass

    def stop(self):
        # Nothing to do for this data feed type
        pass

    def _load(self):
        if self.n >= len(self.list):
            return False

        r = self.list[self.n]
        self.lines.datetime[0] = date2num(r['datetime'])

        self.lines.open[0] = r['FirstTradePrice']
        self.lines.high[0] = r['HighTradePrice']
        self.lines.low[0] = r['LowTradePrice']
        self.lines.close[0] = r['LastTradePrice']
        self.lines.volume[0] = r['Volume']
        self.m[r['datetime']] = r

        self.n = self.n + 1
        return True


class MultiTickStrategy(StrategyTemplate):

    def __init__(self):  # Initiation
        super(MultiTickStrategy, self).__init__()
        self
        self.config["fast_period"] = int(self.config["fast_period"])
        self.config["slow_period"] = int(self.config["slow_period"])
        self.config["size"] = int(self.config["size"])

        self.smaFast = bt.ind.SimpleMovingAverage(period=self.config["fast_period"])
        self.smaSlow = bt.ind.SimpleMovingAverage(period=self.config["slow_period"])
        self.size = self.config["size"]

    def init_broker(broker):
        broker.setcash(1000000.0)
        broker.setcommission(commission=0.0)

    def add_data(cerebro, tick):
        # TODO: Parameterize the code
        data = MultiFeed(dataname=tick)

        cerebro.adddata(data, name=tick)
        return data

    def next(self):  # Processing
        super(MultiTickStrategy, self).next()
        dt = self.datas[0].datetime.datetime(0)
        r = self.data.m[dt]
        # print(r)
        size = self.cerebro.strat_params['size']
        threshold_PctChg = self.cerebro.strat_params['pct_chg']

        # model=self.cerebro.strat_params['model']
        df = spark.createDataFrame([r])
        # VWAP=r['vwap']
        # predictedVWAP = model.transform(df).collect()[0]['prediction']
        # expectedPctChg=(predictedVWAP-VWAP)/VWAP*100.0
        # print(self.data[0])

        postitions = [d._name for d, pos in self.getpositions().items() if pos]

        # goLong=self.datas[0].close>self.datas[0].open
        # goShort=self.datas[0].close< self.datas[0].open
        goLong = r['UptickVolume'] < r['DowntickVolume']
        goShort = r['UptickVolume'] > r['DowntickVolume']
        # print("expectedPctChg=%s,goLong=%s,goShort=%s" % (expectedPctChg,goLong,goShort))

        if not self.position:
            if goLong:
                print("%s:%s x BUY @ %.2f" % (dt, size, r['LastTradePrice']))
                self.buy(size=size)  # Go long
            else:
                print("%s:%s x SELL @ %.2f" % (dt, size, r['LastTradePrice']))
                self.sell(size=size)  # Go short
        elif self.position.size > 0 and goShort:
            print("%s:%s x SELL @ %.2f" % (dt, size * 2, r['LastTradePrice']))
            self.sell(size=size * 2)
        elif self.position.size < 0 and goLong:
            print("%s:%s x BUY @ %.2f" % (dt, size * 2, r['LastTradePrice']))
            self.buy(size=size * 2)


def run_strat():
    """

    :return:
    :rtype:
    """
    # TODO: Add code to dynamically fetch unique tickers - for now, I'm hardcoding
    tickers_multi = ["MSFT", "AAPL", "AMZN", "GOOG", "NVDA"]

    config = {"user": "user",
              "fast_period": "50",
              "slow_period": "200",
              "size": "100"
              }

    scenarios = []
    for p in range(0, 5):
        for s in range(0, 1):
            c = {'scenario': (p + 1), "size": 100, "pct_chg": 0.01}
            print(c)
        scenarios.append(c)
    scenarios

    # run scenarios
    best_config = None
    best_pnl = None
    n = 0
    for c in scenarios:
        print("*** [%s] RUN SCENARIO:%s" % ((n + 1), c))
        config = c
        algo = MultiAlgoStrategy(MultiTickStrategy)
        algo.cerebro.strat_params = config
        algo.run()
        ending_value = algo.cerebro.broker.getvalue()
        if best_pnl is None or best_pnl < ending_value:
            best_config = c
            best_pnl = ending_value
        n += 1