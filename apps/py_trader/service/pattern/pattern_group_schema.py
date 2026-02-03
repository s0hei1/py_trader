from datetime import datetime
from pydantic import BaseModel, ConfigDict
from apps.py_trader.data.enums.times_frame_enum import TimeFrameEnum


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

