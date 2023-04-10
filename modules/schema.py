from pydantic import root_validator
from models.helpers import MongoBaseModel
from custom_errors import *
from modules.constants import *
import re

class CreateItemParams(MongoBaseModel):
    name: str
    description: str
    price: int
    seller: str
    image: str
    size: str
    colour: str
    spec: str
    category: str

    @root_validator(pre=True)
    def check(cls, values):
        if int(values["price"]) < 0:
            raise InvalidPrice
        if values["name"].strip() == "":
            raise InvalidName
        if values["category"] not in get_ctype_elems(ItemCategory):
            raise InvalidCategory
        return values