import sqlalchemy.exc
import sqlalchemy.orm.exc
from app.api.v1.models import GeneralErrorResponse
from fastapi import Request
from fastapi import status
from fastapi.responses import JSONResponse


async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=GeneralErrorResponse(message=str(exc)).dict(),
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
