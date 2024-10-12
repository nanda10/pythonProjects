"""item service"""
import pytz
from datetime import datetime
from typing import Optional

from fastapi import Depends, APIRouter, status, Request, Response, Query
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse, JSONResponse

from clockin.db_config.models import ItemModel, UpdateItemModel
from clockin.stores.items import add_item, get_item_by_id, update_item_by_id, delete_item_by_id, get_items_by_filters, aggregate_for_items, check_item_exist
from clockin.schemas import ItemResponse, FilterItemResponse, AggregateItemResponse

item_route = APIRouter()

@item_route.post("", response_model=ItemResponse)
async def create_items(
    request: Request,
    _input: ItemModel
):
    """add item data to db"""
    await check_item_exist(request=request, item_data=jsonable_encoder(_input))
    IST = pytz.timezone('Asia/Kolkata')
    _input.insert_date = datetime.now(IST).strftime('%Y-%m-%d')
    item_data = jsonable_encoder(_input)
    item_details = await add_item(request=request, item_data=item_data)
    item_details["id_"] = str(item_details.pop("_id"))
    return JSONResponse(content=item_details, status_code=status.HTTP_201_CREATED)


@item_route.get("/filter", response_model=FilterItemResponse)
async def filter_items_with_query(
    request: Request,
    email: Optional[str] = None,
    expiry_date: Optional[datetime] = None,
    insert_date: Optional[datetime] = None,
    quantity: Optional[int] = None
):
    """filter data based on query params"""
    filters = {}
    if email:
        filters['email'] = email
    if expiry_date:
        filters['expiry_date'] = {"$gt": expiry_date.strftime('%Y-%m-%d')}
    if insert_date:
        filters['insert_date'] = {"$gt": insert_date.strftime('%Y-%m-%d')}
    if quantity:
        filters['quantity'] = {"$gte": quantity}

    if not filters:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Should give atleast one filter value")
    items_list = await get_items_by_filters(request=request, filters=filters)
    return dict(items=items_list, count=len(items_list))


@item_route.get("/email-count", response_model=AggregateItemResponse)
async def count_quantity_by_email(request: Request):
    """aggregate count and group by email"""
    pipeline = [
        {
            "$group": {
                "_id": "$email",
                "count": {"$sum": 1}
            }
        }
    ]
    item_data = await aggregate_for_items(request, pipeline)
    item_list = []
    for data in item_data:
        data["id_"] = data.pop("_id")
        item_list.append(data)
    return dict(group_by_email=item_list)


@item_route.get("/{item_id}", response_model=ItemResponse)
async def get_item_details(
    request: Request,
    item_id: str
):
    """get item by id"""
    item_details = await get_item_by_id(request=request, item_id=item_id)
    item_details["id_"] = str(item_details.pop("_id"))
    return item_details

# used patch instead of put because i am updating the data not replacing it
@item_route.patch("/{item_id}", response_model=ItemResponse)
async def update_item_details(
    request: Request,
    _input: UpdateItemModel,
    item_id: str
):
    """update item"""
    item_details = await get_item_by_id(request=request, item_id=item_id)
    update_item_data = jsonable_encoder(_input)
    await update_item_by_id(request=request, item_id=item_id, item_data=update_item_data)
    item_details["id_"] = str(item_details.pop("_id"))
    for key in update_item_data.keys():
        item_details[key] = update_item_data[key]
    return item_details


@item_route.delete("/{item_id}")
async def delete_item(
    request: Request,
    item_id: str
):
    """delete item by id"""
    deleted = await delete_item_by_id(request=request, item_id=item_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item with ID:{item_id} not found")
    return Response(status_code=204)
    