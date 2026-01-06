"""
Pytest Testing Examples

This module demonstrates comprehensive testing with pytest, including
fixtures, parametrization, mocking, and best practices.
"""

import pytest
import tempfile
import os
import json
from typing import List, Dict, Any
from unittest.mock import Mock, patch, MagicMock


# Code under test (usually in separate modules)
class Calculator:
    """Simple calculator class for testing."""

    def add(self, a: float, b: float) -> float:
        return a + b

    def subtract(self, a: float, b: float) -> float:
        return a - b

    def multiply(self, a: float, b: float) -> float:
        return a * b

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

    def power(self, base: float, exponent: float) -> float:
        return base ** exponent


class UserManager:
    """User management class for testing."""

    def __init__(self):
        self.users = {}

    def create_user(self, user_id: str, name: str, email: str) -> Dict[str, Any]:
        if user_id in self.users:
            raise ValueError(f"User {user_id} already exists")

        user = {
            'id': user_id,
            'name': name,
            'email': email,
            'active': True
        }
        self.users[user_id] = user
        return user

    def get_user(self, user_id: str) -> Dict[str, Any]:
        if user_id not in self.users:
            raise KeyError(f"User {user_id} not found")
        return self.users[user_id]

    def update_user(self, user_id: str, **updates) -> Dict[str, Any]:
        user = self.get_user(user_id)
        user.update(updates)
        return user

    def delete_user(self, user_id: str) -> None:
        if user_id not in self.users:
            raise KeyError(f"User {user_id} not found")
        del self.users[user_id]


class FileProcessor:
    """File processing class for testing."""

    def read_json_file(self, filepath: str) -> Dict[str, Any]:
        with open(filepath, 'r') as f:
            return json.load(f)

    def write_json_file(self, filepath: str, data: Dict[str, Any]) -> None:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

    def process_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process data and add metadata."""
        processed = data.copy()
        processed['processed_at'] = '2024-01-01T00:00:00Z'
        processed['version'] = '1.0'
        return processed


# Test fixtures
@pytest.fixture
def calculator():
    """Fixture providing a Calculator instance."""
    return Calculator()


@pytest.fixture
def user_manager():
    """Fixture providing a UserManager instance."""
    return UserManager()


@pytest.fixture
def sample_user_data():
    """Fixture providing sample user data."""
    return {
        'user_id': 'test_user_123',
        'name': 'John Doe',
        'email': 'john@example.com'
    }


@pytest.fixture
def temp_json_file():
    """Fixture creating a temporary JSON file."""
    data = {'name': 'Test', 'value': 42}

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(data, f)
        temp_path = f.name

    yield temp_path

    # Cleanup
    if os.path.exists(temp_path):
        os.unlink(temp_path)


# Basic test functions
def test_calculator_add(calculator):
    """Test calculator addition."""
    assert calculator.add(2, 3) == 5
    assert calculator.add(-1, 1) == 0
    assert calculator.add(0.5, 0.3) == 0.8


def test_calculator_subtract(calculator):
    """Test calculator subtraction."""
    assert calculator.subtract(5, 3) == 2
    assert calculator.subtract(1, 1) == 0
    assert calculator.subtract(0.5, 0.3) == 0.2


def test_calculator_multiply(calculator):
    """Test calculator multiplication."""
    assert calculator.multiply(2, 3) == 6
    assert calculator.multiply(-2, 3) == -6
    assert calculator.multiply(0.5, 2) == 1.0


def test_calculator_divide(calculator):
    """Test calculator division."""
    assert calculator.divide(6, 2) == 3.0
    assert calculator.divide(5, 2) == 2.5

    # Test division by zero
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        calculator.divide(5, 0)


def test_calculator_power(calculator):
    """Test calculator power function."""
    assert calculator.power(2, 3) == 8
    assert calculator.power(4, 0.5) == 2.0
    assert calculator.power(10, -1) == 0.1


# Parametrized tests
@pytest.mark.parametrize("a,b,expected", [
    (2, 3, 5),
    (-1, 1, 0),
    (0, 0, 0),
    (100, 200, 300),
])
def test_calculator_add_parametrized(calculator, a, b, expected):
    """Parametrized test for calculator addition."""
    assert calculator.add(a, b) == expected


@pytest.mark.parametrize("operation,a,b,expected", [
    ("add", 2, 3, 5),
    ("subtract", 5, 3, 2),
    ("multiply", 2, 3, 6),
    ("divide", 6, 2, 3.0),
])
def test_calculator_operations_parametrized(calculator, operation, a, b, expected):
    """Parametrized test for all calculator operations."""
    method = getattr(calculator, operation)
    assert method(a, b) == expected


# UserManager tests
def test_create_user(user_manager, sample_user_data):
    """Test creating a new user."""
    user = user_manager.create_user(**sample_user_data)

    assert user['id'] == sample_user_data['user_id']
    assert user['name'] == sample_user_data['name']
    assert user['email'] == sample_user_data['email']
    assert user['active'] is True


def test_create_duplicate_user(user_manager, sample_user_data):
    """Test creating a user that already exists."""
    # Create user first
    user_manager.create_user(**sample_user_data)

    # Try to create again
    with pytest.raises(ValueError, match="already exists"):
        user_manager.create_user(**sample_user_data)


def test_get_user(user_manager, sample_user_data):
    """Test retrieving a user."""
    created_user = user_manager.create_user(**sample_user_data)
    retrieved_user = user_manager.get_user(sample_user_data['user_id'])

    assert retrieved_user == created_user


def test_get_nonexistent_user(user_manager):
    """Test retrieving a user that doesn't exist."""
    with pytest.raises(KeyError, match="not found"):
        user_manager.get_user("nonexistent_user")


def test_update_user(user_manager, sample_user_data):
    """Test updating user information."""
    user_manager.create_user(**sample_user_data)

    updated_user = user_manager.update_user(
        sample_user_data['user_id'],
        name="Jane Doe",
        email="jane@example.com"
    )

    assert updated_user['name'] == "Jane Doe"
    assert updated_user['email'] == "jane@example.com"


def test_delete_user(user_manager, sample_user_data):
    """Test deleting a user."""
    user_manager.create_user(**sample_user_data)

    # Verify user exists
    user_manager.get_user(sample_user_data['user_id'])

    # Delete user
    user_manager.delete_user(sample_user_data['user_id'])

    # Verify user is gone
    with pytest.raises(KeyError):
        user_manager.get_user(sample_user_data['user_id'])


# FileProcessor tests with mocking
def test_read_json_file(temp_json_file):
    """Test reading a JSON file."""
    processor = FileProcessor()
    data = processor.read_json_file(temp_json_file)

    assert data['name'] == 'Test'
    assert data['value'] == 42


def test_write_json_file():
    """Test writing a JSON file."""
    processor = FileProcessor()
    data = {'message': 'Hello', 'number': 123}

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_path = f.name

    try:
        processor.write_json_file(temp_path, data)

        # Verify file was written correctly
        with open(temp_path, 'r') as f:
            written_data = json.load(f)

        assert written_data == data
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)


@patch('builtins.open')
def test_process_data(mock_open):
    """Test data processing with mocked file operations."""
    processor = FileProcessor()
    input_data = {'name': 'Test', 'value': 42}

    result = processor.process_data(input_data)

    # Verify the result has additional fields
    assert result['name'] == 'Test'
    assert result['value'] == 42
    assert 'processed_at' in result
    assert result['version'] == '1.0'

    # Verify original data wasn't modified
    assert input_data == {'name': 'Test', 'value': 42}


# Mock examples
@patch('json.load')
def test_read_json_with_mock(mock_json_load):
    """Test reading JSON with mocked json.load."""
    mock_json_load.return_value = {'mocked': True, 'data': 'test'}

    processor = FileProcessor()

    with patch('builtins.open', create=True):
        result = processor.read_json_file('fake_file.json')

    assert result['mocked'] is True
    assert result['data'] == 'test'
    mock_json_load.assert_called_once()


@patch('requests.get')
def test_api_call_with_mock(mock_get):
    """Example of mocking external API calls."""
    # Mock the response
    mock_response = Mock()
    mock_response.json.return_value = {'status': 'success', 'data': [1, 2, 3]}
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    # Import requests here to avoid import errors if not installed
    import requests

    # Simulate API call
    response = requests.get('https://api.example.com/data')
    data = response.json()

    assert data['status'] == 'success'
    assert data['data'] == [1, 2, 3]
    mock_get.assert_called_once_with('https://api.example.com/data')


# Test classes
class TestCalculatorClass:
    """Test class for Calculator."""

    def setup_method(self):
        """Setup method called before each test."""
        self.calc = Calculator()

    def teardown_method(self):
        """Teardown method called after each test."""
        pass

    def test_add_in_class(self):
        """Test addition within a test class."""
        assert self.calc.add(1, 2) == 3

    def test_divide_by_zero_in_class(self):
        """Test division by zero within a test class."""
        with pytest.raises(ValueError):
            self.calc.divide(5, 0)


# Custom markers and skipping
@pytest.mark.slow
def test_slow_operation():
    """A test that takes a long time (marked as slow)."""
    import time
    time.sleep(0.1)  # Simulate slow operation
    assert True


@pytest.mark.skip(reason="This test is temporarily disabled")
def test_skipped():
    """A test that is skipped."""
    assert False  # This would fail if run


@pytest.mark.skipif(os.name != 'posix', reason="Test only runs on POSIX systems")
def test_posix_only():
    """Test that only runs on POSIX systems."""
    assert True


# Fixtures with different scopes
@pytest.fixture(scope="session")
def database_connection():
    """Session-scoped fixture for database connection."""
    # In real code, this would create a database connection
    connection = {"connected": True, "id": "session_db"}
    yield connection
    # Cleanup after all tests in session
    connection["connected"] = False


@pytest.fixture(scope="module")
def module_data():
    """Module-scoped fixture."""
    return {"module_value": 42}


def test_with_session_fixture(database_connection):
    """Test using session-scoped fixture."""
    assert database_connection["connected"] is True


def test_with_module_fixture(module_data):
    """Test using module-scoped fixture."""
    assert module_data["module_value"] == 42


# Custom pytest configuration and conftest.py examples would go here
# (typically in conftest.py file in the test directory)


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])