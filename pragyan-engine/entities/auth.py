from pydantic import BaseModel
from typing import Union


class User(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str


class RegisterUser(User):
    password: str


class AuthToken(BaseModel):
    access_token: str
    token_type: str


class AuthTokenData(BaseModel):
    username: Union[str, None]
