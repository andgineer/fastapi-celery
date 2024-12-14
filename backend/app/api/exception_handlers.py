import logging
from pprint import pformat
from typing import Callable, Any

import sqlalchemy.exc
import sqlalchemy.orm.exc
from app.api.v1.models import GeneralErrorResponse
from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

log = logging.getLogger()


async def unhandled_exception_middleware(
    request: Request, call_next: Callable[[Any], Any]
) -> JSONResponse:
    try:
        return await call_next(request)  # type: ignore
    except Exception as e:
        log.error(f"Unhandled exception {e}")
        # todo for some app it is not secure to reveal unhandled exception to client
        return JSONResponse(
            content=GeneralErrorResponse(message=str(e)).dict(),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def general_exception_handler(
    request: Request,  # pylint: disable=unused-argument
    exc: Exception,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=GeneralErrorResponse(message=str(exc)).dict(),
    )


async def validation_exception_handler(
    request: Request,  # pylint: disable=unused-argument
    exc: RequestValidationError,
) -> JSONResponse:
    message = f"{pformat(exc.errors())}\n{pformat(exc.body)}"
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=GeneralErrorResponse(message=message).dict(),
    )


async def db_exception_handler(
    request: Request,  # pylint: disable=unused-argument
    exc: sqlalchemy.exc.IntegrityError,
) -> JSONResponse:
    detail = str(exc).split("DETAIL:")[1].split("\n")[0]
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=GeneralErrorResponse(message=f"DB integrity error: {detail}").dict(),
    )


async def db_not_found_exception_handler(
    request: Request,  # pylint: disable=unused-argument
    exc: sqlalchemy.orm.exc.NoResultFound,  # pylint: disable=unused-argument
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=GeneralErrorResponse(message="Not found").dict(),
    )
