from src.data.repo.pattern_repo import PatternRepo
from src.tools.di.container import Container
import pandas as pd

class PatternVM:

    _patterns_df : pd.DataFrame


    def __init__(self):
        self.pattern_repo : PatternRepo = Container.pattern_repo()

        patterns_df = self.pattern_repo.get_patterns(as_data_frame=True)
        self._set_patterns_df(patterns_df)



    def _set_patterns_df(self,value : pd.DataFrame):
        self._patterns_df = value
    @property
    def patterns_df(self) :
        return self._patterns_df


