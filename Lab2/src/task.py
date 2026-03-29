from descriptors import TypeDescriptor, PriorityDescriptor, StatusDescriptor, CreatedAtDescriptor
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

    def __init__(self, id, description, priority, status="Created"):
        self.id = id
        self.description = description
        self.priority = priority
        self.status = status
        self._created_at = datetime.datetime.now().replace(microsecond=0)

    @property
    def is_ready(self):
        """Method for check is task ready or not

        Returns:
            bool: True, when all important fields are not none, else False
        """
        return self.status == "Created" and self.priority > 0 and self.id

    
    @property
    def time_from_creation(self):
        """Method for checking timedelta from creation

        Returns:
            datetime: Time since creation
        """
        return datetime.datetime.now().replace(microsecond=0) - self._created_at
    
    def show_creation_time(self):
        """Method for checking creation time

        Returns:
            datetime: when task was created
        """
        print(self._created_at)

