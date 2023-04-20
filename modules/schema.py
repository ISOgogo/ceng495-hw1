from pydantic import root_validator
from models.helpers import MongoBaseModel
from custom_errors import *
from modules.constants import *
import re

class CreateItemParams(MongoBaseModel):
    name: str
    description: str
    price: float
    seller: str
    image: str
    size: str
    colour: str
    spec: str
    category: str

    @root_validator(pre=True)
    def check(cls, values):
        try:
            values["price"] = float(values["price"])
            if values["price"] < 0: raise
        except:
            raise InvalidPrice
        if values["name"].strip() == "":
            raise InvalidName
        if values["category"] not in get_ctype_elems(ItemCategory):
            raise InvalidCategory
        if values.get("image"):
            if check_is_valid_url(values.get("image")) is False:
                raise InvalidUrl
        return values

def check_is_valid_url(url: str):
    url_pattern = re.compile(r'^https?://')
    return url_pattern.match(url)