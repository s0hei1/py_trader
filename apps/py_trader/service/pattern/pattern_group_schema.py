from datetime import datetime
from pydantic import BaseModel, ConfigDict, model_validator
from apps.py_trader.data.enums.times_frame_enum import TimeFrameEnum
from apps.py_trader.data.models.models import Pattern


class PatternRead(BaseModel):
    id: int
    pattern_group_id: int
    pattern_group_name: int
    pattern_first_candle: datetime
    pattern_last_candle: datetime
    is_active: bool
    time_frame: TimeFrameEnum
    symbol_id: int
    symbol_name: int

    model_config = ConfigDict(from_attributes=True)


class PatternCreate(BaseModel):
    pattern_group_id: int
    pattern_first_candle: datetime
    pattern_last_candle: datetime
    is_active: bool
    time_frame: TimeFrameEnum
    symbol_id: int

    @model_validator(mode='after')
    def validate_pattern_createion(self):
        if self.pattern_first_candle >= self.pattern_last_candle:
            raise ValueError("pattern first candle datetime can not grater than last candle datetime")

        if not self.is_active:
            raise ValueError("you can not add inactive pattern!")

        return self

    def to_pattern(self) -> Pattern:
        return Pattern(
            pattern_group_id=self.pattern_group_id,
            pattern_first_candle=self.pattern_first_candle,
            pattern_last_candle=self.pattern_last_candle,
            is_active=self.is_active,
            time_frame=self.time_frame,
            symbol_id=self.symbol_id,
        )
