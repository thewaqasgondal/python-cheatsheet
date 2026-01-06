"""
Advanced Testing Techniques

This module demonstrates advanced testing patterns including mocking,
fixtures, parametrization, property-based testing, and testing best practices.
"""

import pytest
import unittest.mock as mock
from unittest.mock import MagicMock, patch, Mock
import tempfile
import os
import json
import time
from typing import List, Dict, Any, Optional, Callable
import requests
from dataclasses import dataclass
import hypothesis
from hypothesis import given, strategies as st
import coverage
import subprocess
import sys


# Sample code to test (would normally be in separate modules)
@dataclass
class User:
    """Sample User dataclass."""
    id: int
    name: str
    email: str
    active: bool = True


class UserService:
    """Sample service class for testing."""

    def __init__(self, api_url: str = "https://api.example.com"):
        self.api_url = api_url
        self.session = requests.Session()

    def get_user(self, user_id: int) -> Optional[User]:
        """Fetch user from API."""
        try:
            response = self.session.get(f"{self.api_url}/users/{user_id}")
            response.raise_for_status()
            data = response.json()
            return User(**data)
        except (requests.RequestException, ValueError):
            return None

    def create_user(self, name: str, email: str) -> Optional[User]:
        """Create a new user via API."""
        try:
            data = {"name": name, "email": email}
            response = self.session.post(f"{self.api_url}/users", json=data)
            response.raise_for_status()
            result = response.json()
            return User(**result)
        except (requests.RequestException, ValueError):
            return None

    def get_all_users(self) -> List[User]:
        """Fetch all users."""
        try:
            response = self.session.get(f"{self.api_url}/users")
            response.raise_for_status()
            data = response.json()
            return [User(**user_data) for user_data in data]
        except (requests.RequestException, ValueError):
            return []

    def update_user(self, user_id: int, **updates) -> bool:
        """Update user information."""
        try:
            response = self.session.patch(f"{self.api_url}/users/{user_id}", json=updates)
            response.raise_for_status()
            return True
        except requests.RequestException:
            return False

    def delete_user(self, user_id: int) -> bool:
        """Delete a user."""
        try:
            response = self.session.delete(f"{self.api_url}/users/{user_id}")
            response.raise_for_status()
            return True
        except requests.RequestException:
            return False


class DataProcessor:
    """Sample data processing class."""

    def __init__(self, config_file: Optional[str] = None):
        self.config = self._load_config(config_file)

    def _load_config(self, config_file: Optional[str]) -> Dict[str, Any]:
        """Load configuration from file."""
        if config_file and os.path.exists(config_file):
            with open(config_file, 'r') as f:
                return json.load(f)
        return {"batch_size": 100, "timeout": 30}

    def process_batch(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process a batch of data."""
        if not data:
            return []

        batch_size = self.config.get("batch_size", 100)
        processed = []

        for i in range(0, len(data), batch_size):
            batch = data[i:i + batch_size]
            processed_batch = []

            for item in batch:
                # Simulate processing
                processed_item = item.copy()
                processed_item["processed"] = True
                processed_item["timestamp"] = time.time()
                processed_item["batch_id"] = i // batch_size
                processed_batch.append(processed_item)

            processed.extend(processed_batch)

        return processed

    def validate_data(self, data: Dict[str, Any]) -> List[str]:
        """Validate data and return list of errors."""
        errors = []

        required_fields = ["id", "name", "value"]
        for field in required_fields:
            if field not in data:
                errors.append(f"Missing required field: {field}")

        if "value" in data:
            if not isinstance(data["value"], (int, float)):
                errors.append("Value must be numeric")
            elif data["value"] < 0:
                errors.append("Value must be non-negative")

        if "name" in data and len(str(data["name"])) < 2:
            errors.append("Name must be at least 2 characters long")

        return errors


class FileManager:
    """Sample file management class."""

    def __init__(self, base_dir: str = "/tmp"):
        self.base_dir = base_dir

    def save_data(self, filename: str, data: Any) -> bool:
        """Save data to file."""
        try:
            filepath = os.path.join(self.base_dir, filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)

            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception:
            return False

    def load_data(self, filename: str) -> Optional[Any]:
        """Load data from file."""
        try:
            filepath = os.path.join(self.base_dir, filename)
            with open(filepath, 'r') as f:
                return json.load(f)
        except Exception:
            return None

    def list_files(self, pattern: str = "*") -> List[str]:
        """List files in base directory."""
        try:
            import glob
            return glob.glob(os.path.join(self.base_dir, pattern))
        except Exception:
            return []


# Test fixtures and setup
@pytest.fixture
def sample_user():
    """Fixture providing a sample user."""
    return User(id=1, name="John Doe", email="john@example.com")


@pytest.fixture
def user_service():
    """Fixture providing a UserService instance."""
    return UserService("https://api.example.com")


@pytest.fixture
def temp_config_file(tmp_path):
    """Fixture creating a temporary config file."""
    config = {"batch_size": 50, "timeout": 60}
    config_file = tmp_path / "config.json"
    with open(config_file, 'w') as f:
        json.dump(config, f)
    return str(config_file)


@pytest.fixture
def data_processor(temp_config_file):
    """Fixture providing a DataProcessor with temp config."""
    return DataProcessor(temp_config_file)


@pytest.fixture
def temp_dir(tmp_path):
    """Fixture providing a temporary directory."""
    return str(tmp_path)


@pytest.fixture
def file_manager(temp_dir):
    """Fixture providing a FileManager with temp directory."""
    return FileManager(temp_dir)


# Basic mocking examples
def test_user_service_get_user_success(user_service, sample_user):
    """Test successful user retrieval with mocking."""
    # Mock the session.get method
    mock_response = Mock()
    mock_response.json.return_value = {
        "id": sample_user.id,
        "name": sample_user.name,
        "email": sample_user.email,
        "active": sample_user.active
    }

    with patch.object(user_service.session, 'get', return_value=mock_response) as mock_get:
        result = user_service.get_user(1)

        assert result is not None
        assert result.id == sample_user.id
        assert result.name == sample_user.name
        assert result.email == sample_user.email

        # Verify the API call was made correctly
        mock_get.assert_called_once_with("https://api.example.com/users/1")


def test_user_service_get_user_failure(user_service):
    """Test user retrieval failure."""
    # Mock a failed request
    with patch.object(user_service.session, 'get', side_effect=requests.RequestException):
        result = user_service.get_user(999)
        assert result is None


def test_user_service_create_user(user_service):
    """Test user creation with mocking."""
    expected_user = User(id=2, name="Jane Doe", email="jane@example.com")

    mock_response = Mock()
    mock_response.json.return_value = {
        "id": 2,
        "name": "Jane Doe",
        "email": "jane@example.com",
        "active": True
    }

    with patch.object(user_service.session, 'post', return_value=mock_response) as mock_post:
        result = user_service.create_user("Jane Doe", "jane@example.com")

        assert result is not None
        assert result.name == "Jane Doe"
        assert result.email == "jane@example.com"

        # Verify the POST request
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        assert call_args[0][0] == "https://api.example.com/users"
        assert call_args[1]["json"] == {"name": "Jane Doe", "email": "jane@example.com"}


# Advanced mocking with context managers
def test_user_service_with_multiple_operations(user_service):
    """Test multiple operations with complex mocking."""
    # Mock responses for different operations
    get_response = Mock()
    get_response.json.return_value = {"id": 1, "name": "Test", "email": "test@example.com"}

    post_response = Mock()
    post_response.json.return_value = {"id": 2, "name": "New", "email": "new@example.com"}

    patch_response = Mock()
    delete_response = Mock()

    with patch.object(user_service.session, 'get', return_value=get_response), \
         patch.object(user_service.session, 'post', return_value=post_response), \
         patch.object(user_service.session, 'patch', return_value=patch_response), \
         patch.object(user_service.session, 'delete', return_value=delete_response):

        # Test all operations
        user = user_service.get_user(1)
        assert user is not None

        new_user = user_service.create_user("New", "new@example.com")
        assert new_user is not None

        success = user_service.update_user(1, name="Updated")
        assert success

        deleted = user_service.delete_user(1)
        assert deleted


# Parametrized tests
@pytest.mark.parametrize("user_id,expected_name", [
    (1, "User One"),
    (2, "User Two"),
    (3, "User Three"),
])
def test_get_user_parametrized(user_service, user_id, expected_name):
    """Parametrized test for different user IDs."""
    mock_response = Mock()
    mock_response.json.return_value = {
        "id": user_id,
        "name": expected_name,
        "email": f"user{user_id}@example.com"
    }

    with patch.object(user_service.session, 'get', return_value=mock_response):
        result = user_service.get_user(user_id)
        assert result.name == expected_name


@pytest.mark.parametrize("data,expected_errors", [
    ({}, ["Missing required field: id", "Missing required field: name", "Missing required field: value"]),
    ({"id": 1}, ["Missing required field: name", "Missing required field: value"]),
    ({"id": 1, "name": "A", "value": -5}, ["Name must be at least 2 characters long", "Value must be non-negative"]),
    ({"id": 1, "name": "Valid", "value": 10}, []),
])
def test_data_validation_parametrized(data_processor, data, expected_errors):
    """Parametrized test for data validation."""
    errors = data_processor.validate_data(data)
    assert errors == expected_errors


# Property-based testing with Hypothesis
@given(
    user_id=st.integers(min_value=1, max_value=1000),
    name=st.text(min_size=1, max_size=50),
    email=st.emails()
)
def test_user_creation_properties(user_id, name, email):
    """Property-based test for user creation."""
    # This would normally test the User class directly
    user = User(id=user_id, name=name, email=email)

    assert user.id == user_id
    assert user.name == name
    assert user.email == email
    assert user.active is True  # default value


@given(
    data=st.lists(
        st.dictionaries(
            keys=st.text(),
            values=st.one_of(st.integers(), st.floats(), st.text()),
            min_size=1,
            max_size=10
        ),
        min_size=0,
        max_size=100
    )
)
def test_data_processing_properties(data_processor, data):
    """Property-based test for data processing."""
    result = data_processor.process_batch(data)

    # Properties that should always hold
    assert len(result) >= len(data)  # May add fields but not remove items
    assert all("processed" in item for item in result)
    assert all("timestamp" in item for item in result)
    assert all("batch_id" in item for item in result)


# Testing file operations
def test_file_manager_save_load(file_manager, sample_user):
    """Test file save and load operations."""
    filename = "test_user.json"

    # Test save
    success = file_manager.save_data(filename, {
        "id": sample_user.id,
        "name": sample_user.name,
        "email": sample_user.email
    })
    assert success

    # Test load
    loaded_data = file_manager.load_data(filename)
    assert loaded_data is not None
    assert loaded_data["name"] == sample_user.name


def test_file_manager_list_files(file_manager):
    """Test file listing."""
    # Create some test files
    file_manager.save_data("file1.json", {"test": 1})
    file_manager.save_data("file2.json", {"test": 2})
    file_manager.save_data("data.txt", "text data")

    files = file_manager.list_files("*.json")
    assert len(files) >= 2
    assert any("file1.json" in f for f in files)
    assert any("file2.json" in f for f in files)


# Testing exceptions and error conditions
def test_user_service_network_error(user_service):
    """Test handling of network errors."""
    with patch.object(user_service.session, 'get', side_effect=requests.ConnectionError):
        result = user_service.get_user(1)
        assert result is None


def test_data_processor_invalid_config():
    """Test data processor with invalid config."""
    # Test with non-existent config file
    processor = DataProcessor("/nonexistent/config.json")

    # Should use default config
    assert processor.config["batch_size"] == 100
    assert processor.config["timeout"] == 30


# Testing with temporary files and directories
def test_file_operations_with_temp_files(tmp_path):
    """Test file operations using pytest's tmp_path fixture."""
    # Create test files
    file1 = tmp_path / "test1.json"
    file2 = tmp_path / "test2.json"

    data1 = {"name": "test1", "value": 1}
    data2 = {"name": "test2", "value": 2}

    # Write files
    file1.write_text(json.dumps(data1))
    file2.write_text(json.dumps(data2))

    # Test file manager with temp directory
    fm = FileManager(str(tmp_path))

    # Load and verify
    loaded1 = fm.load_data("test1.json")
    loaded2 = fm.load_data("test2.json")

    assert loaded1 == data1
    assert loaded2 == data2


# Mocking environment and system calls
def test_system_operations_with_mocking():
    """Test operations that interact with the system."""
    with patch('os.makedirs') as mock_makedirs, \
         patch('builtins.open', new_callable=mock.mock_open) as mock_file:

        fm = FileManager("/test/dir")
        success = fm.save_data("test.json", {"test": "data"})

        assert success
        mock_makedirs.assert_called_once_with("/test/dir", exist_ok=True)
        mock_file.assert_called()


# Testing async code (if applicable)
@pytest.mark.asyncio
async def test_async_operation():
    """Example of testing async code."""
    # This would test async functions if they existed
    pass


# Custom test markers and configuration
@pytest.mark.slow
def test_slow_operation():
    """A test that takes a long time."""
    time.sleep(0.1)  # Simulate slow operation
    assert True


@pytest.mark.integration
def test_integration_with_external_service():
    """Integration test that might be skipped in CI."""
    # This would test real external services
    assert True


# Test coverage and reporting
def test_coverage_collection():
    """Demonstrate coverage collection."""
    # This is just an example - coverage is usually handled by pytest-cov
    assert True


# Fixtures with different scopes
@pytest.fixture(scope="session")
def session_fixture():
    """Session-scoped fixture - runs once per test session."""
    print("Setting up session fixture")
    yield "session_data"
    print("Tearing down session fixture")


@pytest.fixture(scope="module")
def module_fixture():
    """Module-scoped fixture - runs once per test module."""
    print("Setting up module fixture")
    yield "module_data"
    print("Tearing down module fixture")


@pytest.fixture(scope="class")
def class_fixture():
    """Class-scoped fixture - runs once per test class."""
    print("Setting up class fixture")
    yield "class_data"
    print("Tearing down class fixture")


@pytest.fixture
def function_fixture():
    """Function-scoped fixture - runs for each test function."""
    print("Setting up function fixture")
    yield "function_data"
    print("Tearing down function fixture")


def test_fixture_scopes(session_fixture, module_fixture, function_fixture):
    """Test demonstrating different fixture scopes."""
    assert session_fixture == "session_data"
    assert module_fixture == "module_data"
    assert function_fixture == "function_data"


# Test configuration and conftest.py concepts
def test_configuration_loading():
    """Test loading configuration for tests."""
    # This would typically be in conftest.py
    assert True


if __name__ == "__main__":
    # Run tests manually for demonstration
    print("Advanced Testing Examples")
    print("=" * 30)

    # Note: In practice, these would be run with pytest
    print("Run these tests with: pytest advanced_testing/test_examples.py -v")
    print("For coverage: pytest --cov=advanced_testing --cov-report=html")
    print("For hypothesis: pytest -k 'properties'")

    # Demonstrate basic functionality
    print("\nDemonstrating basic functionality...")

    # Test data processor
    processor = DataProcessor()
    test_data = [{"id": 1, "name": "Test", "value": 10}]
    result = processor.process_batch(test_data)

    print(f"Processed {len(result)} items")
    print(f"Sample result: {result[0] if result else 'None'}")

    # Test validation
    errors = processor.validate_data({"id": 1, "name": "A", "value": -5})
    print(f"Validation errors: {errors}")

    print("\nTo run the full test suite:")
    print("1. Install dependencies: pip install pytest mock hypothesis")
    print("2. Run tests: pytest advanced_testing/ -v")
    print("3. Run with coverage: pytest --cov=advanced_testing --cov-report=html")