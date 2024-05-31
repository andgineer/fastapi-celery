"""
celery test config
should be imported into `conftest.py`
"""
import os.path

import pytest
from app.celery_app import get_task_packages

print(">>> celery fixtures are importing <<<")


@pytest.fixture(scope="session")
def celery_config():
    """
    Setup Celery test app configuration (for fixture celery_app)
    https://docs.celeryproject.org/en/stable/userguide/testing.html
    """
    print(">>> celery_config <<<")
    return {
        "broker_url": "memory://localhost//",
        "result_backend": "cache+memory://",
        "task_always_eager": True,
        "broker_connection_retry_on_startup": True,
        "task_ignore_result": False,
    }


@pytest.fixture(scope="session")
def celery_worker_parameters():
    """
    Setup Celery worker parameters
    https://docs.celeryproject.org/en/stable/userguide/testing.html
    """
    print(">>> celery_worker_parameters <<<")
    return {
        "queues": ("main-queue", "celery"),
        "loglevel": "INFO",
        "without_heartbeat": True,
    }


@pytest.fixture(scope="session", autouse=True)
def celery_enable_logging():
    """
    Enable logging in embedded workers
    https://docs.celeryproject.org/en/stable/userguide/testing.html
    """
    return True


@pytest.fixture(scope="session")
def celery_includes():
    """
    Add additional imports for embedded workers
    https://docs.celeryproject.org/en/stable/userguide/testing.html
    """
    return get_task_packages(os.path.join("backend", "app", "tasks"))


@pytest.fixture(scope="session")
def use_celery_app_trap():
    """
    Raise exception on falling back to default app
    https://docs.celeryproject.org/en/stable/userguide/testing.html
    """
    return True
