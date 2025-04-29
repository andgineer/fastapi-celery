import logging

import app.api.v1.models as api_models
from app.api.v1.words import router
from app.controllers import tasks
from fastapi import Path

log = logging.getLogger()


@router.delete("/{words_id}", responses=api_models.ErrorResponses)  # type: ignore
def delete_words_result(
    words_id: str = Path(
        ...,
        description="words ID",
        example="0ed49234-2069-4bf1-955b-124df445dc24",
    ),
) -> None:
    """
    Delete result of `POST /words`.

    If the task is still running then kill it.
    """
    tasks.delete(words_id)
