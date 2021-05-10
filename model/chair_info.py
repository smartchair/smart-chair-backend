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

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
