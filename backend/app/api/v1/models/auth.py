from typing import List

from pydantic import BaseModel


class Token(BaseModel):  # type: ignore
    token: str
    type: str


class TokenData(BaseModel):  # type: ignore
    user_group: str = None
    scopes: List[str] = []


class Credentials(BaseModel):  # type: ignore
    login: str
    password: str
