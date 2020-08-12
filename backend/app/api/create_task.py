from typing import List
import app.controllers.tasks as tasks
from starlette.requests import Request
from starlette.responses import Response
from fastapi import status


def create_task(task_name: str, task_args: List, request: Request, response: Response):
    """
    Create task and return the task id in `Location` header with 303 status code.
    """
    task_id = tasks.send(
        task_name,
        args=task_args
    )
    response.status_code = status.HTTP_303_SEE_OTHER
    response.headers['Location'] = f'{request.url.path}/{task_id}'
