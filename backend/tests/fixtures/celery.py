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
    return {"broker_url": "memory://", "result_backend": "rpc"}


@pytest.fixture(scope="session")
def celery_worker_parameters():
    """
    Setup Celery worker parameters
    https://docs.celeryproject.org/en/stable/userguide/testing.html
    """
    return {
        "queues": ("main-queue", "celery"),
        "loglevel": "INFO",
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
    return get_task_packages(os.path.join("app", "tasks"))


@pytest.fixture(scope="session")
def use_celery_app_trap():
    """
    Raise exception on falling back to default app
    https://docs.celeryproject.org/en/stable/userguide/testing.html
    """
    return True
