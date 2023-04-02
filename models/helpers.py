from bson import ObjectId

class PydanticObjectId(ObjectId):
    """
    ObjectId not directly supported by pydantic. So this class will help us both
    serialization and validation
    """

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")