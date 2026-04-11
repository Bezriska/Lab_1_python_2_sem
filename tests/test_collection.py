import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from collection import TaskQueue
from task.task import Task
# Для запуска тестов с покрытием: pytest tests/test_collection.py -v --cov=collection --cov-report=term-missing --import-mode=importlib


# Fixtures

@pytest.fixture
def empty_queue() -> TaskQueue:
    """Return an empty TaskQueue"""
    return TaskQueue()


@pytest.fixture
def queue_with_tasks() -> TaskQueue:
    """Return a TaskQueue with 5 tasks of different priorities and statuses"""
    queue = TaskQueue()
    queue.add_task(Task(1, "Fix bug", 2))
    queue.add_task(Task(2, "Write tests", 4))
    queue.add_task(Task(3, "Deploy", 5))
    queue.add_task(Task(4, "Code review", 1, "In_progress"))
    queue.add_task(Task(5, "Update docs", 3, "Completed"))
    return queue


# Tests: add_task

def test_add_task_increases_size(empty_queue: TaskQueue) -> None:
    """Adding tasks increases the number of items in the queue"""
    empty_queue.add_task(Task(1, "Task", 2))
    assert len(empty_queue.task_dict) == 1


def test_add_multiple_tasks(empty_queue: TaskQueue) -> None:
    """Multiple tasks are stored with sequential keys"""
    empty_queue.add_task(Task(1, "Task 1", 1))
    empty_queue.add_task(Task(2, "Task 2", 2))
    assert len(empty_queue.task_dict) == 2
    assert empty_queue.task_dict[1].description == "Task 1"
    assert empty_queue.task_dict[2].description == "Task 2"


# --- Tests: __iter__ ---

def test_iter_returns_all_tasks(queue_with_tasks: TaskQueue) -> None:
    """Iterating over queue yields all tasks"""
    tasks = list(queue_with_tasks)
    assert len(tasks) == 5


def test_iter_returns_task_objects(queue_with_tasks: TaskQueue) -> None:
    """Iteration yields Task instances"""
    for task in queue_with_tasks:
        assert isinstance(task, Task)


def test_iter_empty_queue(empty_queue: TaskQueue) -> None:
    """Iterating over empty queue yields no items"""
    assert list(empty_queue) == []


def test_iter_repeated(queue_with_tasks: TaskQueue) -> None:
    """Queue supports repeated iteration — each pass returns the same result"""
    first = [t.id for t in queue_with_tasks]
    second = [t.id for t in queue_with_tasks]
    assert first == second


def test_stop_iteration(queue_with_tasks: TaskQueue) -> None:
    """StopIteration is raised when iterator is exhausted"""
    iterator = iter(queue_with_tasks)
    collected = []
    try:
        while True:
            collected.append(next(iterator))
    except StopIteration:
        pass
    assert len(collected) == 5


# --- Tests: compatibility with builtins ---

def test_list_compatibility(queue_with_tasks: TaskQueue) -> None:
    """list() works with TaskQueue"""
    result = list(queue_with_tasks)
    assert len(result) == 5


def test_sum_compatibility(queue_with_tasks: TaskQueue) -> None:
    """sum() works with TaskQueue via generator expression"""
    total = sum(task.priority for task in queue_with_tasks)
    assert total == 2 + 4 + 5 + 1 + 3  # 15


def test_for_loop_compatibility(queue_with_tasks: TaskQueue) -> None:
    """for loop works with TaskQueue"""
    ids = []
    for task in queue_with_tasks:
        ids.append(task.id)
    assert ids == [1, 2, 3, 4, 5]


# --- Tests: filter by status ---

def test_filter_by_status_in_progress(queue_with_tasks: TaskQueue) -> None:
    """Filter by status returns only matching tasks"""
    result = list(queue_with_tasks.filter(status="In_progress"))
    assert len(result) == 1
    assert result[0].description == "Code review"


def test_filter_by_status_completed(queue_with_tasks: TaskQueue) -> None:
    """Filter by Completed status returns only completed tasks"""
    result = list(queue_with_tasks.filter(status="Completed"))
    assert len(result) == 1
    assert result[0].description == "Update docs"


def test_filter_by_status_created(queue_with_tasks: TaskQueue) -> None:
    """Filter by Created status returns all default tasks"""
    result = list(queue_with_tasks.filter(status="Created"))
    assert len(result) == 3


def test_filter_by_status_no_match(queue_with_tasks: TaskQueue) -> None:
    """Filter returns empty result when no task matches status"""
    result = list(queue_with_tasks.filter(status="Completed"))
    for task in result:
        assert task.status == "Completed"


# --- Tests: filter by high_priority ---

def test_filter_high_priority(queue_with_tasks: TaskQueue) -> None:
    """Filter by high_priority returns tasks with priority >= 3"""
    result = list(queue_with_tasks.filter(high_priority=True))
    assert len(result) == 3
    for task in result:
        assert task.priority >= 3


def test_filter_high_priority_is_lazy(queue_with_tasks: TaskQueue) -> None:
    """filter() returns a generator, not a list"""
    import types
    result = queue_with_tasks.filter(high_priority=True)
    assert isinstance(result, types.GeneratorType)


# Tests: filter by exact priority

def test_filter_by_exact_priority(queue_with_tasks: TaskQueue) -> None:
    """Filter by priority returns tasks with exact priority value"""
    result = list(queue_with_tasks.filter(priority=4))
    assert len(result) == 1
    assert result[0].description == "Write tests"


def test_filter_by_priority_no_match(queue_with_tasks: TaskQueue) -> None:
    """Filter by priority with no matches returns empty result"""
    result = list(queue_with_tasks.filter(priority=0))
    assert result == []


# Tests: filter validation
def test_filter_no_args_raises(queue_with_tasks: TaskQueue) -> None:
    """Calling filter() without arguments raises ValueError"""
    with pytest.raises(ValueError):
        list(queue_with_tasks.filter())


def test_filter_two_args_raises(queue_with_tasks: TaskQueue) -> None:
    """Calling filter() with two arguments raises ValueError"""
    with pytest.raises(ValueError):
        list(queue_with_tasks.filter(status="Created", high_priority=True))


def test_filter_status_and_priority_raises(queue_with_tasks: TaskQueue) -> None:
    """Calling filter() with status and priority raises ValueError"""
    with pytest.raises(ValueError):
        list(queue_with_tasks.filter(status="Created", priority=2))


def test_filter_high_priority_and_priority_raises(queue_with_tasks: TaskQueue) -> None:
    """Calling filter() with high_priority and priority raises ValueError"""
    with pytest.raises(ValueError):
        list(queue_with_tasks.filter(high_priority=True, priority=2))
