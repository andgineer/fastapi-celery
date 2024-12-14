import inspect
import logging
from typing import Any

from celery import Task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


class ErrorLoggingTask(Task):  # pylint: disable=abstract-method
    def on_success(self, retval: Any, task_id: str, args: Any, kwargs: Any) -> None:
        """Success handler.

        Run by the worker if the tasks executes successfully.

        Arguments:
            retval: The return value of the tasks.
            task_id: Unique id of the executed tasks.
            args: Original arguments for the executed tasks.
            kwargs: Original keyword arguments for the executed tasks.

        Returns:
            None: The return value of this handler is ignored.
        """
        if inspect.currentframe():
            logger.info(
                f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}"
            )
        logger.info(f"retval: {retval}")
        logger.info(f"task_id: {task_id}")
        logger.info(f"args: {args}")
        logger.info(f"kwargs: {kwargs}")

    def on_retry(self, exc, task_id, args, kwargs, einfo):  # pylint: disable=too-many-positional-arguments
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
        logger.info(
            f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}"
        )
        logger.info(f"task_id: {task_id}")
        logger.info(f"args: {args}")
        logger.info(f"kwargs: {kwargs}")
        logger.info(f"einfo: {einfo}")

    def on_failure(self, exc, task_id, args, kwargs, einfo):  # pylint: disable=too-many-positional-arguments
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
        logger.error(
            f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}"
        )
        logger.error(f"task_id: {task_id}")
        logger.error(f"args: {args}")
        logger.error(f"einfo: {einfo}")
        if logger.isEnabledFor(logging.DEBUG):
            kwargs["exc_info"] = exc
        super().on_failure(exc, task_id, args, kwargs, einfo)
