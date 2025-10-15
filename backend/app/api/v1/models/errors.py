from typing import Any

from pydantic import BaseModel


class GeneralErrorResponse(BaseModel):
    message: str


class ValidationErrorResponse(BaseModel):
    """
    Pydantic params validation error
    """

    detail: dict[str, Any]


ErrorResponses = {
    400: {"model": GeneralErrorResponse},
    401: {"model": GeneralErrorResponse},
    404: {"model": GeneralErrorResponse},
    422: {"model": ValidationErrorResponse},
}
