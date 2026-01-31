from datetime import datetime, UTC
from typing import Annotated

from pydantic import BaseModel, ConfigDict
from pydantic.fields import Field

from apps.py_trader.data.models.models import Config


class ConfigRead(BaseModel):
    id : Annotated[int, Field(frozen=True, gt=0)]
    maximum_risk_percentage : Annotated[float, Field(frozen=True, gt=0.0, lt=100.0)]
    default_risk_percentage : Annotated[float, Field(frozen=True, gt=0.0, lt=100.0)]
    total_balance : Annotated[float, Field(frozen=True, gt=0.00)]

    model_config = ConfigDict(from_attributes=True)

class ConfigCreate(BaseModel):
    maximum_risk_percentage : Annotated[float, Field(frozen=True, gt=0.0, lt=100.0)]
    default_risk_percentage : Annotated[float, Field(frozen=True, gt=0.0, lt=100.0)]
    total_balance : Annotated[float, Field(frozen=True, gt=0.00)]

    def to_config(self) -> Config:
        return Config(
            creation_datetime = datetime.now(UTC),
            maximum_risk_percentage = self.maximum_risk_percentage,
            default_risk_percentage = self.default_risk_percentage,
            total_balance = self.total_balance,
        )
