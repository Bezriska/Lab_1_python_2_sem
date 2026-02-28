from generators import ApiGen, MachineGen, JsonGen
from protocol import GetTasks, get_all_tasks
import os

api_gen = ApiGen()
machine_gen = MachineGen(10)
json_gen = JsonGen(f"{os.path.dirname(os.path.dirname(__file__))}/DATA/tasks.json")

# print(get_all_tasks([ApiGen, MachineGen, JsonGen]))
print(get_all_tasks([api_gen, machine_gen, json_gen]))