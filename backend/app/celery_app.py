"""
Celery worker main and celery_app for tasks sender.

Register all tasks from app/tasks
"""
import os.path
from typing import List

import app.config as app_config  # to not shadow global app var with FastAPI app
from celery import Celery
from fastapi.logger import logger
from kombu.exceptions import OperationalError

mq_uri = app_config.get_config().mq_uri
logger.info(f"amqp_uri: {mq_uri}")


class Config:
    """
    https://docs.celeryproject.org/en/latest/userguide/configuration.html#configuration-and-defaults
    """

    task_acks_late = True  # guarantee task completion but the task may be executed twice
    # if the worker crashes mid execution
    result_expires = (
        600  # A built-in periodic task will delete the results after this time (seconds)
    )
    # assuming that celery beat is enabled. The task runs daily at 4am.
    # task_ignore_result = True  # now we control this per task
    task_compression = "gzip"
    result_compression = "gzip"
    broker_connection_retry = True
    broker_connection_retry_on_startup = True


def get_task_packages(path: str) -> List[str]:
    result = []
    for dirpath, dirnames, filenames in os.walk(path):
        for name in filenames:
            if "__" not in dirpath:  # exclude __pycache__
                result.append(
                    os.path.join(dirpath, name.split(".")[0]).replace("/", ".").replace("\\", ".")
                )
    return result


try:
    celery_app = Celery(
        "celery",
        backend=app_config.get_config().celery_backend_uri,
        broker=app_config.get_config().celery_broker_uri,
        include=get_task_packages(os.path.join("app", "tasks")),
    )
    celery_app.config_from_object(Config)
    celery_app.connection().ensure_connection(max_retries=3, timeout=15)
    print(f">>> celery_app: {app_config.get_config().celery_backend_uri}, {app_config.get_config().celery_broker_uri}")
except OperationalError:
    raise RuntimeError(
        f"Connection to {app_config.get_config().celery_broker_uri} broker refused."
    )

logger.info(f"Connection to {mq_uri} established.")

celery_app.conf.task_default_queue = "main-queue"


if __name__ == "__main__":
    celery_app.worker_main()
