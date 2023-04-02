from pydantic import BaseModel, root_validator, Field
from typing import Optional
from models.helpers import PydanticObjectId

class User(BaseModel):
    __collection_name__: str = 'user'
    id: Optional[PydanticObjectId] = Field(None, alias='_id')
    email: str
    password: bytes

    @classmethod
    def get_collection_name(cls):
        return cls.__collection_name__
    