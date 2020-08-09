import celery.result
from app.celery_app import celery_app
import celery.result
from app.config import get_config
from typing import Optional


class TasksDatabase:
    """
    Celery does not track tasks status and if we want to distinguish
    between unknown task and task waiting for processing we have to store
    that information outside of Celery.
    """

    def __init__(self):
        self.tasks_hash = 'celery_task_ids'
        self.redis = get_config().redis

    def create(self, task_id: str):
        self.redis.hincrby(self.tasks_hash, task_id)

    def exists(self, task_id: str):
        return self.redis.hexists(self.tasks_hash, task_id)

    def delete(self, task_id: str):
        self.redis.hdel(self.tasks_hash, task_id)


tasks_db = TasksDatabase()


def send(*args, **kwargs) -> str:
    """
    Send task.
    Pass args to celery's send_task

    Returns task id
    """
    task: celery.result.AsyncResult = celery_app.send_task(*args, **kwargs)
    tasks_db.create(task.id)
    return task.id


def get(task_id: str) -> Optional[dict]:
    """
    If task does not exists raise exception.
    If task finished return task result.
    Else return None
    """
    if tasks_db.exists(task_id):
        task: celery.result.AsyncResult = celery_app.AsyncResult(task_id)
        if not task.ready():
            return None
        else:
            return task.result
    else:
        raise ValueError(f'No such task {task_id}')


def delete(task_id: str):
    if tasks_db.exists(task_id):
        task: celery.result.AsyncResult = celery_app.AsyncResult(task_id)
        task.revoke(terminate=True)
        task.forget()
        tasks_db.delete(task_id)
    else:
        raise ValueError(f'No such task {task_id}')
