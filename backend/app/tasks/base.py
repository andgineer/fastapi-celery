import inspect
import logging

from celery import Task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


class ErrorLoggingTask(Task):
    def on_success(self, retval, task_id, args, kwargs):
        """Success handler.

        Run by the worker if the tasks executes successfully.

        Arguments:
            retval (Any): The return value of the tasks.
            task_id (str): Unique id of the executed tasks.
            args (Tuple): Original arguments for the executed tasks.
            kwargs (Dict): Original keyword arguments for the executed tasks.

        Returns:
            None: The return value of this handler is ignored.
        """
        logger.info(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}")
        logger.info(f"retval: {retval}")
        logger.info(f"task_id: {task_id}")
        logger.info(f"args: {args}")
        logger.info(f"kwargs: {kwargs}")

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        """Retry handler.

        This is run by the worker when the tasks is to be retried.

        Arguments:
            exc (Exception): The exception sent to :meth:`retry`.
            task_id (str): Unique id of the retried tasks.
            args (Tuple): Original arguments for the retried tasks.
            kwargs (Dict): Original keyword arguments for the retried tasks.
            einfo (~billiard.einfo.ExceptionInfo): Exception information.

        Returns:
            None: The return value of this handler is ignored.
        """
        logger.info(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}")
        logger.info(f"task_id: {task_id}")
        logger.info(f"args: {args}")
        logger.info(f"kwargs: {kwargs}")
        logger.info(f"einfo: {einfo}")

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """Error handler.

        This is run by the worker when the tasks fails.

        Arguments:
            exc (Exception): The exception raised by the tasks.
            task_id (str): Unique id of the failed tasks.
            args (Tuple): Original arguments for the tasks that failed.
            kwargs (Dict): Original keyword arguments for the tasks that failed.
            einfo (~billiard.einfo.ExceptionInfo): Exception information.

        Returns:
            None: The return value of this handler is ignored.
        """
        logger.error(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}")
        logger.error(f"task_id: {task_id}")
        logger.error(f"args: {args}")
        logger.error(f"einfo: {einfo}")
        if logger.isEnabledFor(logging.DEBUG):
            kwargs["exc_info"] = exc
        super().on_failure(exc, task_id, args, kwargs, einfo)
