from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import DatabaseError

from apps.py_trader.service.utllity.failure_schema import ErrorResponse, ErrorDetail


async def database_exceptions(request : Request, e : DatabaseError) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content=ErrorResponse(
            detail=[
                ErrorDetail(
                    type="database_error",
                    msg=e._message(),
                )
            ]
        ).model_dump(exclude_unset=True)
    )
