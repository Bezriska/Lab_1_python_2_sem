import asyncio
from async_queue import TaskQueue
from handler import LogHandler, EmailHandler
from TaskExecutor import TaskExecutor
from task.task import Task


async def main() -> None:
    print("  Async Task Executor — Demo")

    # Create tasks
    task1 = Task(1, "Send welcome email", priority=5)
    task2 = Task(2, "Generate monthly report", priority=3)
    task3 = Task(3, "Clean up temp files", priority=1)
    task4 = Task(4, "Backup database", priority=4)
    task5 = Task(5, "Notify admin", priority=2)

    # Demo 1: LogHandler
    print("\n[Demo 1] LogHandler — tasks are written to LOG.log")

    log_queue = TaskQueue()
    for task in [task1, task2, task3]:
        await log_queue.add_task(task)

    print(f"Queue size before execution: {log_queue.size()}")

    async with TaskExecutor(LogHandler(), log_queue) as executor:
        await executor.execute()

    print(f"Queue size after execution:  {log_queue.size()}")

    # Demo 2: EmailHandler
    print("\n[Demo 2] EmailHandler — tasks are sent via email (simulated)")

    email_queue = TaskQueue()
    for task in [task4, task5]:
        await email_queue.add_task(task)

    print(f"Queue size before execution: {email_queue.size()}")

    async with TaskExecutor(EmailHandler(), email_queue) as executor:
        await executor.execute()

    print(f"Queue size after execution:  {email_queue.size()}")

    # Demo 3: Error handling
    print("\n[Demo 3] Error handling — on_error is called when handle() raises")

    class BrokenHandler:
        async def handle(self, task: Task) -> None:
            raise ValueError(f"Cannot process task {task.id}")

        async def on_error(self, task: Task, exception: Exception) -> None:
            print(f"  [on_error] Caught error for task {task.id}: {exception}")

    error_queue = TaskQueue()
    await error_queue.add_task(Task(99, "Broken task", priority=2))

    async with TaskExecutor(BrokenHandler(), error_queue) as executor:
        await executor.execute()

    print("  Demo complete. Check LOG.log for log entries.")


asyncio.run(main())
