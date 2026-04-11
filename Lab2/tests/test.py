import pytest # type: ignore
import sys
import os
import datetime
# Для теста с покрытием pytest tests/test.py -v --cov=src --cov-report=term-missing --import-mode=importlib

# Add src path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from task import Task # type: ignore
from exceptions import PriorityError, StatusError # type: ignore
from descriptors import TypeDescriptor, PriorityDescriptor, StatusDescriptor, CreatedAtDescriptor # type: ignore


# Tests for TypeDescriptor
def test_valid_type():
    """Test correct type validation"""
    task = Task(1, "Test task", 3)
    assert task.id == 1
    assert task.description == "Test task"


def test_invalid_type_id():
    """Test error when id has invalid type"""
    with pytest.raises(TypeError):
        Task("not_int", "Test", 2)


def test_invalid_type_description():
    """Test error when description has invalid type"""
    task = Task(1, "Valid", 2)
    with pytest.raises(TypeError):
        task.description = 123


# Tests for PriorityDescriptor
def test_valid_priority():
    """Test valid priority values"""
    for priority in range(0, 6):
        task = Task(1, "Test", priority)
        assert task.priority == priority


def test_invalid_priority_range_upper():
    """Test error when priority exceeds maximum value"""
    with pytest.raises(PriorityError):
        Task(1, "Test", 6)


def test_invalid_priority_range_lower():
    """Test error when priority is negative"""
    with pytest.raises(PriorityError):
        Task(1, "Test", -1)


def test_invalid_priority_type():
    """Test error when priority has invalid type"""
    with pytest.raises(TypeError):
        Task(1, "Test", "high")


# Tests for StatusDescriptor
def test_valid_statuses():
    """Test valid status values"""
    valid_statuses = ["Created", "In_progress", "Completed"]
    for status in valid_statuses:
        task = Task(1, "Test", 2, status)
        assert task.status == status


def test_invalid_status():
    """Test error when status is invalid"""
    with pytest.raises(StatusError):
        Task(1, "Test", 2, "Invalid")


def test_default_status():
    """Test default status value"""
    task = Task(1, "Test", 2)
    assert task.status == "Created"


# Tests for CreatedAtDescriptor (non-data descriptor)
def test_created_at_set_on_init():
    """Test creation time is set on initialization"""
    before = datetime.datetime.now().replace(microsecond=0)
    task = Task(1, "Test", 2)
    after = datetime.datetime.now().replace(microsecond=0)
    
    assert isinstance(task._created_at, datetime.datetime)
    assert task._created_at >= before
    assert task._created_at <= after


def test_non_data_descriptor_shadowing():
    """Test non-data descriptor shadowing"""
    task = Task(1, "Test", 2)
    original_time = task._created_at
    
    # Non-data descriptor allows shadowing
    task._created_at = "shadowed"
    assert task._created_at == "shadowed"
    assert task._created_at != original_time


# Tests for Task class
def test_task_creation():
    """Test task creation"""
    task = Task(1, "My task", 3, "Created")
    assert task.id == 1
    assert task.description == "My task"
    assert task.priority == 3
    assert task.status == "Created"


def test_is_ready_when_all_conditions_met():
    """Test is_ready when all conditions are met"""
    task = Task(1, "Test", 3, "Created")
    assert task.is_ready == True


def test_is_ready_when_priority_zero():
    """Test is_ready when priority is zero"""
    task = Task(1, "Test", 0, "Created")
    assert task.is_ready is False


def test_is_ready_when_status_not_created():
    """Test is_ready when status is not Created"""
    task = Task(1, "Test", 3, "In_progress")
    assert task.is_ready is False


def test_time_from_creation():
    """Test time calculation since creation"""
    task = Task(1, "Test", 2)
    time_delta = task.time_from_creation
    
    assert isinstance(time_delta, datetime.timedelta)
    assert time_delta.total_seconds() >= 0
    assert time_delta.total_seconds() < 1


# Tests to demonstrate difference between data and non-data descriptors
def test_data_descriptor_not_shadowed():
    """Data descriptors cannot be shadowed via assignment"""
    task = Task(1, "Test", 3)
    
    # Attempting invalid assignment triggers validation
    with pytest.raises(PriorityError):
        task.priority = 999


def test_non_data_descriptor_shadowed():
    """Non-data descriptors can be shadowed via __dict__"""
    task = Task(1, "Test", 3)
    original_time = task._created_at
    
    # Shadowing via __dict__
    task.__dict__['_created_at'] = "shadowed"
    assert task._created_at == "shadowed"
