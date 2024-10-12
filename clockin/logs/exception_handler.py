"""Exception Handling"""
import sys

from typing import Union

from fastapi import Request
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.exception_handlers import http_exception_handler as _http_exception_handler
from fastapi.exception_handlers import (
    request_validation_exception_handler as _request_validation_exception_handler,
)
from fastapi.responses import JSONResponse
from fastapi.responses import PlainTextResponse
from fastapi.responses import Response

from clockin.logs.logger import file_logger

async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """
    Client input is not valid
    """
    query_params = request.query_params._dict  # pylint: disable=protected-access
    detail = {"errors": exc.errors(), "body": exc.body, "query_params": query_params}
    file_logger.warning(detail)
    return await _request_validation_exception_handler(request, exc)


async def http_exception_handler(
    request: Request, exc: HTTPException
) -> Union[JSONResponse, Response]:
    """
    HTTPException is explicitly raised
    """
    detail = {"status_code": exc.status_code, "exception": exc.detail}
    file_logger.exception(detail)
    return await _http_exception_handler(request, exc)


async def unhandled_exception_handler(
    request: Request, exc: Exception  # pylint: disable=unused-argument
) -> PlainTextResponse:
    """
    Unhandled exceptions
    """
    host = getattr(getattr(request, "client", None), "host", None)
    port = getattr(getattr(request, "client", None), "port", None)
    url = (
        f"{request.url.path}?{request.query_params}"
        if request.query_params
        else request.url.path
    )
    exception_type, exception_value, _ = sys.exc_info()
    exception_name = getattr(exception_type, "__name__", None)
    file_logger.error(  # pylint: disable=W1203
        f"{host}:{port} - {request.method} {url}"
        f" 500 Internal Server Error <{exception_name}: {exception_value}>",
        exc_info=True,
    )
    return PlainTextResponse("Somthing Went Wrong", status_code=500)