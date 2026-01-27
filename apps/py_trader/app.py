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
from apps.py_trader.api.end_points.base_api import base_api

app = FastAPI()

app.include_router(base_api)


