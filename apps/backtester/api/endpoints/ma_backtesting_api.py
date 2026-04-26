from fastapi import APIRouter
from apps.backtester.api.router.routes import Routes
from apps.backtester.data.static_models.static_models import BacktesterLines
from apps.backtester.service.backtesting_service.backtesting_schema import LineRead

ma_backtesting_api = APIRouter(prefix = Routes.MABacktesting.PREFIX)


@ma_backtesting_api.get(Routes.MABacktesting.ReadManyMAs, response_model= list[LineRead])
async def read_many_moving_avergaes():
    MAs = BacktesterLines.read_many_moving_avergaes()

    return [LineRead(**ma) for ma in MAs]

@ma_backtesting_api.post(Routes.MABacktesting.BackTest)
async def backtest():
    return 1
