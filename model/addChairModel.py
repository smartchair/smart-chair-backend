from pydantic import BaseModel


class AddChairModel(BaseModel):
    chairId: str
    nickname: str

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls,v):
        if not isinstance(v,AddChairModel):
            raise TypeError("AddChairModel required")
        return []

