from typing import Optional, Any

from bson import ObjectId
from pydantic import BaseModel, Field

from model.PyObjectIdClass import PyObjectId


class UserInfo(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    email: str
    password: str
    chairsId: Any

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
