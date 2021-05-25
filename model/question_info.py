from typing import Optional, Any

from bson import ObjectId
from pydantic import BaseModel, Field

from model.PyObjectIdClass import PyObjectId


class Question(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    question: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }


class Answer(BaseModel):
    question_id: str
    answer: str
    user_id: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
