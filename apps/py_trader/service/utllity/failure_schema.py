from typing import List, Union, Any
from pydantic import BaseModel

class ErrorContext(BaseModel):
    error: str

class ErrorDetail(BaseModel):
    type: str | None = None
    loc: List[Union[str, int]] | None = None
    msg: str = None
    input: Any | None = None
    ctx: ErrorContext | None = None

class ErrorResponse(BaseModel):
    detail: List[ErrorDetail]
