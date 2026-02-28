from typing import Protocol, runtime_checkable

@runtime_checkable
class GetTasks(Protocol):

    def get_tasks(self) -> list:
        pass

def get_all_tasks(gens: list) -> list[dict]:
    final_tasks = []
    
    for gen in gens:
        
        if isinstance(gen, GetTasks):
            tasks = gen.get_tasks()
            
            for task in tasks:
                final_tasks.append(task)
            
        
        else:
            raise ValueError(f"Method get_tasks is not allowed for {gen}")
        
    return final_tasks
