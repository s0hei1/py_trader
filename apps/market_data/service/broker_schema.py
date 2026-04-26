from pydantic import BaseModel,ConfigDict

from apps.market_data.data.models.models import Broker


class BrokerCreate(BaseModel):
    name: str

    def to_broker(self) -> Broker:
        return Broker(name = self.name)


class BrokerRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str