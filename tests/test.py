import os
import sys
import pytest
import asyncio

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from task.task import Task
from async_queue import TaskQueue
from handler import LogHandler, EmailHandler
from TaskExecutor import TaskExecutor

# Запуск тестов с покрытием: .venv/bin/pytest tests/test.py -v --cov=src --cov-report=term-missing --import-mode=importlib

# Fixtures

def make_task(id: int = 1, desc: str = "Test task", priority: int = 3) -> Task:
    return Task(id, desc, priority)


# TaskQueue tests

@pytest.mark.asyncio
async def test_queue_starts_empty():
    queue = TaskQueue()
    assert queue.is_empty()
    assert queue.size() == 0


@pytest.mark.asyncio
async def test_queue_add_task_increases_size():
    queue = TaskQueue()
    await queue.add_task(make_task())
    assert queue.size() == 1
    assert not queue.is_empty()


@pytest.mark.asyncio
async def test_queue_get_task_returns_correct_task():
    queue = TaskQueue()
    task = make_task(id=5, desc="My task", priority=4)
    await queue.add_task(task)
    result = await queue.get_task()
    assert result is task


@pytest.mark.asyncio
async def test_queue_preserves_fifo_order():
    queue = TaskQueue()
    task1 = make_task(id=1)
    task2 = make_task(id=2)
    await queue.add_task(task1)
    await queue.add_task(task2)
    assert await queue.get_task() is task1
    assert await queue.get_task() is task2


@pytest.mark.asyncio
async def test_queue_task_done_after_get():
    queue = TaskQueue()
    await queue.add_task(make_task())
    await queue.get_task()
    queue.task_done()


@pytest.mark.asyncio
async def test_queue_size_after_multiple_adds():
    queue = TaskQueue()
    for i in range(5):
        await queue.add_task(make_task(id=i))
    assert queue.size() == 5


# LogHandler tests

@pytest.mark.asyncio
async def test_log_handler_handle_does_not_raise():
    handler = LogHandler()
    task = make_task()
    await handler.handle(task)


@pytest.mark.asyncio
async def test_log_handler_on_error_does_not_raise():
    handler = LogHandler()
    task = make_task()
    await handler.on_error(task, ValueError("test error"))


# TaskExecutor tests

@pytest.mark.asyncio
async def test_executor_processes_all_tasks():
    queue = TaskQueue()
    processed = []

    class RecordingHandler:
        async def handle(self, task: Task) -> None:
            processed.append(task)

        async def on_error(self, task: Task, exception: Exception) -> None:
            pass

    for i in range(3):
        await queue.add_task(make_task(id=i))

    async with TaskExecutor(RecordingHandler(), queue) as executor:
        await executor.execute()

    assert len(processed) == 3


@pytest.mark.asyncio
async def test_executor_queue_empty_after_execute():
    queue = TaskQueue()
    await queue.add_task(make_task())

    async with TaskExecutor(LogHandler(), queue) as executor:
        await executor.execute()

    assert queue.is_empty()


@pytest.mark.asyncio
async def test_executor_calls_on_error_on_exception():
    queue = TaskQueue()
    errors = []

    class FailingHandler:
        async def handle(self, task: Task) -> None:
            raise RuntimeError("handle failed")

        async def on_error(self, task: Task, exception: Exception) -> None:
            errors.append((task, exception))

    await queue.add_task(make_task())

    async with TaskExecutor(FailingHandler(), queue) as executor:
        await executor.execute()

    assert len(errors) == 1
    assert isinstance(errors[0][1], RuntimeError)


@pytest.mark.asyncio
async def test_executor_context_manager_enter_returns_executor():
    queue = TaskQueue()
    handler = LogHandler()
    async with TaskExecutor(handler, queue) as executor:
        assert isinstance(executor, TaskExecutor)


@pytest.mark.asyncio
async def test_executor_empty_queue_does_nothing():
    queue = TaskQueue()
    processed = []

    class RecordingHandler:
        async def handle(self, task: Task) -> None:
            processed.append(task)

        async def on_error(self, task: Task, exception: Exception) -> None:
            pass

    async with TaskExecutor(RecordingHandler(), queue) as executor:
        await executor.execute()

    assert processed == []
