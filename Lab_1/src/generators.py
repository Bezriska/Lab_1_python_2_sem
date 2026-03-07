import json
import os
from logger import logger


class MachineGen:
    """Generates tasks programmatically
    
    Attributes:
        count (int): Number of tasks to generate
    """
    def __init__(self, count) -> None:
        self.count = count

    def get_tasks(self) -> list[dict]:
        """Generates a list of tasks programmatically
        
        Returns:
            list[dict]: List of tasks with 'id' and 'payload' fields
        """
        logger.debug("Tasks from MachineGen were generated")
        return [{"id": i, "payload": f"generated-{i}"} for i in range(self.count)]
    

class JsonGen:
    """Collects tasks from a JSON file
    
    Attributes:
        path (str): Path to the JSON file containing tasks
    """
    def __init__(self, path) -> None:
        self.path = path

    def get_tasks(self) -> list[dict]:
        """Reads and returns tasks from a JSON file
        
        Returns:
            list[dict]: List of tasks loaded from the JSON file
            
        Raises:
            FileNotFoundError: If the specified file does not exist
        """

        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                data = json.load(f)
                logger.debug("Tasks from JsonGen were loaded")
            return data["tasks"]
        
        else:
            logger.error(f"File not found {self.path}")
            raise FileNotFoundError(f"File not found {self.path}")
        

class ApiGen:
    """Simulates an API request for tasks
    
    Generates mock API response data for testing purposes
    """
    def __init__(self):
        pass

    def get_tasks(self) -> list[dict]:
        """Simulates fetching tasks from an API
        
        Returns:
            list[dict]: List of tasks with 'id' and 'payload' fields simulating API response
        """
        logger.debug("Tasks from ApiGen were generated")
        return [{"id": f"{i}{i}{i}", "payload": f"api-{i}{i}{i}"} for i in range(10)]
