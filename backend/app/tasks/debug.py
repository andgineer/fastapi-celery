from typing import Any

from app.celery_app import celery_app
from app.tasks.base import ErrorLoggingTask
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


def dummy_function() -> int:
    return 33


@celery_app.task(name="tasks.dummy", base=ErrorLoggingTask, acks_late=True)  # type: ignore
def dummy_task() -> Any:  # Celery serializes result
    """
    To check celery worker test infrastructure
    """
    logger.info(">>> dummy_task <<<")
    return dummy_function()


@celery_app.task(  # type: ignore
    name="tasks.create_test_task",
    base=ErrorLoggingTask,
    acks_late=True,
)
def create_test_task(total: int) -> None:
    import time

    import numpy as np

    for i in range(total):
        logger.info(f"{i}")
        celery_app.current_task.update_state(
            state="PROGRESS",
            meta={"current": i, "total": total},
        )
        if np.random.uniform(0, 1) > 0.5:
            time.sleep(1)

    celery_app.current_task.update_state(
        state="SUCCESS",
        meta={"current": total, "total": total},
    )
