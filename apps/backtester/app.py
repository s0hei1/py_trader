import os
from typing import AnyStr
import sys

from apps.backtester.api.endpoints.strategy_api import strategy_api


def get_current_path_parent(path: AnyStr, depth=1):
    if depth == 0:
        return path
    else:
        path = os.path.dirname(path)
        return get_current_path_parent(path=path, depth=depth - 1)

sys.path.append(get_current_path_parent(path=os.path.abspath(__file__), depth=3))

from fastapi import FastAPI
from apps.backtester.api.endpoints.ma_backtesting_api import ma_backtesting_api
from apps.backtester.api.endpoints.setup_api import setup_api
from apps.backtester.api.endpoints.risk_management_api import risk_management_api

app = FastAPI()

app.include_router(ma_backtesting_api)
app.include_router(setup_api)
app.include_router(risk_management_api)
app.include_router(strategy_api)