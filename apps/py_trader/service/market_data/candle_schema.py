from typing import Sequence
import pandas as pd
from fastapi import UploadFile
from pydantic import BaseModel,ConfigDict
from datetime import datetime
from apps.market_data.data.models.models import Candle

class CandleCreate(BaseModel):
    symbol_id: int
    time_frame_id: int
    broker_id: int
    date_time: datetime
    open_: float
    high: float
    low: float
    close: float
    volume: float

class CandleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    symbol_id: int
    time_frame_id: int
    broker_id: int
    date_time: datetime
    open_: float
    high: float
    low: float
    close: float
    volume: float

def candle_create_to_candle(candles : list[CandleCreate]) -> Sequence[Candle]:
    return [Candle(**c.model_dump()) for c in candles]

def validate_candles_csv_file(file : UploadFile) -> UploadFile:
    valid_formats = ['csv', 'xlsx', 'xls']

    if file.content_type not in valid_formats:
        raise ValueError('Invalid file format')

    return file

def convert_file_to_dataframe(file : UploadFile) -> pd.DataFrame:
    if file.content_type == 'csv':
        return pd.read_csv(file.file)
    if file.content_type in ['xlsx','xls']:
        return pd.read_excel(file.file)

