import logging
import time
from unittest.mock import patch

import celery.result

import app.tasks.debug


log = logging.getLogger()


# todo: flaky uses unpatched task
# def test_celery_boilerplate_send_task(celery_worker, celery_app):
#     """
#     Shows how to test full celery loop - sending and executing task
#     """
#     with patch("app.tasks.debug.dummy_function", return_value=55):
#         celery_worker.reload()
#         result: celery.result.AsyncResult = celery_app.send_task("tasks.dummy")
#         task = celery_app.AsyncResult(id=result.id)
#         while task.state == "PENDING":
#             log.info("Waiting for task..")
#             time.sleep(0.3)
#         assert task.result == 55


def test_celery_boilerplate_task_direct(celery_worker, celery_app):
    """
    Shows how to test celery tasks with test worker
    """
    with patch("app.tasks.debug.dummy_function", return_value=44):
        celery_worker.reload()
        assert app.tasks.debug.dummy_task.delay().get(timeout=10) == 44

