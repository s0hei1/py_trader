from datetime import datetime
from typing import Sequence
from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession
from apps.market_data.data.models.models import Candle
from sqlalchemy import func


class CandleRepo:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_many(self, candles: Sequence[Candle]) -> Sequence[Candle]:

        if len(candles) == 0:
            raise ValueError("Candles cannot be empty")

        candles = sorted(candles, key=lambda candle: candle.date_time)

        symbol_id = candles[0].symbol_id
        time_frame_id = candles[0].time_frame_id
        broker_id = candles[0].time_frame_id

        if any([c.symbol_id != symbol_id for c in candles]):
            raise ValueError('all candle must contain same symbol')
        if any([c.time_frame_id != time_frame_id for c in candles]):
            raise ValueError('all candle must contain same time_frame')
        if any([c.broker_id != broker_id for c in candles]):
            raise ValueError('all candle must contain same broker')

        q_max_date_time = await (self.session.execute(
            select(func.max(Candle.date_time))
            .where(
                Candle.symbol_id == symbol_id,
                Candle.time_frame_id == time_frame_id,
                Candle.broker_id == broker_id
            )
        ))
        q_min_date_time = await (self.session.execute(
            select(func.min(Candle.date_time))
            .where(
                Candle.symbol_id == symbol_id,
                Candle.time_frame_id == time_frame_id,
                Candle.broker_id == broker_id
            )
        ))
        max_date_time = q_max_date_time.scalar_one_or_none()
        min_date_time = q_min_date_time.scalar_one_or_none()

        result = None

        if max_date_time is not None and min_date_time is not None:
            newer_candles = [c for c in candles if c.date_time > max_date_time]
            older_candles = [c for c in candles if c.date_time < min_date_time]
            self.session.add_all(newer_candles)
            self.session.add_all(older_candles)
            result = older_candles + newer_candles
        else:
            self.session.add_all(candles)
            result = candles

        await self.session.commit()

        for c in result:
            await self.session.refresh(c)

        return result

    async def read_many(
            self,
            broker_id: int,
            symbol_id: int,
            time_frame_id : int,
            from_date_time : datetime | None = None,
            to_date_time : datetime | None = None,
            count : int | None = None,
    ) -> Sequence[Candle]:
        q = select(Candle).where(
            Candle.symbol_id == symbol_id,
            Candle.time_frame_id == time_frame_id,
            Candle.broker_id == broker_id,
        )

        if from_date_time is not None:
            q = q.where(Candle.date_time >= from_date_time)
        if to_date_time is not None:
            q = q.where(Candle.date_time <= to_date_time)

        q = q.order_by(Candle.date_time)

        if count is not None:
            q = q.limit(count)

        q_result = await self.session.execute(q)
        candles = q_result.scalars().all()

        return candles
