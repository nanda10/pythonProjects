"""item stores"""
from bson import ObjectId
from fastapi import status, Request
from fastapi.exceptions import HTTPException

from clockin.db_config.utils import transactional

@transactional
async def add_item(request, item_data, _session):
    """add data"""
    created_item = request.app.database["items"].insert_one(item_data, session=_session)
    return await read_item(request, created_item.inserted_id, _session)

@transactional
async def get_item_by_id(request, item_id, _session):
    """get clockin by id"""
    if item := await read_item(request, ObjectId(item_id), _session):
        return item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item with ID:{item_id} not found")

@transactional
async def update_item_by_id(request, item_id, item_data, _session):
    """update data"""
    updated_item = request.app.database["items"].update_one(
        {"_id": ObjectId(item_id)}, {"$set": item_data}, session=_session
    )
    return updated_item

@transactional
async def delete_item_by_id(request, item_id, _session):
    """delete clockin by id"""
    deleted_item = request.app.database["items"].delete_one({"_id":ObjectId(item_id)}, session=_session)
    return deleted_item.deleted_count

@transactional
async def get_items_by_filters(request, filters, _session):
    """filter data"""
    result = request.app.database["items"].find(filters)
    if result:
        item_list = []
        for item in result:
            item["id_"] = str(item["_id"])
            item_list.append(item)
        return item_list

async def aggregate_for_items(request, pipeline):
    """aggregate"""
    return request.app.database["items"].aggregate(pipeline)

@transactional
async def check_item_exist(request, item_data, _session):
    """check if item exist"""
    item_data.pop("insert_date")
    if exist := request.app.database["items"].find_one(item_data, session=_session):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Data already exist. You may update the existing value")

async def read_item(request, id_, _session):
    """read data"""
    return request.app.database["items"].find_one({"_id": id_}, session=_session)
