from itertools import chain
from typing import Optional

from app.api.get_task import get_task
from app.api.v1 import models as api_models
from app.api.v1.words import router
from fastapi import Path
from starlette import status
from starlette.responses import Response


@router.get(  # type: ignore
    "/{words_id}",
    responses=dict(
        chain(
            api_models.ErrorResponses.items(),
            {
                status.HTTP_202_ACCEPTED: {"description": "Results are not ready yet."},
                status.HTTP_200_OK: {"description": "Results."},
            }.items(),
        )
    ),
)
def words_result(
    words_id: str = Path(
        ..., description="words ID", example="0ed49234-2069-4bf1-955b-124df445dc24"
    ),
    response: Response = None,  # type: ignore
) -> Optional[api_models.Words]:
    """
    Returns result of `POST /words`.

    When the result is not yet ready returns `202` response.
    """
    results = get_task(words_id, response=response)
    return api_models.Words(count=results) if results is not None else response
