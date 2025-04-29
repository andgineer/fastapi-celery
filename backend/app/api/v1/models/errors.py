from typing import Any, Dict

from pydantic import BaseModel


class GeneralErrorResponse(BaseModel):
    message: str


class ValidationErrorResponse(BaseModel):
    """
    Pydantic params validation error
    """

    detail: Dict[str, Any]


ErrorResponses = {
    400: {"model": GeneralErrorResponse},
    401: {"model": GeneralErrorResponse},
    404: {"model": GeneralErrorResponse},
    422: {"model": ValidationErrorResponse},
}
