from __future__ import annotations
from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field, model_validator

from apps.backtester.data.enums.enums import StoplossType
from apps.backtester.data.models.models import RiskManagement


class RiskManagementCreate(BaseModel):
    description: Annotated[str, Field()]
    stop_loss_type: StoplossType
    stop_loss_size: Annotated[float, Field(gt=0.0)]
    take_profit_size: Annotated[float, Field(gt=0.0)]

    @model_validator(mode='after')
    def validate_pattern_createion(self):
        if self.stop_loss_type == StoplossType.PRICE_RATIO and self.stop_loss_size > 100.0: \
                raise ValueError("Stop loss size on price ratio Stoploss_type mode can not be grater than 100%")

        return self

    def to_risk_management(self) -> RiskManagement:
        return RiskManagement(
            description=self.description,
            stop_loss_type=self.stop_loss_type,
            stop_loss_size=self.stop_loss_size,
            take_profit_size=self.take_profit_size,
        )


class RiskManagementRead(BaseModel):
    id: int
    description: str
    stop_loss_type: StoplossType
    stop_loss_size: float
    take_profit_size: float

    model_config = ConfigDict(from_attributes=True)
