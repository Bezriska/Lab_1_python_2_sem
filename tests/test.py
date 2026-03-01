import pytest
import os
import json
import tempfile
from src.generators import MachineGen, ApiGen, JsonGen
from src.protocol import GetTasks, get_all_tasks


class TestMachineGen:
    """Tests for MachineGen class."""
    
    def test_machine_gen_creates_correct_count(self):
        """Test that MachineGen generates correct number of tasks."""
        gen = MachineGen(10)
        tasks = gen.get_tasks()
        assert len(tasks) == 10
    
    def test_machine_gen_task_structure(self):
        """Test that generated tasks have correct structure."""
        gen = MachineGen(5)
        tasks = gen.get_tasks()
        
        for i, task in enumerate(tasks):
            assert "id" in task
            assert "payload" in task
            assert task["id"] == i
            assert task["payload"] == f"generated-{i}"
    
    def test_machine_gen_empty(self):
        """Test MachineGen with zero tasks."""
        gen = MachineGen(0)
        tasks = gen.get_tasks()
        assert len(tasks) == 0
    
    def test_machine_gen_implements_protocol(self):
        """Test that MachineGen implements GetTasks protocol."""
        gen = MachineGen(5)
        assert isinstance(gen, GetTasks)


class TestJsonGen:
    """Tests for JsonGen class."""
    
    def test_json_gen_reads_file(self):
        """Test that JsonGen correctly reads tasks from JSON file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({"tasks": [{"id": "1", "payload": "test-1"}]}, f)
            temp_path = f.name
        
        try:
            gen = JsonGen(temp_path)
            tasks = gen.get_tasks()
            assert len(tasks) == 1
            assert tasks[0]["id"] == "1"
            assert tasks[0]["payload"] == "test-1"
        finally:
            os.unlink(temp_path)
    
    def test_json_gen_file_not_found(self):
        """Test that JsonGen raises FileNotFoundError for non-existent file."""
        gen = JsonGen("/non/existent/path/file.json")
        with pytest.raises(FileNotFoundError):
            gen.get_tasks()
    
    def test_json_gen_implements_protocol(self):
        """Test that JsonGen implements GetTasks protocol."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({"tasks": []}, f)
            temp_path = f.name
        
        try:
            gen = JsonGen(temp_path)
            assert isinstance(gen, GetTasks)
        finally:
            os.unlink(temp_path)


class TestApiGen:
    """Tests for ApiGen class."""
    
    def test_api_gen_returns_tasks(self):
        """Test that ApiGen returns list of tasks."""
        gen = ApiGen()
        tasks = gen.get_tasks()
        assert len(tasks) == 10
    
    def test_api_gen_task_structure(self):
        """Test that API tasks have correct structure."""
        gen = ApiGen()
        tasks = gen.get_tasks()
        
        for i, task in enumerate(tasks):
            assert "id" in task
            assert "payload" in task
            assert task["id"] == f"{i}{i}{i}"
            assert task["payload"] == f"api-{i}{i}{i}"
    
    def test_api_gen_implements_protocol(self):
        """Test that ApiGen implements GetTasks protocol."""
        gen = ApiGen()
        assert isinstance(gen, GetTasks)


class TestGetAllTasks:
    """Tests for get_all_tasks function."""
    
    def test_get_all_tasks_combines_sources(self):
        """Test that get_all_tasks combines tasks from multiple sources."""
        machine_gen = MachineGen(3)
        api_gen = ApiGen()
        
        all_tasks = get_all_tasks([machine_gen, api_gen])
        
        assert len(all_tasks) == 13
    
    def test_get_all_tasks_empty_list(self):
        """Test get_all_tasks with empty generator list."""
        all_tasks = get_all_tasks([])
        assert len(all_tasks) == 0
    
    def test_get_all_tasks_single_source(self):
        """Test get_all_tasks with single source."""
        machine_gen = MachineGen(5)
        all_tasks = get_all_tasks([machine_gen])
        assert len(all_tasks) == 5
    
    def test_get_all_tasks_invalid_object(self):
        """Test that get_all_tasks raises ValueError for invalid objects."""
        
        class InvalidGen:
            pass
        
        invalid = InvalidGen()
        
        with pytest.raises(ValueError):
            get_all_tasks([invalid])
    
    def test_get_all_tasks_preserves_order(self):
        """Test that get_all_tasks preserves order of tasks."""
        machine_gen = MachineGen(2)
        
        all_tasks = get_all_tasks([machine_gen])
        
        assert all_tasks[0]["id"] == 0
        assert all_tasks[1]["id"] == 1