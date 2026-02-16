from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

from apps.py_trader.service.utllity.failure_schema import ErrorResponse, ErrorDetail


async def value_error_exception_handler(request : Request, e : ValueError) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content=ErrorResponse(
            detail=[
                ErrorDetail(
                    type="logical_exception",
                    msg=str(e),
                )
            ]
        ).model_dump(exclude_unset=True)
    )
