import json
import os


class MachineGen:
    def __init__(self, count) -> None:
        self.count = count

    def get_tasks(self) -> list[dict]:
        return [{"id": i, "payload": f"generated-{i}"} for i in range(self.count)]
    

class JsonGen:
    def __init__(self, path) -> None:
        self.path = path

    def get_tasks(self) -> list[dict]:        
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                data = json.load(f)
            
            return data["tasks"]
        
        else:
            raise FileNotFoundError(f"File not found {self.path}")
        

class ApiGen:
    def __init__(self):
        pass

    def get_tasks(self):
        return [{"id": f"{i}{i}{i}", "payload": f"api-{i}{i}{i}"} for i in range(10)]

# gen = MachineGen(10)
# print(gen.get_tasks())


# gen1 = JsonGen(f"{os.path.dirname(os.path.dirname(__file__))}/DATA/tasks.json")
# print(gen1.get_tasks())


# gen2 = ApiGen()
# print(gen2.get_tasks())
