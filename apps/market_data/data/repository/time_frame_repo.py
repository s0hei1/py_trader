from typing import Sequence
from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession
from apps.market_data.data.models.models import TimeFrame

class TimeFrameRepo:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_one(self, time_frame: TimeFrame) -> TimeFrame:

        q = select(
            exists().
            where(TimeFrame.name == time_frame.name)
        )

        is_time_frame_duplicate = (await self.session.execute(q)).scalar()

        if is_time_frame_duplicate:
            raise ValueError(f"A time_frame with {time_frame.name} name already exists")

        self.session.add(time_frame)

        await self.session.commit()
        await self.session.refresh(time_frame)

        return time_frame

    async def read_many(self) -> Sequence[TimeFrame]:
        result = await self.session.execute(select(TimeFrame))
        return result.scalars().all()