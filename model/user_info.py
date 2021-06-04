from typing import Optional, Any

from bson import ObjectId
from pydantic import BaseModel, Field

from model.PyObjectIdClass import PyObjectId


class UserInfo(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    email: str
    password: Any
    chairs: dict

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }


class UserLogin(BaseModel):
    username: str
    password: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }


class ChairIn(BaseModel):
    chairId: str
    chairNickname: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
