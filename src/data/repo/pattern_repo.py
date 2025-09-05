from typing import Sequence

from sqlalchemy import select, exists
from sqlalchemy.orm import Session
import datetime as dt

from src.data.core.models import Pattern


class PatternRepo:

    def __init__(self, session: Session):
        self.session = session

    def get_patterns_by_filter(self,
                               id: int = None,
                               pattern_start_date_time: dt.datetime = None,
                               pattern_end_date_time: dt.datetime = None,
                               pattern_time_frame: str = None,
                               symbol_name: str = None,
                               ) -> Sequence[Pattern]:

        q = select(Pattern)

        if id is not None:
            q.where(Pattern.id == id)
        if pattern_start_date_time is not None:
            q.where(Pattern.pattern_start_date_time == pattern_start_date_time)
        if pattern_end_date_time is not None:
            q.where(Pattern.pattern_end_date_time == pattern_end_date_time)
        if pattern_time_frame is not None:
            q.where(Pattern.pattern_time_frame == pattern_time_frame)
        if symbol_name is not None:
            q.where(Pattern.symbol_name == symbol_name)

        result = self.session.execute(q).scalars().all()

        return result

    def add_pattern(self, pattern: Pattern):

        q = select(
            exists().where(
            Pattern.pattern_start_date_time == pattern.pattern_start_date_time,
            Pattern.pattern_end_date_time == pattern.pattern_end_date_time,
            Pattern.symbol_name == pattern.symbol_name,
            Pattern.pattern_time_frame == pattern.pattern_time_frame
        )
        )

        pattern_existance : bool = self.session.execute(q).scalar()

        if pattern_existance:
            raise Exception(f"a pattern with details : {pattern.__dict__} \nis exists")

        self.session.add(pattern)
        self.session.commit()
        self.session.refresh(pattern)

        return pattern
