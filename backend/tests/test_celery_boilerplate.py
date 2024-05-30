import logging
import time
from unittest.mock import patch

import celery.result
import pytest

import app.tasks.debug


log = logging.getLogger()


@pytest.fixture(scope="session", autouse=True)
def mock_dummy_function(request):
    """
    Patch the dummy_function in the app.tasks.debug module before the
    Celery worker is started.
    """
    if request.param in [44, 55]:
        with patch("backend.app.tasks.debug.dummy_function", return_value=request.param):
            yield
    else:
        yield


@pytest.mark.parametrize("mock_dummy_function", [55], indirect=True)
def test_celery_boilerplate_send_task(mock_dummy_function, celery_worker, celery_app):
    """
    Shows how to test full celery loop - sending and executing task
    """
    result: celery.result.AsyncResult = celery_app.send_task("tasks.dummy")
    task = celery_app.AsyncResult(id=result.id)
    while task.state == "PENDING":
        log.info("Waiting for task..")
        time.sleep(0.3)
    assert task.result == 55


@pytest.mark.parametrize("mock_dummy_function", [44], indirect=True)
def test_celery_boilerplate_task_direct(mock_dummy_function, celery_worker, celery_app):
    """
    Shows how to test celery tasks with test worker
    """
    assert app.tasks.debug.dummy_task.delay().get(timeout=10) == 44

