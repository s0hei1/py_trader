from pydantic import BaseModel,ConfigDict

from apps.market_data.data.models.models import Symbol


class SymbolCreate(BaseModel):
    name: str

    def to_symbol(self) -> Symbol:
        return Symbol(name=self.name)


class SymbolRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str