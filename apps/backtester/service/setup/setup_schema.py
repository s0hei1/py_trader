from __future__ import annotations
from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field,model_validator
from apps.backtester.data.enums.enums import TriggerType
from apps.backtester.data.models.models import Setup
from apps.backtester.data.static_models.static_models import BacktesterLines


class SetupCreate(BaseModel):
    description: Annotated[str, Field(max_length=64)]
    trigger_type: TriggerType
    line_a_id: Annotated[int, Field(gt=0)]
    line_a_period: Annotated[int, Field(gt=0)] | None
    line_b_id: Annotated[int, Field(gt=0)]
    line_b_period: Annotated[int, Field(gt=0)] | None

    def to_setup(self) -> Setup:

        line_a = BacktesterLines.read_line_by_id(self.line_a_id)
        line_b = BacktesterLines.read_line_by_id(self.line_b_id)

        return Setup(
            description=self.description,
            trigger_type=self.trigger_type,
            line_a_id=self.line_a_id,
            line_a_name=line_a.name,
            line_a_period=self.line_a_period if line_a.line_type != 'PRICE' else None,
            line_b_id=self.line_b_id,
            line_b_name=line_b.name,
            line_b_period=self.line_b_period if line_b.line_type != 'PRICE' else None,
        )


class SetupRead(BaseModel):
    id: int
    description: str
    trigger_type: TriggerType
    line_a_name: str
    line_a_id: int
    line_b_name: str
    line_b_id: int

    model_config = ConfigDict(from_attributes=True)
