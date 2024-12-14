from pydantic import BaseModel


class Words(BaseModel):
    count: int
