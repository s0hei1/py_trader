from typing import Sequence
from sqlalchemy import select, exists
from sqlalchemy.orm import Session
import datetime as dt
import pandas as pd

from apps.py_trader.data.enums.times_frame_enum import TimeFrameEnum
from apps.py_trader.data.models.models import Pattern


class PatternRepo:

    def __init__(self, session: Session):
        self.session = session

    def read_many(
        self,
        id: int | None = None,
        group_id: int | None = None,
        symbol_id: int | None = None,
        time_frame: TimeFrameEnum | None = None,
        start_dt: dt.datetime | None = None,
        end_dt: dt.datetime | None = None,
        only_active: bool = True,
        return_first: bool = False,
    ) -> Sequence[Pattern] | Pattern | None:

        q = select(Pattern)

        if id is not None:
            q = q.where(Pattern.id == id)

        if group_id is not None:
            q = q.where(Pattern.pattern_group_id == group_id)

        if symbol_id is not None:
            q = q.where(Pattern.symbol_id == symbol_id)

        if time_frame is not None:
            q = q.where(Pattern.time_frame == time_frame)

        if only_active:
            q = q.where(Pattern.is_active.is_(True))

        if start_dt and end_dt:
            q = q.where(
                Pattern.pattern_first_candle <= end_dt,
                Pattern.pattern_last_candle >= start_dt
            )
        elif start_dt:
            q = q.where(Pattern.pattern_last_candle >= start_dt)
        elif end_dt:
            q = q.where(Pattern.pattern_first_candle <= end_dt)

        result = self.session.execute(q).scalars()

        return result.first() if return_first else result.all()

    def create(self, pattern: Pattern) -> Pattern:

        if pattern.pattern_first_candle >= pattern.pattern_last_candle:
            raise ValueError("pattern_first_candle must be earlier than pattern_last_candle")

        # prevent duplicates
        q = select(
            exists().where(
                Pattern.symbol_id == pattern.symbol_id,
                Pattern.time_frame == pattern.time_frame,
                Pattern.pattern_first_candle == pattern.pattern_first_candle,
                Pattern.pattern_last_candle == pattern.pattern_last_candle,
            )
        )

        if self.session.execute(q).scalar():
            raise ValueError("Pattern already exists")

        self.session.add(pattern)
        self.session.commit()
        self.session.refresh(pattern)

        return pattern

    def create_many(self, patterns: list[Pattern]) -> list[Pattern]:
        self.session.add_all(patterns)
        self.session.commit()
        return patterns

    def deactivate(self, pattern_id: int) -> None:
        pattern = self.session.get(Pattern, pattern_id)
        if pattern:
            pattern.is_active = False
            self.session.commit()

    def get_df(
        self,
        symbol_id: int | None = None,
        time_frame: TimeFrameEnum | None = None,
    ) -> pd.DataFrame:

        q = select(
            Pattern.id,
            Pattern.pattern_group_id,
            Pattern.symbol_id,
            Pattern.time_frame,
            Pattern.pattern_first_candle,
            Pattern.pattern_last_candle,
            Pattern.is_active,
        )

        if symbol_id:
            q = q.where(Pattern.symbol_id == symbol_id)

        if time_frame:
            q = q.where(Pattern.time_frame == time_frame)

        result = self.session.execute(q)

        return pd.DataFrame(result.fetchall(), columns=result.keys())