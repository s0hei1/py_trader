import os
from typing import AnyStr
import sys

from apps.py_trader.api.exception_handler.value_error_handler import value_error_exception_handler


def get_current_path_parent(path: AnyStr, depth=1):
    if depth == 0:
        return path
    else:
        path = os.path.dirname(path)
        return get_current_path_parent(path=path, depth=depth - 1)

sys.path.append(get_current_path_parent(path=os.path.abspath(__file__), depth=3))

from fastapi import FastAPI
from apps.py_trader.api.end_points.base_api import base_api
from apps.py_trader.api.end_points.strategy_api import strategy_api
from apps.py_trader.api.end_points.symbol_api import symbol_api
from apps.py_trader.api.end_points.pattern_api import pattern_api

app = FastAPI()

app.include_router(base_api)
app.include_router(strategy_api)
app.include_router(symbol_api)
app.include_router(pattern_api)


app.add_exception_handler(ValueError, value_error_exception_handler)

