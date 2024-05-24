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
    return {
        "broker_url": "memory://",
        "result_backend": "rpc://",
        "task_always_eager": False,
        "task_store_eager_results": True,
        "broker_connection_retry_on_startup": True,
        "task_ignore_result": False,
    }


@pytest.fixture(scope="session")
def celery_worker_parameters():
    """
    Setup Celery worker parameters
    https://docs.celeryproject.org/en/stable/userguide/testing.html
    """
    return {
        "queues": ("main-queue", "celery"),
        "loglevel": "DEBUG",
        "without_heartbeat": False,
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
    return get_task_packages(os.path.join(app_folder(), "tasks"))


def app_folder():
    """Backend app folder relative to pytest working dir.

    Tests can be run from the project root folder or from the backend/ folder.
    """
    return (
        "app"
        if os.path.isdir(os.path.join(os.getcwd(), "app"))
        else os.path.join("backend", "app")
    )


@pytest.fixture(scope="session")
def use_celery_app_trap():
    """
    Raise exception on falling back to default app
    https://docs.celeryproject.org/en/stable/userguide/testing.html
    """
    return True
