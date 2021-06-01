from typing import Optional, Any, List

from bson import ObjectId
from pydantic import BaseModel, Field

from model.PyObjectIdClass import PyObjectId


class UserInfo(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    email: str
    password: Any
    chairs: List

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
    userId: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }


class ChairModel(BaseModel):
    chairId: str
    chairNickname: str

    def create(self, Chair_in: ChairIn):
        self.chairId = Chair_in.chairId
        self.chairNickname = Chair_in.chairNickname

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
