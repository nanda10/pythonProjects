"""models used to for payload validation"""
import pytz
from typing import Optional, Literal
from datetime import date, datetime
from pydantic import BaseModel, EmailStr, constr, conint, validator


class ItemModel(BaseModel):
    name: constr(pattern=r'^[a-zA-Z]+$', min_length=2, max_length=20)
    email: EmailStr
    item_name: constr(pattern=r'^[a-zA-Z]+$', min_length=2, max_length=20)
    quantity: conint(ge=1)
    expiry_date: date
    insert_date: date = None

    @validator("expiry_date")
    @classmethod
    def validate_expiry_date(cls, expiry_date):
        """validate expiry date"""
        IST = pytz.timezone('Asia/Kolkata')
        current_date = datetime.now(IST).strftime('%Y-%m-%d')
        if current_date > str(expiry_date):
            raise ValueError("Please specify a date that is beyond the current date.")
        return expiry_date


class UpdateItemModel(BaseModel):
    name: Optional[constr(pattern=r'^[a-zA-Z]+$', min_length=2, max_length=20)]
    email: Optional[EmailStr]
    item_name: Optional[constr(pattern=r'^[a-zA-Z]+$', min_length=2, max_length=20)]
    quantity: Optional[conint(ge=1)]
    expiry_date: Optional[date]

    @validator("expiry_date")
    @classmethod
    def validate_expiry_date(cls, expiry_date):
        """validate expiry date"""
        if not expiry_date:
            return
        IST = pytz.timezone('Asia/Kolkata')
        current_date = datetime.now(IST).strftime('%Y-%m-%d')
        if current_date > str(expiry_date):
            raise ValueError("Please specify a date that is beyond the current date.")
        return expiry_date


class ClockinModel(BaseModel):
    email: EmailStr
    location: Literal["ASIA", "AFRICA", "AUSTRALIA", "ANTARTICA", "EUROPE", "NORTH AMERICA", "SOUTH AMERICA"]
    insert_datetime: datetime = None


class UpdateClockinModel(BaseModel):
    email: Optional[EmailStr]
    location: Optional[Literal["ASIA", "AFRICA", "AUSTRALIA", "ANTARTICA", "EUROPE", "NORTH AMERICA", "SOUTH AMERICA"]]
