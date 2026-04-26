from __future__ import annotations
from typing import Annotated
from pydantic import BaseModel, Field, ConfigDict

from apps.backtester.data.models.models import Strategy


class StrategyCreate(BaseModel):
    description: Annotated[str, Field(max_length=64)]
    setup_id: Annotated[int, Field(gt=0)]
    risk_management_id: Annotated[int, Field(gt=0)]

    def to_strategy(self) -> Strategy:
        return Strategy(
            description=self.description,
            setup_id=self.setup_id,
            risk_management_id=self.risk_management_id,
        )


class StrategyRead(BaseModel):
    id: int
    description: str
    setup_id: int
    risk_management_id: int

    model_config = ConfigDict(from_attributes=True)

