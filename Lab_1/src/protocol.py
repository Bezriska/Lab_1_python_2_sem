from typing import Protocol, runtime_checkable
from logger import logger

@runtime_checkable
class GetTasks(Protocol):
    """Protocol for task source implementations
    
    Any class implementing this protocol must provide a get_tasks() method
    that returns a list of task dictionaries
    """

    def get_tasks(self) -> list[dict]:
        """Returns a list of tasks
        
        Returns:
            list[dict]: List of task dictionaries with 'id' and 'payload' fields
        """
        pass

def get_all_tasks(gens: list[GetTasks]) -> list[dict]:
    """Collects all tasks from multiple task sources
    
    Args:
        gens (list[GetTasks]): List of objects implementing the GetTasks protocol
        
    Returns:
        list[dict]: Combined list of all tasks from all sources
        
    Raises:
        ValueError: If any object in gens does not implement the GetTasks protocol
    """
    final_tasks = []
    
    for gen in gens:
        
        if isinstance(gen, GetTasks):
            tasks = gen.get_tasks()
            
            for task in tasks:
                final_tasks.append(task)
        
        else:
            logger.error(f"Method get_tasks is not allowed for {gen}")
            raise ValueError(f"Method get_tasks is not allowed for {gen}")
        
    logger.debug("All tasks were successfully claimed")
    return final_tasks