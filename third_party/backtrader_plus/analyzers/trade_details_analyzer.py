class TradeDetailsAnalyzer(bt.Analyzer):

    def notify_trade(self, trade: Trade):
        if trade.isclosed:
            trade_ = AutoOrderedDict()
            trade_.open_date_time = trade.open_datetime()
            trade_.close_date_time = trade.close_datetime()
            trade_.trade_id = trade.tradeid
            trade_.len = trade.barlen

            self.rets.trades_.append(trade_)

    def stop(self):
        self.rets._close()

    def create_analysis(self):
        self.rets = AutoOrderedDict()

        self.rets.trades_ = []
