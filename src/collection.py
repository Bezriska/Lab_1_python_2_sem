from __future__ import annotations
from typing import Generator, Optional
from task.task import Task



class TaskQueue:
    """Collection of tasks based on dict"""

    def __init__(self) -> None:
        """Initialize empty task queue"""
        self.task_dict: dict[int, Task] = {}
        self.last_num: int = 1

    def __iter__(self) -> Generator[Task, None, None]:
        """Iterate over all tasks in queue

        Yields:
            Task: next task in queue
        """
        for task in self.task_dict.values():
            yield task

    def add_task(self, task: Task) -> None:
        """Add task to queue

        Args:
            task (Task): task to add
        """
        self.task_dict[self.last_num] = task
        self.last_num += 1


    def filter(
        self,
        *,
        status: Optional[str] = None,
        high_priority: Optional[bool] = None,
        priority: Optional[int] = None
    ) -> Generator[Task, None, None]:
        """Lazy filter for tasks — accepts exactly one filter argument

        Args:
            status (str, optional): filter tasks by status value
            high_priority (bool, optional): filter tasks with priority >= 3
            priority (int, optional): filter tasks by exact priority value

        Raises:
            ValueError: raised when zero or more than one filter is provided

        Yields:
            Task: task matching the filter condition
        """
        if status is None and high_priority is None and priority is None:
            raise ValueError("Choose one filter")
        
        if sum([status is not None, high_priority is not None, priority is not None]) > 1:
            raise ValueError("Choose one filter")

        if status:
            for task in self:
                if task.status == status:
                    yield task

        if high_priority:
            for task in self:
                if task.priority >= 3:
                    yield task

        if priority:
            for task in self:
                if task.priority == priority:
                    yield task
        

        

            




