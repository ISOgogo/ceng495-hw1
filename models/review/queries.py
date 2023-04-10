from models.base_queries import BaseQueryOps
from typing import List, Optional
from pymongo.client_session import ClientSession
from pymongo.database import Database
from models.base_queries import BaseQueryOps
from models.review.base import Review

class ReviewQueryOps(BaseQueryOps):
    def __init__(self, db: Database, session: Optional[ClientSession] = None):
        super().__init__(db, Review, session)