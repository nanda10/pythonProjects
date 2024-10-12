"""main.py"""
from fastapi import FastAPI, APIRouter, Depends
from fastapi.exceptions import RequestValidationError, HTTPException
from pymongo import MongoClient

from clockin.services.item_service import item_route
from clockin.services.clockin_service import clockin_route
from clockin.utils.common_utils import strict_query_params
from clockin.globals import DB_URL, DB_NAME

from clockin.logs.exception_handler import (
    request_validation_exception_handler,
    http_exception_handler,
    unhandled_exception_handler,
)

app = FastAPI(
    responses={404: {"description": "Not Found"}},
    dependencies=[Depends(strict_query_params)],
)

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)

base_router = APIRouter(prefix="/api/v1")
base_router.include_router(item_route, prefix="/items")
base_router.include_router(clockin_route, prefix="/clock-in")

app.include_router(base_router)

@app.on_event("startup")
def startup_db_client():
    app.client = MongoClient(DB_URL)
    app.database = app.client[DB_NAME]


@app.on_event("shutdown")
def shutdown_db_client():
    app.client.close()