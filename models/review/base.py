from pydantic import root_validator, Field
from typing import Optional
from models.helpers import PydanticObjectId, MongoBaseModel
from pymongo.database import Database
from pymongo.errors import CollectionInvalid

class Review(MongoBaseModel):
    __collection_name__: str = 'item'
    id: Optional[PydanticObjectId] = Field(None, alias='_id')
    user: str
    item: str
    review: str

    @classmethod
    def get_collection_name(cls):
        return cls.__collection_name__

def create_collection(db: Database):
    try:
        db.create_collection("review", {})
    except CollectionInvalid:  # collection already exists
        pass
    # Make unique indexes
    db.user.create_index("user", unique=False)
    db.user.create_index("item", unique=False)
