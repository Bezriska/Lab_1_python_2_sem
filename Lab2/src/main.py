from task import Task
from exceptions import PriorityError, StatusError
from time import sleep

task = Task(1, "Hello", 2)

try:
    task.description = 12
except TypeError as t:
    print("Error has catched while changing description")
    print(t)
    print("\n")

try:
    task.priority = 10
except PriorityError as p:
    print("Error has catched while changing priority")
    print(p)
    print("\n")

try:
    task.status = "Error"
except StatusError as s:
    print("Error has catched while changing status")
    print(s)
    print("\n")

if task.is_ready:
    print("Task is ready")
else:
    print("Task is not ready")

sleep(5)


print("\n")
print("Time from creation task:")
print(task.time_from_creation)
print("\nTask created at:")
task.show_creation_time()


