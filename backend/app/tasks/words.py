import celery.app.task
import celery.exceptions
import celery.states
from celery.utils.log import get_task_logger

from app.celery_app import celery_app
from app.controllers.words import count_words
from app.tasks.base import ErrorLoggingTask
from app.tasks.states import TaskStates

logger = get_task_logger(__name__)


@celery_app.task(
    name="tasks.words",
    base=ErrorLoggingTask,
    bind=True,
    throws=(celery.exceptions.InvalidTaskError, ValueError)
)
def words(
        self: celery.app.task.Task, text: str
) -> int:
    """
    Count words
    """
    logger.info(f'>>> tasks.words {str(self.request.id)} started <<<')
    try:
        try:
            self.update_state(state=TaskStates.PROGRESS)
            result = count_words(text)
            logger.info(f'>>> tasks.words {str(self.request.id)} finished <<<')
            return result
        except Exception as e:
            raise celery.exceptions.InvalidTaskError(str(e))
    except Exception as e:
        self.update_state(state=celery.states.FAILURE)
        raise e
