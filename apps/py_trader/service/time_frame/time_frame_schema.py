from pydantic import BaseModel,ConfigDict

from apps.market_data.data.models.models import TimeFrame


class TimeFrameCreate(BaseModel):
    name: str
    resolution: int

    def to_time_frame(self) -> TimeFrame:
        return TimeFrame(
            name = self.name,
            resolution = self.resolution,
        )


class TimeFrameRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    resolution: int
