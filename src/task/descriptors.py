from .exceptions import PriorityError, StatusError


class TypeDescriptor:
    """Data-descriptor for validation type"""
    
    def __init__(self, type):
        self.type = type

    def __set_name__(self, owner, name):
        self.name = name

    def __set__(self, instance, value):
        if not isinstance(value, self.type):
            raise TypeError(f"Expected type: {self.type.__name__}")
        else:
            instance.__dict__[self.name] = value

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)
    

class PriorityDescriptor:
    """Data-descriptor for validation priority value"""

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)
    
    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError(f"Expected str type, your type: {type(value).__name__}")
        
        if not 0 <= value < 6:
            raise PriorityError(f"Priority must be in range: 0-5. Input priority: {value}")
        
        instance.__dict__[self.name] = value


class StatusDescriptor:
    """Data-descriptor for validation task status"""

    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)
    
    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise TypeError(f"Expected str type, your type: {type(value).__name__}")
        
        if value not in ("Created", "In_progress", "Completed"):
            raise StatusError(f"Status must be 'Created', 'In_progress' or 'Completed'. Your status: {value}")
        
        instance.__dict__[self.name] = value


class CreatedAtDescriptor:
    """Non-data Descriptor for creation time"""

    def __set_name__(self, owner, name):
        self.name = f"_{name}"

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)
    
        
        


        
