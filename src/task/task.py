from .descriptors import TypeDescriptor, PriorityDescriptor, StatusDescriptor, CreatedAtDescriptor
import datetime


class Task:
    """Class for task object with id, description, priority, status and timestamp

    Returns:
        Task: task for your app
    """
    id = TypeDescriptor(int)
    description = TypeDescriptor(str)
    priority = PriorityDescriptor()
    status = StatusDescriptor()
    _created_at = CreatedAtDescriptor()

    def __init__(self, id: int, description: str, priority: int, status: str = "Created") -> None:
        """Initialize task with given fields

        Args:
            id (int): unique task identifier
            description (str): task description
            priority (int): task priority in range 0-5
            status (str): task status, defaults to 'Created'
        """
        self.id = id
        self.description = description
        self.priority = priority
        self.status = status
        self._created_at = datetime.datetime.now().replace(microsecond=0)

    @property
    def is_ready(self) -> bool:
        """Check if task is ready to be processed

        Returns:
            bool: True when status is 'Created', priority > 0 and id is set
        """
        return self.status == "Created" and self.priority > 0 and self.id

    
    @property
    def time_from_creation(self) -> datetime.timedelta:
        """Calculate time elapsed since task creation

        Returns:
            datetime.timedelta: time elapsed since creation
        """
        return datetime.datetime.now().replace(microsecond=0) - self._created_at
    
    def show_creation_time(self) -> None:
        """Print task creation time to stdout"""
        print(self._created_at)


    def __repr__(self) -> str:
        """Return string representation of task

        Returns:
            str: human-readable task representation
        """
        return f"Task(id: {self.id}, description: {self.description}, priority: {self.priority}, status: {self.status}, created_at: {self._created_at})"

