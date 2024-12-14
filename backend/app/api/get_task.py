import app.controllers.tasks as tasks
from fastapi import status
from starlette.responses import Response


def get_task(task_id: str, response: Response) -> None:
    """
    Set response status code to 202 if task in process and 500 if it failed.

    Returns task results if there are any, or None.
    """
    try:
        results = tasks.get(task_id)
        if isinstance(results, Exception):
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return None
        elif results is None:
            response.status_code = status.HTTP_202_ACCEPTED
        return results
    except Exception:
        response.status_code = status.HTTP_404_NOT_FOUND
    return None
