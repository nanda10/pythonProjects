"""clockin store"""
from bson import ObjectId
from fastapi import status, Request
from fastapi.exceptions import HTTPException

from clockin.db_config.utils import transactional


@transactional
async def add_clockin(request, clockin_data, _session):
    """insert data"""
    created_clockin = request.app.database["user_clockin_record"].insert_one(clockin_data, session=_session)
    return await read_clockin(request, created_clockin.inserted_id, _session)

@transactional
async def get_clockin_by_id(request, clockin_id, _session):
    """get data by id"""
    if clockin := await read_clockin(request, ObjectId(clockin_id), _session):
        return clockin
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item with ID:{clockin_id} not found")

@transactional
async def update_clockin_by_id(request, clockin_id, clockin_data, _session):
    """update data"""
    updated_clockin = request.app.database["user_clockin_record"].update_one(
        {"_id": ObjectId(clockin_id)}, {"$set": clockin_data}, session=_session
    )
    return updated_clockin

@transactional
async def delete_clockin_by_id(request, clockin_id, _session):
    """delete data by id"""
    deleted_clockin = request.app.database["user_clockin_record"].delete_one(
        {"_id": ObjectId(clockin_id)}, session=_session
    )
    return deleted_clockin.deleted_count

@transactional
async def get_clockin_by_filters(request, filters, _session):
    """filter data"""
    result = request.app.database["user_clockin_record"].find(filters)
    if result:
        clockin_list = []
        for clockin in result:
            clockin["id_"] = str(clockin["_id"])
            clockin_list.append(clockin)
        return clockin_list


@transactional
async def check_clockin_exist(request, clockin_data, _session):
    """check is item exist"""
    clockin_data.pop("insert_datetime")
    if exist := request.app.database["user_clockin_record"].find_one(clockin_data, session=_session):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Data already exist. You may update the existing value")

async def read_clockin(request, clockin_id, _session):
    """get data"""
    return request.app.database["user_clockin_record"].find_one({"_id": clockin_id}, session=_session)