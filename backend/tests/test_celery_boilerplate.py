import logging
import time

import app.tasks.debug
import celery.result

log = logging.getLogger()


def test_celery_boilerplate_send_task(celery_worker, celery_app, monkeypatch):
    """
    Shows how to test full celery loop - sending and executing task
    """
    # todo: if we patch in both tests it does not work
    monkeypatch.setattr(app.tasks.debug, "dummy_function", lambda: 33)
    celery_worker.reload(reload=True)
    result: celery.result.AsyncResult = celery_app.send_task("tasks.dummy")
    task = celery_app.AsyncResult(id=result.id)
    while task.state == "PENDING":
        log.info("Waiting for task..")
        time.sleep(0.3)
    assert task.result == 33


def test_celery_boilerplate_task_direct(celery_worker, celery_app, monkeypatch):
    """
    Shows how to test celery tasks with test worker
    """
    monkeypatch.setattr(app.tasks.debug, "dummy_function", lambda: 44)
    assert app.tasks.debug.dummy_task.delay().get(timeout=10) == 44
