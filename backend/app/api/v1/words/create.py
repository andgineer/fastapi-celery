from fastapi import UploadFile, File
from starlette import status
from starlette.requests import Request
from starlette.responses import Response
from app.api.v1 import models as api_models

from app.api.v1.words import router
import app.controllers.tasks as tasks


@router.post(
    '',
    status_code=status.HTTP_303_SEE_OTHER,
    responses=api_models.ErrorResponses
)
async def create_words_count_task(
    text: UploadFile = File(
        ..., description="Text"
    ),
    request: Request = None,
    response: Response = None,
) -> None:
    """
    Calculates number of words in the text.

    Works asynchronously - reply with 303 status code and `Location` HTTP header which points to url
    like GET /words/{id} where the result will be available after processing.
    """
    task_id = tasks.send(
        'tasks.words',
        args=[(await text.read()).decode()]
    )
    response.status_code = status.HTTP_303_SEE_OTHER
    response.headers['Location'] = f'{request.url.path}/{task_id}'
