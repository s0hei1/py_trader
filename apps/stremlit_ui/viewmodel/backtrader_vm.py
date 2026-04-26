from apps.stremlit_ui.datasource.api_clients.market_data_client.api_client import MarketDataAPIClient
from apps.stremlit_ui.datasource.api_clients.market_data_client.client_models import BrokerModel, SymbolModel, \
    TimeFrameModel, ReadManyCandlesRequest
from apps.stremlit_ui.datasource.models.analyzer_models import TimeReturnAnalyzerModel
from apps.stremlit_ui.di.Container import Container
from third_party.backtrader_plus.analyzers.equity_tracker import EquityTracker
from third_party.backtrader_plus.strategies import strategies_dict
from backtrader.analyzers import TradeAnalyzer, DrawDown, PositionsValue, TimeReturn
from backtrader import Cerebro, Strategy, TimeFrame
from backtrader.feeds import PandasData
import pandas as pd
from apps.stremlit_ui.datasource.models import AnalyzerDataModel, TradeAnalyzerModel, DrawDownAnalyzerModel
from toolz import first
from third_party.backtrader_plus.analyzers import TradeDetailsAnalyzer
from backtrader.plot import Plot



class BackTraderVM:
    _analyzers: list[AnalyzerDataModel] | None = None
    _broker_cash: int | None = None
    _selected_analyzers: set | None = None
    _market_data: pd.DataFrame | None = None
    _selected_strategy: type | None = None
    _cerebro_result: Strategy | None = None
    _cerebro_plot_fig = None
    _market_data_api_client : MarketDataAPIClient | None = None

    def __init__(self,market_data_api_client : MarketDataAPIClient = Container.market_data_api_client()):

        self._analyzers = [
            AnalyzerDataModel(name='Trade Analyzer', analyzer=TradeAnalyzer, attr_name='trade_analyzer'),
            AnalyzerDataModel(name='Draw Down', analyzer=DrawDown, attr_name='draw_down'),
            AnalyzerDataModel(name='Positions Value', analyzer=PositionsValue, attr_name='positions_value'),
            AnalyzerDataModel(name='Trade Details', analyzer=TradeDetailsAnalyzer, attr_name='trade_details'),
            AnalyzerDataModel(name='Time Return', analyzer=TimeReturn, attr_name='time_return',
                              kwargs={'timeframe': TimeFrame.Months}),
            AnalyzerDataModel(name='Equity Tracker', analyzer=EquityTracker, attr_name='equity_tracer'),
        ]

        self._broker_cash = 1000000
        self._selected_analyzers = set()

        self._market_data_api_client = market_data_api_client
        self._market_data_brokers = self._market_data_api_client.get_brokers()
        self._market_data_symbols = self._market_data_api_client.get_symbols()
        self._market_data_time_frames = self._market_data_api_client.get_time_frames()


    def get_strategies(self) -> list:
        return [i for i in strategies_dict]

    def get_strategy_by_name(self, name: str) -> Strategy:
        return strategies_dict[name]

    def run_strategy(self):
        df_for_feed = self._market_data.copy(deep=True)
        df_for_feed['date_time'] = pd.to_datetime(df_for_feed['date_time'])
        df_for_feed = df_for_feed.set_index("date_time")
        df_for_feed['volume'] = 0
        data = PandasData(dataname=df_for_feed)
        cerebro = Cerebro()
        cerebro.adddata(data)
        cerebro.addstrategy(self._selected_strategy)
        for i in self._analyzers:
            cerebro.addanalyzer(i.analyzer, _name=i.attr_name, **i.kwargs)

        cerebro.broker.setcash(self._broker_cash)
        results = cerebro.run()

        self._cerebro_result = results[0]

        if False:
            self._cerebro_plot_fig = self._cerebro_plot_fig = cerebro.plot(
                plotter=Plot(style='candlestick'),
                volume=False
            )

    def get_analyzers(self):
        return [i.name for i in self._analyzers]

    def add_analyzer(self, analyzer_name: str):
        if analyzer_name not in self._analyzers:
            raise ValueError("Unknown analyzer name")

        self._selected_analyzers.add(analyzer_name)

    def set_selected_strategy(self, strategy_name: str):
        self._selected_strategy = self.get_strategy_by_name(strategy_name)

    def get_trade_analyzer_analysis(self) -> TradeAnalyzerModel | None:
        if self._cerebro_result is None:
            return None

        trade_analyzer_attr_name = first([i.attr_name for i in self._analyzers if i.analyzer == TradeAnalyzer])

        trade_analyzer: TradeAnalyzer = getattr(self._cerebro_result.analyzers, trade_analyzer_attr_name)

        return TradeAnalyzerModel.from_trade_analyzer(trade_analyzer)

    def get_time_return_analyzer_analysis(self):
        if self._cerebro_result is None:
            return None

        analyzer_attr_name = first([i.attr_name for i in self._analyzers if i.analyzer == TimeReturn])

        time_return_analyzer: TimeReturn = getattr(self._cerebro_result.analyzers, analyzer_attr_name)

        return TimeReturnAnalyzerModel.from_time_return_analyzer(time_return_analyzer)

    def get_equity_analysis(self):
        if self._cerebro_result is None:
            return None

        analyzer_attr_name = first([i.attr_name for i in self._analyzers if i.analyzer == EquityTracker])

        analyzer: EquityTracker = getattr(self._cerebro_result.analyzers, analyzer_attr_name)
        df = analyzer.get_analysis(as_dataframe=True)
        df['Equity'] = df['Equity'] / 100
        df['Equity'] = df['Equity'].astype(int)
        return df

    def get_trade_details_dataframe(self) -> pd.DataFrame | None:
        if self._cerebro_result is None:
            return None

        analyzer_attr_name = first([i.attr_name for i in self._analyzers if i.analyzer == TradeDetailsAnalyzer])

        analyzer: TradeDetailsAnalyzer = getattr(self._cerebro_result.analyzers, analyzer_attr_name)

        return analyzer.get_analysis(as_dataframe=True)

    def get_draw_down_analysis(self) -> DrawDownAnalyzerModel | None:
        if self._cerebro_result is None:
            return None

        analyzer_attr_name = first([i.attr_name for i in self._analyzers if i.analyzer == DrawDown])

        analyzer: DrawDown = getattr(self._cerebro_result.analyzers, analyzer_attr_name)

        return DrawDownAnalyzerModel.from_drawdown_analyzer(analyzer)

    def get_cerebro_plot_fig(self) -> list | None:
        return self._cerebro_plot_fig

    def get_market_data_info(self) -> tuple[list[BrokerModel],list[SymbolModel],list[TimeFrameModel]]:
        return self._market_data_brokers, self._market_data_symbols, self._market_data_time_frames

    def get_market_data(self, broker_id : int, symbol_id : int, time_frame_id : int):
        self._market_data = self._market_data_api_client.get_candles(
            ReadManyCandlesRequest(
                time_frame_id = time_frame_id,
                broker_id = broker_id,
                symbol_id = symbol_id,
            ),
            to_dataframe=True
        )
        self._market_data = self._market_data.rename(
            columns={'open_' : 'open'}
        )
        print(self._market_data.columns)

    @property
    def is_data_feed(self):
        return self._market_data is not None