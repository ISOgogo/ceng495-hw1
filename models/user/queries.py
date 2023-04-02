from models.base_queries import BaseQueryOps
from typing import List, Optional
from pymongo.client_session import ClientSession
from pymongo.database import Database
from models.base_queries import BaseQueryOps
from models.user.base import User
from custom_errors import UserNotFound

class UserQueryOps(BaseQueryOps):
    def __init__(self, db: Database, session: Optional[ClientSession] = None):
        super().__init__(db, User, session)

    def get_by_email(self, email: str) -> User:
        result = self.collection.find_one({'email': email})
        try:
            return User.parse_obj(result)
        except:
            raise UserNotFound