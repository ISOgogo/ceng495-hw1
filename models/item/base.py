from pydantic import root_validator, Field
from typing import Optional
from models.helpers import PydanticObjectId, MongoBaseModel
from pymongo.database import Database
from pymongo.errors import CollectionInvalid
from custom_errors import *
from modules.constants import *

class Item(MongoBaseModel):
    __collection_name__: str = 'item'
    id: Optional[PydanticObjectId] = Field(None, alias='_id')
    name: str
    description: str
    price: int
    seller: str
    image: str
    size: str
    colour: str
    spec: str
    category: str
    rating: float = 0
    reviews: list = Field(default_factory=list)

    @classmethod
    def get_collection_name(cls):
        return cls.__collection_name__

def create_collection(db: Database):
    try:
        db.create_collection("item", {})
    except CollectionInvalid:  # collection already exists
        pass
    # Make unique indexes
    db.user.create_index("name", unique=True)
    db.user.create_index("seller", unique=False)
