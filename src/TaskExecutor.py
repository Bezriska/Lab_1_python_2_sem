from __future__ import annotations
from types import TracebackType
from typing import Optional, Type
from handler import TaskHandler
from async_queue import TaskQueue
from logger import logger


class TaskExecutor:
    """Async task executor that processes tasks from a queue using a handler"""

    def __init__(self, handler: TaskHandler, queue: TaskQueue) -> None:
        """Initialize executor with a handler and a queue

        Args:
            handler (TaskHandler): handler that processes tasks
            queue (TaskQueue): queue to take tasks from
        """
        self.queue = queue
        self.handler = handler

    async def __aenter__(self) -> TaskExecutor:
        """Start the executor and log the event

        Returns:
            TaskExecutor: self
        """
        logger.info("\nTask executor started\n")
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> None:
        """Wait for all tasks to finish and log completion

        Args:
            exc_type: type of exception if raised, else None
            exc: exception instance if raised, else None
            tb: traceback if exception raised, else None
        """
        await self.queue.task_queue.join()
        if not exc:
            logger.info("Task executor finished without errors")
        else:
            logger.info(f"Task executor finished with error: {exc}")

    async def execute(self) -> None:
        """Process all tasks from the queue until it is empty"""
        while not self.queue.is_empty():
            task = await self.queue.get_task()
            try:
                await self.handler.handle(task)
                logger.info(f"Task {task} processed successfully")
            except Exception as e:
                await self.handler.on_error(task, e)
                logger.error(f"Error processing task {task}: {e}")
            finally:
                self.queue.task_done()
                logger.info("Task marked as done")
