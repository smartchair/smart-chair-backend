from bson import ObjectId
from pydantic import BaseModel


class AddChairModel(BaseModel):
    chairId: str
    nickname: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
