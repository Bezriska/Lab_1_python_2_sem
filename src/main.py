from collection import TaskQueue
from task.task import Task


queue = TaskQueue()

task1 = Task(1, "Fix bug", 2)
task2 = Task(2, "Write tests", 4)
task3 = Task(3, "Deploy", 5)
task4 = Task(4, "Code review", 1, "In_progress")
task5 = Task(5, "Update docs", 3, "Completed")

for task in [task1, task2, task3, task4, task5]:
    queue.add_task(task)



print("=== 1. Iterating over queue ===")
for task in queue:
    print(f"  [{task.id}] {task.description} | priority={task.priority} | status={task.status}")


print("\n=== 2. Repeated iteration ===")
first_pass = [task.id for task in queue]
second_pass = [task.id for task in queue]
print(f"  First pass:  {first_pass}")
print(f"  Second pass: {second_pass}")
print(f"  Equal: {first_pass == second_pass}")


print("\n=== 3. StopIteration demonstration ===")
iterator = iter(queue)
try:
    while True:
        task = next(iterator)
        print(f"  Got: {task.description}")
except StopIteration:
    print("  Queue exhausted — StopIteration raised")


print("\n=== 4. Lazy filter by status='In_progress' ===")
for task in queue.filter(status="In_progress"):
    print(f"  [{task.id}] {task.description}")


print("\n=== 5. Lazy filter by high_priority ===")
for task in queue.filter(high_priority=True):
    print(f"  [{task.id}] {task.description} | priority={task.priority}")


print("\n=== 6. Compatibility with list(), sum(), for ===")
all_tasks = list(queue)
print(f"  list(queue) -> {len(all_tasks)} tasks")

total_priority = sum(task.priority for task in queue)
print(f"  sum of priorities -> {total_priority}")

count_ready = sum(1 for task in queue if task.is_ready)
print(f"  ready tasks count -> {count_ready}")


print("\n=== 7. ValueError on wrong filter ===")
try:
    list(queue.filter())
except ValueError as e:
    print(f"  No filter: {e}")

try:
    list(queue.filter(status="Created", high_priority=True))
except ValueError as e:
    print(f"  Two filters: {e}")
