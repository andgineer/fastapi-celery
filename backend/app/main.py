"""
Backend main
Starts FASTAPI app
"""

import logging
from typing import Any, Callable

import app.config as app_config  # to not shadow global app var with FastAPI app
import app.db.session as app_session
import sqlalchemy.exc
import sqlalchemy.orm.exc
from app.api.exception_handlers import (
    db_exception_handler,
    db_not_found_exception_handler,
    general_exception_handler,
    unhandled_exception_middleware,
    validation_exception_handler,
)
from app.api.routing import TAGS, router
from app.config import API_V1_STR
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request

log = logging.getLogger()


app = FastAPI(
    title="FastAPI service template",
    openapi_tags=TAGS,
    description="[API summary](https://example.com)",
    version="1.0.0",
    exception_handlers={
        Exception: general_exception_handler,
        RequestValidationError: validation_exception_handler,
        sqlalchemy.exc.IntegrityError: db_exception_handler,
        sqlalchemy.orm.exc.NoResultFound: db_not_found_exception_handler,
    },
)
app.middleware("http")(unhandled_exception_middleware)
app.include_router(router, prefix=API_V1_STR)


@app.middleware("http")
async def db_session_middleware(
    request: Request,
    call_next: Callable[[Request], Any],
) -> Any:
    """
    Opens DB session for each API request
    """
    try:
        request.state.db = app_session.get_session(app_config.get_config())
        response = await call_next(request)
    except Exception as e:
        logging.exception(f"Cannot get session in middleware: {e}")
        raise
    finally:
        request.state.db.close()
    return response


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
