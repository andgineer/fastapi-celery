import app.controllers.tasks as tasks
from starlette.responses import Response
from fastapi import status


def get_task(task_id: str, response: Response):
    """
    Set response status code to 202 if task in process and 500 if it failed.

    Returns task results if there are any, or None.
    """
    try:
        results = tasks.get(task_id)
        if results is None:
            response.status_code = status.HTTP_202_ACCEPTED
        elif isinstance(results, Exception):
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return None
        return results
    except Exception:
        response.status_code = status.HTTP_404_NOT_FOUND
    return None
