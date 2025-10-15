from app.controllers import tasks
from fastapi import status
from starlette.requests import Request
from starlette.responses import Response


def create_task(
    task_name: str,
    task_args: list[str],
    request: Request,
    response: Response,
) -> None:
    """
    Create task and return the task id in `Location` header with 303 status code.
    """
    task_id = tasks.send(task_name, args=task_args)
    response.status_code = status.HTTP_303_SEE_OTHER
    response.headers["Location"] = f"{request.url.path}/{task_id}"
