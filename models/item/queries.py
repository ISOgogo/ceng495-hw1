from models.base_queries import BaseQueryOps
from typing import List, Optional
from pymongo.client_session import ClientSession
from pymongo.database import Database
from models.base_queries import BaseQueryOps
from models.item.base import Item
from modules.schema import CreateItemParams

class ItemQueryOps(BaseQueryOps):
    def __init__(self, db: Database, session: Optional[ClientSession] = None):
        super().__init__(db, Item, session)
    
    def get_by_name(self, name: str) -> Optional[Item]:
        result =  self.collection.find_one({"name": name})
        return self.model.parse_obj(result)
    
    def update_with_params(self, create_item_params: CreateItemParams):
        item = self.get_by_name(create_item_params.name)
        item = item.update_fields(create_item_params.dict())
        self.update(item)

    def delete_by_name(self, name:str):
        self.collection.delete_one({"name": name})