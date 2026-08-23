from fastapi import APIRouter, Depends
from apps.market_data.api.routes.routes import Routes
from apps.market_data.di import Container
from apps.market_data.data.repository import TimeFrameRepo
from apps.market_data.service.time_frame_schema import TimeFrameRead, TimeFrameCreate

timeframe_api_router = APIRouter(prefix=Routes.TimeFrame.PREFIX, tags=["TimeFrames"])

@timeframe_api_router.post(Routes.TimeFrame.CreateOne, response_model=TimeFrameRead)
async def create_timeframe(
    payload: TimeFrameCreate,
    timeframe_repo: TimeFrameRepo = Depends(Container.time_frame_repo)
):
    return await timeframe_repo.create_one(payload.to_time_frame())

@timeframe_api_router.get(Routes.TimeFrame.ReadMany, response_model=list[TimeFrameRead])
async def read_many_timeframes(
    timeframe_repo: TimeFrameRepo = Depends(Container.time_frame_repo)
):
    return await timeframe_repo.read_many()
