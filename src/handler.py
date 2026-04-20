from typing import Protocol
from logger import logger
import asyncio
from task.task import Task


class TaskHandler(Protocol):
    """Protocol defining the interface for all task handlers"""

    async def handle(self, task: Task) -> None:
        """Process a single task

        Args:
            task (Task): task to process
        """
        ...

    async def on_error(self, task: Task, exception: Exception) -> None:
        """Handle an error that occurred during task processing

        Args:
            task (Task): task that caused the error
            exception (Exception): exception that was raised
        """
        ...


class LogHandler:
    """Handler that logs task processing via the logger"""

    async def handle(self, task: Task) -> None:
        """Log successful task processing

        Args:
            task (Task): task to log
        """
        logger.info(f"Task {task} logged")

    async def on_error(self, task: Task, exception: Exception) -> None:
        """Log an error that occurred during task processing

        Args:
            task (Task): task that caused the error
            exception (Exception): exception that was raised
        """
        logger.error(f"Error logging task {task}: {exception}")


class EmailHandler:
    """Handler that simulates sending tasks via email"""

    async def handle(self, task: Task) -> None:
        """Send task via email (simulated with delay)

        Args:
            task (Task): task to send
        """
        await asyncio.sleep(2)
        print(f"Task {task} sent via email")

    async def on_error(self, task: Task, exception: Exception) -> None:
        """Handle email sending error (simulated with delay)

        Args:
            task (Task): task that caused the error
            exception (Exception): exception that was raised
        """
        await asyncio.sleep(2)
        print(f"Error sending task {task} via email: {exception}")
