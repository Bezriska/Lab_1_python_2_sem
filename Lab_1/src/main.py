from .generators import ApiGen, MachineGen, JsonGen
from .protocol import get_all_tasks
import os

api_gen = ApiGen()
machine_gen = MachineGen(10)
json_gen = JsonGen(f"{os.path.dirname(os.path.dirname(__file__))}/DATA/tasks.json")

print("Collecting tasks...\n")

all_tasks = get_all_tasks([api_gen, machine_gen, json_gen])

print("Tasks:\n")

for task in all_tasks:
    if "generated" in task["payload"]:
        print(f"Task from MachineGen: {task}")
    elif "api" in task["payload"]:
        print(f"Task from api: {task}")
    elif "json" in task["payload"]:
        print(f"Task from json: {task}")
    else:
        print(f"Unknown task: {task}")

print("\nAll tasks successfully collected")
        