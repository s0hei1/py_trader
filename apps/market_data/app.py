import os
from typing import AnyStr
import sys


def get_current_path_parent(path: AnyStr, depth=1):
    if depth == 0:
        return path
    else:
        path = os.path.dirname(path)
        return get_current_path_parent(path=path, depth=depth - 1)


sys.path.append(get_current_path_parent(path=os.path.abspath(__file__), depth=3))

from fastapi import FastAPI
from apps.market_data.api.end_points import \
    base_api_router, symbol_api_router, timeframe_api_router, broker_api_router,candle_api_router
from apps.market_data.data.log.log import setup_logging


setup_logging()
app = FastAPI()

app.include_router(base_api_router)
app.include_router(symbol_api_router)
app.include_router(timeframe_api_router)
app.include_router(broker_api_router)
app.include_router(candle_api_router)
