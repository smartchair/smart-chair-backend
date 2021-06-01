from bson import ObjectId
from pydantic import BaseModel


class AddChairModel(BaseModel):
    chairId: str
    nickname: str

    class Config:
        json_encoders = {
            ObjectId: str
        }
