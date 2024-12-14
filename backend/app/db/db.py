from typing import Any

from starlette.requests import Request


def get_db(request: Request) -> Any:
    return request.state.db
