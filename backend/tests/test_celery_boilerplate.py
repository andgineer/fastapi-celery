import logging
import time
from unittest.mock import patch

import celery.result

import app.tasks.debug


log = logging.getLogger()


def test_celery_boilerplate_send_task(celery_session_worker, celery_session_app):
    """
    Shows how to test full celery loop - sending and executing task
    """
    with patch("backend.app.tasks.debug.dummy_function", return_value=55):
        result: celery.result.AsyncResult = celery_session_app.send_task("tasks.dummy")
        task = celery_session_app.AsyncResult(id=result.id)
        while task.state == "PENDING":
            log.info("Waiting for task..")
            time.sleep(0.3)
        assert task.result == 55


def test_celery_boilerplate_task_direct(celery_session_worker, celery_session_app):
    """
    Shows how to test celery tasks with test worker
    """
    with patch("backend.app.tasks.debug.dummy_function", return_value=44):
        assert app.tasks.debug.dummy_task.delay().get(timeout=10) == 44
