"""utils"""
from fastapi import Request, status
from fastapi.exceptions import HTTPException


async def strict_query_params(request: Request):
    """restrict unwanted query parameter"""
    dependant = request.scope["route"].dependant
    allowed_params = [
        param.alias
        for dependency in dependant.dependencies
        for param in dependency.query_params
    ]
    allowed_params += [modelfield.alias for modelfield in dependant.query_params]
    for requested_param in request.query_params.keys():
        if requested_param not in allowed_params:
            raise HTTPException(400, f"Unknown Query Parameter {requested_param}")
    return

async def is_valid_location(location = None):
    """check if location is valid"""
    LOCATION = ["ASIA", "AFRICA", "AUSTRALIA", "ANTARTICA", "EUROPE", "NORTH AMERICA", "SOUTH AMERICA"]
    if location and location not in LOCATION:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Given location query is not valid. Select from anyone of these: f{LOCATION}")
    return location