from src.data.repo.pattern_repo import PatternRepo
from src.tools.di.container import Container
import pandas as pd
from third_party import mt5_overhead as mt5_source
from third_party.candlestic.defaults import DefaultSymbols, DefaultTimeFrames
from more_itertools import first
import datetime as dt
class PatternVM:
    _patterns_df: pd.DataFrame

    _selected_pattern: pd.DataFrame | None = None
    _selected_pattern_trigger_time: pd.DataFrame | None = None

    def __init__(self):
        self.pattern_repo: PatternRepo = Container.pattern_repo()

        patterns_df = self.pattern_repo.get_patterns(as_data_frame=True)
        self._set_patterns_df(patterns_df)

    def _set_patterns_df(self, value: pd.DataFrame):
        self._patterns_df = value

    def set_selected_pattern(self, selected_pattern_id: int):
        pattern = first(
            self.pattern_repo.read_many(id=selected_pattern_id)
        )

        selected_symbol = DefaultSymbols.get_symbol_by_name(pattern.symbol_name)
        selected_timeframe = DefaultTimeFrames.get_time_frame_by_name(pattern.pattern_time_frame)

        mt5_result = mt5_source.get_market_historical_data(
            symbol=selected_symbol,
            timeframe=selected_timeframe,
            date_from=pattern.pattern_start_date_time,
            date_to=pattern.pattern_end_date_time,
            date_to_le = True,
        )
        self._selected_pattern = mt5_result.result.to_dataframe()


        mt5_result_trigger_time = mt5_source.get_market_historical_data(
            symbol=selected_symbol,
            timeframe=DefaultTimeFrames.get_trigger_time(selected_timeframe),
            date_from=pattern.pattern_start_date_time,
            date_to=pattern.pattern_end_date_time + dt.timedelta(minutes=selected_timeframe.included_m1),
        )

        print(len(mt5_result_trigger_time.result))

        self._selected_pattern_trigger_time = mt5_result_trigger_time.result.to_dataframe()


    @property
    def patterns_df(self):
        return self._patterns_df

    @property
    def selected_pattern(self) -> pd.DataFrame:
        return self._selected_pattern

    @property
    def selected_pattern_trigger_time(self) -> pd.DataFrame:
        return self._selected_pattern_trigger_time
