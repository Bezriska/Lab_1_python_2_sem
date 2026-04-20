from __future__ import annotations
from typing import Generator, Optional
from task.task import Task
import asyncio


class TaskQueue:
    """Collection of tasks based on dict"""

    def __init__(self) -> None:
        """Initialize empty task queue"""
        self.task_queue = asyncio.Queue()

    async def add_task(self, task: Task) -> None:
        """Add task to queue

        Args:
            task (Task): task to add
        """
        await self.task_queue.put(task)

    async def get_task(self) -> Task:
        """Remove and return the next task from the queue

        Returns:
            Task: next task in the queue
        """
        return await self.task_queue.get()

    def task_done(self) -> None:
        """Mark the last retrieved task as processed"""
        self.task_queue.task_done()

    def is_empty(self) -> bool:
        """Check whether the queue has no tasks

        Returns:
            bool: True if queue is empty, False otherwise
        """
        return self.task_queue.empty()

    def size(self) -> int:
        """Return the number of tasks currently in the queue

        Returns:
            int: number of tasks in the queue
        """
        return self.task_queue.qsize()


    # def filter(
    #     self,
    #     *,
    #     status: Optional[str] = None,
    #     high_priority: Optional[bool] = None,
    #     priority: Optional[int] = None
    # ) -> Generator[Task, None, None]:
    #     """Lazy filter for tasks — accepts exactly one filter argument

    #     Args:
    #         status (str, optional): filter tasks by status value
    #         high_priority (bool, optional): filter tasks with priority >= 3
    #         priority (int, optional): filter tasks by exact priority value

    #     Raises:
    #         ValueError: raised when zero or more than one filter is provided

    #     Yields:
    #         Task: task matching the filter condition
    #     """
    #     if status is None and high_priority is None and priority is None:
    #         raise ValueError("Choose one filter")
        
    #     if sum([status is not None, high_priority is not None, priority is not None]) > 1:
    #         raise ValueError("Choose one filter")

    #     if status:
    #         for task in self:
    #             if task.status == status:
    #                 yield task

    #     if high_priority:
    #         for task in self:
    #             if task.priority >= 3:
    #                 yield task

    #     if priority:
    #         for task in self:
    #             if task.priority == priority:
    #                 yield task
        

        

            




