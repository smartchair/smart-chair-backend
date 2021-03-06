from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field

from model.PyObjectIdClass import PyObjectId


class ChairInfo(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    chairId: str
    temp: float
    presence: bool
    noise: float
    lum: float
    hum: float
    time: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }


class ChairInfoIn(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    chairId: str
    temp: float
    presence: bool
    noise: float
    lum: float
    hum: float

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }


class GetPropModel(BaseModel):
    day: str
    chairId: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }


class postLum(BaseModel):
    userId: str
    deviceType: str
    lum: float

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
