from pydantic import BaseModel


class Token(BaseModel):
    token: str
    type: str


class TokenData(BaseModel):
    user_group: str | None = None
    scopes: list[str] = []


class Credentials(BaseModel):
    login: str
    password: str
