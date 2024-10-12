"""clockin service"""
import pytz
from datetime import datetime
from typing import Optional

from fastapi import Depends, APIRouter, status, Request, Response, Query
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse, JSONResponse

from clockin.db_config.models import ClockinModel, UpdateClockinModel
from clockin.stores.clockin import add_clockin, update_clockin_by_id, get_clockin_by_id, delete_clockin_by_id, get_clockin_by_filters, check_clockin_exist
from clockin.utils.common_utils import is_valid_location
from clockin.schemas import ClockinResponse, FilterClockinResponse


clockin_route = APIRouter()

@clockin_route.post("", response_model=ClockinResponse)
async def create_clockin(
    request: Request,
    _input: ClockinModel
):
    """add clockin data to db"""
    await check_clockin_exist(request=request, clockin_data=jsonable_encoder(_input))
    IST = pytz.timezone('Asia/Kolkata')
    _input.insert_datetime = datetime.now(IST)
    clockin_data = jsonable_encoder(_input)
    clockin_details = await add_clockin(request=request, clockin_data=clockin_data)
    clockin_details["id_"] = str(clockin_details.pop("_id"))
    return clockin_details


@clockin_route.get("/filter", response_model=FilterClockinResponse)
async def filter_clockin_with_query(
    request: Request,
    email: Optional[str] = None,
    insert_date: Optional[datetime] = None,
    location: Optional[str] = Depends(is_valid_location)
):
    """filter data based on query params"""
    filters = {}
    if email:
        filters['email'] = email
    if insert_date:
        filters['insert_date'] = {"$gt": insert_date.strftime('%Y-%m-%d')}
    if location:
        filters['location'] = location

    if not filters:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Should give atleast one filter value")
    clockin_list = await get_clockin_by_filters(request=request, filters=filters)
    return dict(clockins=clockin_list, count=len(clockin_list))


@clockin_route.get("/{clockin_id}", response_model=ClockinResponse)
async def get_clockin_details(
    request: Request,
    clockin_id: str
):
    """get data using id"""
    clockin_details = await get_clockin_by_id(request=request, clockin_id=clockin_id)
    clockin_details["id_"] = str(clockin_details.pop("_id"))
    return clockin_details

# used patch instead of put because i am updating the data not replacing it
@clockin_route.patch("/{clockin_id}", response_model=ClockinResponse)
async def update_clockin_details(
    request: Request,
    clockin_id: str,
    _input: UpdateClockinModel
):
    """update clockin (insert_datetime is excluded)"""
    clockin_details = await get_clockin_by_id(request=request, clockin_id=clockin_id)
    update_clockin_data = jsonable_encoder(_input)
    await update_clockin_by_id(request=request, clockin_id=clockin_id, clockin_data=update_clockin_data)
    clockin_details["id_"] = str(clockin_details.pop("_id"))
    for key in update_clockin_data.keys():
        clockin_details[key] = update_clockin_data[key]
    return clockin_details

@clockin_route.delete("/{clockin_id}")
async def delete_clockin(
    request: Request,
    clockin_id: str
):
    """delete data by id"""
    deleted = await delete_clockin_by_id(request=request, clockin_id=clockin_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item with ID:{clockin_id} not found")
    return Response(status_code=204)