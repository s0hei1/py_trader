from typing import Annotated
from pydantic import BaseModel, ConfigDict,Field
from apps.py_trader.data.models.models import Symbol

class SymbolRead(BaseModel):
    id: int
    base_currency: str
    quote_currency: str

    model_config = ConfigDict(from_attributes=True)

class SymbolCreate(BaseModel):
    base_currency: Annotated[str, Field(max_length=5, min_length=1)]
    quote_currency: Annotated[str, Field(max_length=5, min_length=1)]

    def to_symbol(self) -> Symbol:
        return Symbol(
            base_currency=self.base_currency.upper(),
            quote_currency=self.quote_currency.upper(),
        )

