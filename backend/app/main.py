"""
Backend main
Starts FASTAPI app
"""
from fastapi import FastAPI
import sqlalchemy.exc
import sqlalchemy.orm.exc
from starlette.requests import Request
import logging

from app.api.routing import router, TAGS
from app.api.exception_handlers import (db_exception_handler, general_exception_handler,
                                        db_not_found_exception_handler)
import app.config as app_config  # to not shadow global app var with FastAPI app
from app.db.session import get_session
from app.config import API_V1_STR


log = logging.getLogger()



app = FastAPI(
    title="FastAPI service template",
    openapi_tags=TAGS,
    description="[API summary](https://example.com)",
    version="1.0.0",
    exception_handlers={
        Exception: general_exception_handler,
        sqlalchemy.exc.IntegrityError: db_exception_handler,
        sqlalchemy.orm.exc.NoResultFound: db_not_found_exception_handler
    },
)

app.include_router(router, prefix=API_V1_STR)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    """
    Opens DB session for each API request
    """
    try:
        try:
            request.state.db = get_session(app_config.get_config())
        except Exception as e:
            logging.exception(f'Cannot get session in middleware: {e}')
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
