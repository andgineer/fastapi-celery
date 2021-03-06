import logging
import time
from unittest.mock import patch

import app.tasks.debug

log = logging.getLogger()


@patch("app.tasks.debug.dummy_function")
def test_celery_boilerplate_task_direct(
    function_mock, celery_session_worker, celery_session_app
):
    """
    Shows how to test celery tasks with test worker
    """
    function_mock.return_value = 44
    assert app.tasks.debug.dummy_task.delay().get(timeout=10) == 44
    function_mock.assert_called()


@patch("app.tasks.debug.dummy_function")
def test_celery_boilerplate_send_task(
    function_mock, celery_session_worker, celery_session_app
):
    """
    Shows how to test full celery loop - sending and executing task
    """
    function_mock.return_value = 44
    task_id = celery_session_app.send_task("tasks.dummy")
    task = celery_session_app.AsyncResult(id=task_id)
    while task.state == "PENDING":
        log.info("Waiting for task..")
        time.sleep(0.3)
    function_mock.assert_called()
    assert task.result == 44
