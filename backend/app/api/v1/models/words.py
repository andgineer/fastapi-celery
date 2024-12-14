from pydantic import BaseModel


class Words(BaseModel):  # type: ignore
    count: int
