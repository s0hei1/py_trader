from typing import Annotated
from pydantic import BaseModel, ConfigDict
from pydantic.fields import Field
from apps.py_trader.data.enums.strategy_type import StrategyType
from apps.py_trader.data.models.models import Strategy


class StrategyRead(BaseModel):
    id: int
    strategy_name: str
    strategy_type: StrategyType

    model_config = ConfigDict(from_attributes=True)


class StrategyCreate(BaseModel):
    strategy_name: Annotated[str, Field(max_length=64, min_length=1)]
    strategy_type: StrategyType

    def to_strategy(self) -> Strategy:
        return Strategy(
            strategy_name=self.strategy_name,
            strategy_type=self.strategy_type,
        )


class StrategyUpdate(BaseModel):
    strategy_name: Annotated[str, Field(max_length=64, min_length=1)]
    strategy_type: StrategyType
