from pydantic import root_validator, BaseModel
from custom_errors import *
import re
import bcrypt

class AuthRegisterParams(BaseModel):
    email: str
    password: bytes

    @root_validator(pre=True)
    def check(cls, values):
        if values['email'] is None or values['email'] == "":
            raise EmptyEmailError('Email cannot be empty')
        if values['password'] is None or values['password'] == "":
            raise EmptyPasswordError('Password cannot be empty')
        # validate and lower the email
        values['email'] = check_email(values['email'])
        if not is_valid_password(values['password']):
            raise InvalidPassword('Password is invalid')
        # Hash the password
        values['password'] = bcrypt.hashpw(values['password'].encode('utf-8'), bcrypt.gensalt())
        return values

class AuthLoginParams(BaseModel):
    email: str
    password: bytes

    @root_validator(pre=True)
    def check(cls, values):
        if values['email'] is None or values['email'] == "":
            raise EmptyEmailError('Email cannot be empty')
        if values['password'] is None or values['password'] == "":
            raise EmptyPasswordError('Password cannot be empty')
        # Turn into bytes
        values['password'] = values['password'].encode('utf-8')
        return values


def check_email(email):
    email = email.strip()
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.fullmatch(regex, email):
        return email.lower()
    raise InvalidEmail('Invalid email format.')

def is_valid_password(new_password: str):
    # password must be at least 6 characters
    if len(new_password) < 6:
        return False
    # password must contain at least 1 digit
    if not bool(re.search(r'\d', new_password)):
        return False
    # password must contain at least 1 character
    if not bool(re.search(r"[a-z]", new_password.lower())):
        return False
    return True
