import pandas as pd

from third_party.candlestic import Symbol, Chart


class ExternalDataframeLoader:

    @classmethod
    def load_EURUSD_m15_20200401_20230401(cls) -> Chart:
        df = pd.read_csv(r'/apps/backtester/assets/eurusd_m15_2020-04-01_2023-04-01.csv')

        Chart.from_pd_dataframe(df)
