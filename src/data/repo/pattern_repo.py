from typing import Sequence
from sqlalchemy import select, exists
from sqlalchemy.orm import Session
import datetime as dt
import pandas as pd
from src.data.core.models import Pattern
from src.data.exceptions.exc import InvalidArgumentException


class PatternRepo:

    def __init__(self, session: Session):
        self.session = session

    def read_many(self,
                  id: int = None,
                  pattern_start_date_time: dt.datetime = None,
                  pattern_end_date_time: dt.datetime = None,
                  pattern_time_frame: str = None,
                  symbol_name: str = None,
                  return_first: bool = False
                  ) -> Sequence[Pattern]:

        q = select(Pattern)

        if id is not None:
            q = q.where(Pattern.id == id)
        if pattern_start_date_time is not None:
            q = q.where(Pattern.pattern_start_date_time == pattern_start_date_time)
        if pattern_end_date_time is not None:
            q = q.where(Pattern.pattern_end_date_time == pattern_end_date_time)
        if pattern_time_frame is not None:
            q = q.where(Pattern.pattern_time_frame == pattern_time_frame)
        if symbol_name is not None:
            q = q.where(Pattern.symbol_name == symbol_name)

        result = self.session.execute(q).scalars().all()

        return result

    def create(self, pattern: Pattern) -> Pattern:

        if pattern.pattern_start_date_time >= pattern.pattern_end_date_time:
            raise InvalidArgumentException("Pattern start dt must less than end dt")

        q = select(
            exists().where(
                Pattern.pattern_start_date_time == pattern.pattern_start_date_time,
                Pattern.pattern_end_date_time == pattern.pattern_end_date_time,
                Pattern.symbol_name == pattern.symbol_name,
                Pattern.pattern_time_frame == pattern.pattern_time_frame
            )
        )

        pattern_existance: bool = self.session.execute(q).scalar()

        if pattern_existance:
            raise Exception(f"a pattern with details : {pattern.__dict__} \nis exists")

        self.session.add(pattern)
        self.session.commit()
        self.session.refresh(pattern)

        return pattern

    def create_many(self, patterns: list[Pattern]) -> list[Pattern]:
        for i, pattern, in enumerate(patterns):
            patterns[i] = self.create(pattern)
        return patterns

    def get_patterns(self, as_data_frame: bool | None = None) -> Sequence[Pattern] | pd.DataFrame:

        q = select(Pattern)

        result = self.session.execute(q).scalars().all()

        if as_data_frame:
            return pd.DataFrame([i.as_dict() for i in result])

        return result

    def get_patterns_df(self) -> pd.DataFrame:
        q = select(
            Pattern.id,
            Pattern.symbol_name,
            Pattern.pattern_time_frame,
            Pattern.pattern_start_date_time,
            Pattern.pattern_end_date_time
        )

        result = self.session.execute(q)

        df = pd.DataFrame(result, columns=[key for key in result.keys()])

        return df
