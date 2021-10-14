import sqlalchemy.exc
import sqlalchemy.orm.exc
from app.api.v1.models import GeneralErrorResponse
from fastapi import Request
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pprint import pformat
import logging


log = logging.getLogger()


async def unhandled_exception_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        log.error(f"Unhandled exception {e}")
        # todo for some app it is not secure to reveal unhandled exception to client
        return JSONResponse(
            content=GeneralErrorResponse(message=str(e)).dict(),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=GeneralErrorResponse(message=str(exc)).dict(),
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    message = f"{pformat(exc.errors())}\n{pformat(exc.body)}"
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=GeneralErrorResponsemessage(message=message).dict(),
    )


async def db_exception_handler(request: Request, exc: sqlalchemy.exc.IntegrityError):
    detail = str(exc).split("DETAIL:")[1].split("\n")[0]
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=GeneralErrorResponse(message=f"DB integrity error: {detail}").dict(),
    )


async def db_not_found_exception_handler(
    request: Request, exc: sqlalchemy.orm.exc.NoResultFound
):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=GeneralErrorResponse(message="Not found").dict(),
    )
