# Advanced Testing Examples

This directory contains comprehensive examples of advanced testing techniques and best practices.

## Files

- `advanced_testing_patterns.py` - Complete advanced testing tutorial covering mocking, fixtures, parametrization, and property-based testing

## Prerequisites

```bash
pip install pytest>=6.0.0
pip install pytest-cov>=2.0.0
pip install hypothesis>=6.0.0
pip install mock>=4.0.0  # Usually included with Python 3.3+
```

## Topics Covered

### advanced_testing_patterns.py

#### Mocking and Patching
- **unittest.mock**: Mock objects, patching, context managers
- **API mocking**: Mocking HTTP requests and external services
- **Object mocking**: Mocking classes, methods, and attributes
- **Side effect mocking**: Simulating exceptions and errors

#### Advanced Fixtures
- **Fixture scopes**: function, class, module, session
- **Fixture parametrization**: Dynamic fixture values
- **Fixture dependencies**: Fixtures using other fixtures
- **Temporary resources**: pytest's tmp_path and tmp_dir

#### Parametrized Tests
- **@pytest.mark.parametrize**: Testing multiple input combinations
- **Indirect parametrization**: Parametrizing fixtures
- **Complex parametrization**: Nested parameters and combinations

#### Property-Based Testing
- **Hypothesis library**: Generating test cases automatically
- **Strategies**: Defining data generation strategies
- **Property testing**: Testing general properties of code
- **Shrinking**: Automatic minimization of failing test cases

#### Test Organization
- **Test markers**: Custom markers for test categorization
- **Test configuration**: conftest.py patterns
- **Test discovery**: Naming conventions and structure
- **Test isolation**: Ensuring tests don't interfere with each other

#### Error and Exception Testing
- **Exception testing**: Testing expected failures
- **Error conditions**: Testing edge cases and error paths
- **Network failures**: Testing connectivity issues
- **File system errors**: Testing I/O failures

#### Test Data Management
- **Sample data**: Creating realistic test data
- **Data fixtures**: Reusable test data
- **Temporary files**: Safe file operations in tests
- **Database mocking**: Testing database operations

## Running the Examples

```bash
# Run all tests
pytest advanced_testing/advanced_testing_patterns.py -v

# Run with coverage
pytest advanced_testing/ --cov=advanced_testing --cov-report=html

# Run specific test categories
pytest -m "not slow"  # Skip slow tests
pytest -k "mock"      # Run tests containing "mock"

# Run property-based tests
pytest -k "properties"

# Generate coverage report
pytest --cov=advanced_testing --cov-report=term-missing
```

## Key Concepts

### Mocking Patterns

#### Basic Mocking
```python
from unittest.mock import Mock, patch

# Mock a function
mock_func = Mock(return_value=42)
result = mock_func()
assert result == 42

# Patch an object
with patch('module.Class.method') as mock_method:
    mock_method.return_value = "mocked"
    result = some_function()
    assert result == "mocked"
```

#### Context Manager Mocking
```python
with patch.object(obj, 'method', return_value=42) as mock_method:
    result = obj.method()
    assert result == 42
    mock_method.assert_called_once()
```

### Advanced Fixtures

#### Scoped Fixtures
```python
@pytest.fixture(scope="session")  # Once per test session
def expensive_resource():
    resource = create_expensive_resource()
    yield resource
    resource.cleanup()

@pytest.fixture(scope="function")  # For each test function
def temp_data():
    return {"test": "data"}
```

#### Parametrized Fixtures
```python
@pytest.fixture(params=[1, 2, 3])
def number(request):
    return request.param

def test_with_number(number):
    assert number in [1, 2, 3]
```

### Parametrization

#### Basic Parametrization
```python
@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
])
def test_double(input, expected):
    assert double(input) == expected
```

#### Multiple Parameters
```python
@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (4, 5, 9),
    (-1, 1, 0),
])
def test_add(a, b, expected):
    assert add(a, b) == expected
```

### Property-Based Testing

#### Basic Hypothesis Test
```python
from hypothesis import given, strategies as st

@given(x=st.integers(), y=st.integers())
def test_add_commutative(x, y):
    assert add(x, y) == add(y, x)
```

#### Complex Strategies
```python
@given(
    name=st.text(min_size=1, max_size=50),
    age=st.integers(min_value=0, max_value=150),
    email=st.emails()
)
def test_user_creation(name, age, email):
    user = User(name=name, age=age, email=email)
    assert user.name == name
    assert user.age == age
```

## Test Structure Best Practices

### File Organization
```
tests/
├── __init__.py
├── conftest.py          # Shared fixtures and configuration
├── test_unit.py         # Unit tests
├── test_integration.py  # Integration tests
├── test_api.py          # API tests
└── fixtures/
    ├── __init__.py
    └── sample_data.py   # Test data fixtures
```

### Test Naming Conventions
```python
def test_function_name_condition_expected_result():
    """Test that function_name behaves correctly under condition."""
    pass

def test_user_creation_with_valid_data_returns_user():
    pass

def test_api_call_with_invalid_token_raises_authentication_error():
    pass
```

### Test Categories with Markers
```python
@pytest.mark.unit
def test_fast_unit_test():
    pass

@pytest.mark.integration
@pytest.mark.slow
def test_slow_integration_test():
    pass

@pytest.mark.skip(reason="Not implemented yet")
def test_future_feature():
    pass
```

## Mocking Best Practices

1. **Patch at the right level**: Patch where the code imports, not where it's defined
2. **Use context managers**: Ensure mocks are cleaned up properly
3. **Verify interactions**: Use `assert_called_once()`, `assert_called_with()` etc.
4. **Don't mock everything**: Only mock external dependencies
5. **Keep mocks simple**: Complex mocks make tests hard to understand

## Common Testing Patterns

### Testing External APIs
```python
def test_api_call_success():
    mock_response = Mock()
    mock_response.json.return_value = {"data": "value"}

    with patch('requests.get', return_value=mock_response):
        result = api_call()
        assert result["data"] == "value"
```

### Testing File Operations
```python
def test_file_save(tmp_path):
    file_path = tmp_path / "test.txt"
    save_data(file_path, "content")

    assert file_path.exists()
    assert file_path.read_text() == "content"
```

### Testing Exceptions
```python
def test_invalid_input_raises_error():
    with pytest.raises(ValueError, match="Invalid input"):
        process_data("invalid")
```

## Coverage and Quality

### Coverage Configuration
```ini
# pytest.ini or setup.cfg
[tool:pytest]
addopts = --cov=package --cov-report=html --cov-report=term-missing
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

### Quality Checks
```bash
# Run tests with coverage
pytest --cov=package --cov-report=html

# Check for missing tests
coverage report --fail-under=80

# Run with additional checks
pytest --strict-markers --disable-warnings
```

## Integration with CI/CD

### GitHub Actions Example
```yaml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.8'
    - name: Install dependencies
      run: |
        pip install -e .
        pip install -r requirements-dev.txt
    - name: Run tests
      run: pytest --cov=package --cov-report=xml
    - name: Upload coverage
      uses: codecov/codecov-action@v2
```

## Debugging Tests

### Common Issues
- **Import errors**: Check Python path and package structure
- **Mock not working**: Verify patch target path
- **Fixture not found**: Check fixture scope and location
- **Test isolation**: Ensure tests don't depend on each other

### Debugging Tools
```python
# Add debug prints
def test_something():
    result = some_function()
    print(f"Debug: result = {result}")  # Temporary debug
    assert result == expected

# Use pytest breakpoints
def test_with_breakpoint():
    result = some_function()
    import pdb; pdb.set_trace()  # Breakpoint
    assert result == expected

# Run specific test with verbose output
pytest tests/test_file.py::TestClass::test_method -v -s
```