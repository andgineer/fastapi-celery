from app.api.create_task import create_task
from app.api.v1 import models as api_models
from app.api.v1.words import router
from fastapi import File, UploadFile
from starlette import status
from starlette.requests import Request
from starlette.responses import Response


@router.post("", status_code=status.HTTP_303_SEE_OTHER, responses=api_models.ErrorResponses)
async def create_words_count_task(
    text: UploadFile = File(..., description="Text"),
    request: Request = None,
    response: Response = None,
) -> None:
    """
    Calculates number of words in the text.

    Works asynchronously - reply with 303 status code and `Location` HTTP header which points to url
    like GET /words/{id} where the result will be available after processing.
    If it’s not ready yet the GET request will return 202 status code.
    """
    create_task(
        task_name="tasks.words",
        task_args=[(await text.read()).decode()],
        request=request,
        response=response,
    )
