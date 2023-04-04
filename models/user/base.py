from pydantic import BaseModel, root_validator, Field
from typing import Optional
from models.helpers import PydanticObjectId
from pymongo.database import Database
from pymongo.errors import CollectionInvalid
import bcrypt
import os

class User(BaseModel):
    __collection_name__: str = 'user'
    id: Optional[PydanticObjectId] = Field(None, alias='_id')
    email: str
    username: str
    password: bytes

    @classmethod
    def get_collection_name(cls):
        return cls.__collection_name__

    def create_collection(db: Database):
        try:
            db.create_collection("user", {})
        except CollectionInvalid:  # collection already exists
            pass
        # Make unique indexes
        db.user.create_index("username", unique=True)
        db.user.create_index("email", unique=True)
        db.user.insert_one({ "email":"admin@mail.com", # Create admin user
                             "username":"admin", 
                             # TODO: os.environ.get("ADMIN_PASS")
                             "password": bcrypt.hashpw("very-strong-password".encode("utf-8"), bcrypt.gensalt())
                            })
    