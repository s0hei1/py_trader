from __future__ import annotations

from pydantic import BaseModel

class LineRead(BaseModel):
    id : int
    name : str

class MaBacktestCreate(BaseModel):
    moving_averages_ids : list[int]
    rules : list[RuleSchema]

class RuleSchema(BaseModel):
    left_side_ma_id : int
    right_side_ma_id : int
