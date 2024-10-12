"""schemas.py"""
from datetime import date, datetime
from typing import Literal, List, Dict, Union
from pydantic import BaseModel, EmailStr


class ItemResponse(BaseModel):
    id_: str
    name: str
    email: EmailStr
    item_name: str
    quantity: int
    expiry_date: date
    insert_date: date

class FilterItemResponse(BaseModel):
    items: List[ItemResponse]
    count: int

class EmailCount(BaseModel):
    id_: EmailStr
    count: int

class AggregateItemResponse(BaseModel):
    group_by_email: List[EmailCount]

class ClockinResponse(BaseModel):
    id_: str
    email: EmailStr
    location: Literal["ASIA", "AFRICA", "AUSTRALIA", "ANTARTICA", "EUROPE", "NORTH AMERICA", "SOUTH AMERICA"]
    insert_datetime: datetime

class FilterClockinResponse(BaseModel):
    clockins: List[ClockinResponse]
    count: int