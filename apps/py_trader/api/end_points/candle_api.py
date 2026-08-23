from fastapi import APIRouter, Depends,UploadFile
from apps.market_data.api.routes.routes import Routes
from apps.market_data.di import Container
from apps.market_data.data.repository import CandleRepo
from apps.market_data.service.candle_schema import CandleCreate, CandleRead,candle_create_to_candle,validate_candles_csv_file
from logging import getLogger

logger = getLogger(__name__)
candle_api_router = APIRouter(prefix=Routes.Candle.PREFIX, tags=["Candles"])

@candle_api_router.post(Routes.Candle.CreateMany, response_model=list[CandleRead])
async def create_many_candles(
    payloads: list[CandleCreate],
    candle_repo: CandleRepo = Depends(Container.candle_repo)
):
    logger.info(len(payloads))

    return await candle_repo.create_many(
        candle_create_to_candle(payloads)
    )

@candle_api_router.get(Routes.Candle.ReadMany, response_model=list[CandleRead])
async def read_many_candles(
    broker_id : int,
    symbol_id : int,
    time_frame_id : int,
    candle_repo: CandleRepo = Depends(Container.candle_repo)
):
    return await candle_repo.read_many(
        broker_id = broker_id,
        symbol_id = symbol_id,
        time_frame_id = time_frame_id,
    )

# @candle_api_router.post(Routes.Candle.CreateManyByFile, response_model=CandleRead)
# async def create_many_candles_by_file(
#     file: UploadFile,
#     candle_repo: CandleRepo = Depends(Container.candle_repo)
# ):
#     file = validate_candles_csv_file(file)
#
#     raise NotImplemented("This method is not implemented yet")


