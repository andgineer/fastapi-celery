from typing import Dict, Any

from pydantic import BaseModel


class GeneralErrorResponse(BaseModel):  # type: ignore
    message: str


class ValidationErrorResponse(BaseModel):  # type: ignore
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
