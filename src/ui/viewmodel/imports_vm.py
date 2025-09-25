from typing import Literal
import pandas as pd

from src.data.core.models import Pattern
from src.tools.di.container import Container
from src.ui.viewmodel.exceptions import VMException
from src.ui.viewmodel.vm_result import VMResult


class ImportsVM:
    Actions = Literal['Pattern', 'Lefex Info']

    _selected_action: Actions | None = None
    _uploaded_df: pd.DataFrame | None = None

    def __init__(self):
        self.patterns_repo = Container.pattern_repo()

    @property
    def selected_action(self):
        return self._selected_action

    @property
    def uploaded_df(self):
        return self._uploaded_df

    def set_selected_action(self, value: Actions) -> None:
        self._selected_action = value

    def set_uploaded_df(self, value: pd.DataFrame) -> None:
        action_required_cols = self.get_action_cols(self._selected_action)
        if not all(i in action_required_cols for i in value.columns):
            raise VMException(f"this columns is required in this actions: {action_required_cols}")

        self._uploaded_df = value

    def get_action_cols(self, selected_action: Actions | None) -> list[str]:

        if selected_action is None:
            raise VMException("please select an action")

        action_cols_name_dict = {
            'Pattern': Pattern.get_columns_name(exclude=['id'])
        }

        return action_cols_name_dict[selected_action]

    def on_sync_data_click(self) -> VMResult:
        if self._selected_action == 'Pattern':
            patterns = [Pattern(
                pattern_start_date_time=row['pattern_start_date_time'],
                pattern_end_date_time=row['pattern_end_date_time'],
                pattern_time_frame=row['pattern_time_frame'],
                symbol_name=row['symbol_name'],
            ) for i, row in self._uploaded_df.iterrows()]
            self.patterns_repo.create_many(patterns)
            
            return VMResult()
