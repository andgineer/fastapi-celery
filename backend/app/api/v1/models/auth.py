from pydantic import BaseModel
from typing import List


class Token(BaseModel):
    token: str
    type: str


class TokenData(BaseModel):
    user_group: str = None
    scopes: List[str] = []


class Credentials(BaseModel):
    login: str
    password: str
