from fastapi import Path
import logging
import app.api.v1.models as api_models
import app.controllers.tasks as tasks

from app.api.v1.words import router


log = logging.getLogger()


@router.delete(
    '/{words_id}',
    responses=api_models.ErrorResponses
)
def delete_words_result(
    words_id: str = Path(
        None,
        description='words ID',
        example='0ed49234-2069-4bf1-955b-124df445dc24'
    ),
):
    """
    Delete result of `POST /words`.

    If the task is still running then kill it.
    """
    tasks.delete(words_id)
