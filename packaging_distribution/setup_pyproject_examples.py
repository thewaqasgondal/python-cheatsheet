"""
Python Packaging and Distribution

This module demonstrates comprehensive Python packaging techniques
including setup.py, pyproject.toml, and modern distribution practices.
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional
import json
import shutil


def create_setup_py_example():
    """Create a complete setup.py example with all features."""
    print("=== Creating setup.py Example ===")

    setup_py_content = '''"""
Example setup.py for a Python package.

This demonstrates comprehensive packaging with setup.py.
"""

from setuptools import setup, find_packages
import os

# Read the contents of README file
def read_readme():
    """Read README file."""
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "A comprehensive Python package example."

# Read requirements from file
def read_requirements():
    """Read requirements from requirements.txt."""
    req_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(req_path):
        with open(req_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

# Package metadata
NAME = "mypackage"
VERSION = "1.0.0"
DESCRIPTION = "A comprehensive Python package example"
AUTHOR = "Your Name"
AUTHOR_EMAIL = "your.email@example.com"
URL = "https://github.com/yourusername/mypackage"
LICENSE = "MIT"

# Long description
LONG_DESCRIPTION = read_readme()
LONG_DESCRIPTION_CONTENT_TYPE = "text/markdown"

# Classifiers help users find your project
CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Utilities",
]

# Keywords for PyPI
KEYWORDS = ["python", "package", "example", "packaging"]

# Dependencies
INSTALL_REQUIRES = read_requirements() or [
    "requests>=2.25.0",
    "click>=8.0.0",
    "numpy>=1.21.0",
]

# Optional dependencies
EXTRAS_REQUIRE = {
    "dev": [
        "pytest>=6.0.0",
        "pytest-cov>=2.0.0",
        "black>=21.0.0",
        "flake8>=3.9.0",
        "mypy>=0.900",
        "sphinx>=4.0.0",
        "sphinx-rtd-theme>=1.0.0",
    ],
    "docs": [
        "sphinx>=4.0.0",
        "sphinx-rtd-theme>=1.0.0",
    ],
    "test": [
        "pytest>=6.0.0",
        "pytest-cov>=2.0.0",
    ],
}

# Entry points for console scripts
ENTRY_POINTS = {
    "console_scripts": [
        "mypackage-cli=mypackage.cli:main",
        "mypackage-analyze=mypackage.analyzer:analyze_command",
    ],
}

# Package data and manifest
PACKAGE_DATA = {
    "mypackage": [
        "data/*.json",
        "templates/*.html",
        "config/*.yaml",
    ],
}

# Include package data
INCLUDE_PACKAGE_DATA = True

# Exclude patterns
EXCLUDE_PACKAGE_DATA = {
    "mypackage": [
        "*.pyc",
        "__pycache__",
        "*.pyo",
    ],
}

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    license=LICENSE,
    classifiers=CLASSIFIERS,
    keywords=KEYWORDS,
    packages=find_packages(exclude=["tests", "tests.*", "docs"]),
    include_package_data=INCLUDE_PACKAGE_DATA,
    package_data=PACKAGE_DATA,
    exclude_package_data=EXCLUDE_PACKAGE_DATA,
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    entry_points=ENTRY_POINTS,
    python_requires=">=3.8",
    zip_safe=False,  # For mypy compatibility
    project_urls={
        "Bug Reports": f"{URL}/issues",
        "Source": URL,
        "Documentation": f"{URL}/blob/main/README.md",
    },
)
'''

    # Write setup.py
    with open('setup.py', 'w', encoding='utf-8') as f:
        f.write(setup_py_content)

    print("Created setup.py with comprehensive configuration")


def create_pyproject_toml_example():
    """Create a modern pyproject.toml example."""
    print("\n=== Creating pyproject.toml Example ===")

    pyproject_content = '''[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "mypackage"
version = "1.0.0"
description = "A comprehensive Python package example"
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.8"
authors = [
    {name = "Your Name", email = "your.email@example.com"},
]
maintainers = [
    {name = "Your Name", email = "your.email@example.com"},
]
keywords = ["python", "package", "example", "packaging"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Utilities",
]
dependencies = [
    "requests>=2.25.0",
    "click>=8.0.0",
    "numpy>=1.21.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=6.0.0",
    "pytest-cov>=2.0.0",
    "black>=21.0.0",
    "flake8>=3.9.0",
    "mypy>=0.900",
    "sphinx>=4.0.0",
    "sphinx-rtd-theme>=1.0.0",
]
docs = [
    "sphinx>=4.0.0",
    "sphinx-rtd-theme>=1.0.0",
]
test = [
    "pytest>=6.0.0",
    "pytest-cov>=2.0.0",
]

[project.urls]
Homepage = "https://github.com/yourusername/mypackage"
Documentation = "https://mypackage.readthedocs.io/"
Repository = "https://github.com/yourusername/mypackage"
"Bug Reports" = "https://github.com/yourusername/mypackage/issues"
Changelog = "https://github.com/yourusername/mypackage/blob/main/CHANGELOG.md"

[project.scripts]
mypackage-cli = "mypackage.cli:main"
mypackage-analyze = "mypackage.analyzer:analyze_command"

[tool.setuptools]
zip-safe = false
include-package-data = true

[tool.setuptools.packages.find]
exclude = ["tests*", "docs*"]

[tool.setuptools.package-data]
mypackage = ["data/*.json", "templates/*.html", "config/*.yaml"]

# Black code formatting
[tool.black]
line-length = 88
target-version = ['py38', 'py39', 'py310', 'py311']
include = '\\.pyi?$'
extend-exclude = '''
/(
  # directories
  \\.eggs
  | \\.git
  | \\.hg
  | \\.mypy_cache
  | \\.tox
  | \\.venv
  | build
  | dist
)/
'''

# isort import sorting
[tool.isort]
profile = "black"
multi_line_output = 3
line_length = 88
known_first_party = ["mypackage"]
known_third_party = ["numpy", "pandas", "requests"]

# MyPy type checking
[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
warn_unreachable = true
strict_equality = true

[[tool.mypy.overrides]]
module = ["tests.*"]
ignore_errors = true

# Pytest configuration
[tool.pytest.ini_options]
minversion = "6.0"
addopts = "-ra -q --cov=mypackage --cov-report=html --cov-report=term-missing"
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]

[tool.coverage.run]
source = ["mypackage"]
omit = [
    "*/tests/*",
    "*/test_*.py",
    "setup.py",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "class .*\bProtocol\\):",
    "@(abc\\.)?abstractmethod",
]
'''

    # Write pyproject.toml
    with open('pyproject.toml', 'w', encoding='utf-8') as f:
        f.write(pyproject_content)

    print("Created pyproject.toml with modern Python packaging standards")


def create_manifest_in_example():
    """Create MANIFEST.in for additional files."""
    print("\n=== Creating MANIFEST.in Example ===")

    manifest_content = '''# MANIFEST.in - Include additional files in source distribution
# This file is used when building with setup.py (not needed for pyproject.toml)

# Include all files in these directories
recursive-include mypackage/data *
recursive-include mypackage/templates *
recursive-include mypackage/config *

# Include specific file types
include *.md
include *.txt
include LICENSE
include CHANGELOG.md

# Include documentation
recursive-include docs *

# Exclude patterns
global-exclude *.pyc
global-exclude __pycache__
global-exclude *.pyo
global-exclude .git*
global-exclude .DS_Store
global-exclude Thumbs.db

# Include tests (optional, usually excluded from distributions)
# recursive-include tests *
'''

    with open('MANIFEST.in', 'w', encoding='utf-8') as f:
        f.write(manifest_content)

    print("Created MANIFEST.in for additional file inclusion")


def create_package_structure():
    """Create a sample package structure."""
    print("\n=== Creating Sample Package Structure ===")

    # Create package directory
    package_dir = Path('mypackage')
    package_dir.mkdir(exist_ok=True)

    # Create __init__.py
    init_content = '''"""
MyPackage - A comprehensive Python package example.

This package demonstrates best practices for Python packaging and distribution.
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .core import MyClass
from .utils import helper_function

__all__ = ["MyClass", "helper_function"]
'''

    with open(package_dir / '__init__.py', 'w', encoding='utf-8') as f:
        f.write(init_content)

    # Create core.py
    core_content = '''"""
Core functionality for MyPackage.
"""

from typing import Optional, List, Dict, Any
import json
import os
from pathlib import Path


class MyClass:
    """A sample class demonstrating package structure."""

    def __init__(self, name: str, value: Optional[int] = None):
        """Initialize MyClass.

        Args:
            name: The name of the instance
            value: An optional integer value
        """
        self.name = name
        self.value = value or 0
        self.data = []

    def add_data(self, item: Any) -> None:
        """Add an item to the data list."""
        self.data.append(item)

    def get_data(self) -> List[Any]:
        """Get the current data list."""
        return self.data.copy()

    def save_to_file(self, filepath: str) -> None:
        """Save instance data to a JSON file."""
        data = {
            'name': self.name,
            'value': self.value,
            'data': self.data
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    @classmethod
    def load_from_file(cls, filepath: str) -> 'MyClass':
        """Load instance data from a JSON file."""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        instance = cls(data['name'], data['value'])
        instance.data = data['data']
        return instance

    def __str__(self) -> str:
        return f"MyClass(name='{self.name}', value={self.value}, items={len(self.data)})"

    def __repr__(self) -> str:
        return f"MyClass('{self.name}', {self.value})"
'''

    with open(package_dir / 'core.py', 'w', encoding='utf-8') as f:
        f.write(core_content)

    # Create utils.py
    utils_content = '''"""
Utility functions for MyPackage.
"""

from typing import List, Dict, Any, Union
import hashlib
import time


def helper_function(data: List[Any]) -> Dict[str, Any]:
    """A helper function that processes a list of data.

    Args:
        data: List of items to process

    Returns:
        Dictionary with processing results
    """
    if not data:
        return {'count': 0, 'sum': 0, 'average': 0}

    # Calculate statistics
    count = len(data)
    numeric_data = [x for x in data if isinstance(x, (int, float))]

    if numeric_data:
        total = sum(numeric_data)
        average = total / len(numeric_data)
    else:
        total = 0
        average = 0

    return {
        'count': count,
        'sum': total,
        'average': average,
        'numeric_count': len(numeric_data)
    }


def generate_hash(text: str, algorithm: str = 'sha256') -> str:
    """Generate a hash of the given text.

    Args:
        text: Text to hash
        algorithm: Hash algorithm to use (md5, sha1, sha256, sha512)

    Returns:
        Hexadecimal hash string
    """
    hash_obj = hashlib.new(algorithm)
    hash_obj.update(text.encode('utf-8'))
    return hash_obj.hexdigest()


def measure_execution_time(func, *args, **kwargs):
    """Measure the execution time of a function.

    Args:
        func: Function to measure
        *args: Positional arguments for the function
        **kwargs: Keyword arguments for the function

    Returns:
        Tuple of (result, execution_time)
    """
    start_time = time.perf_counter()
    result = func(*args, **kwargs)
    end_time = time.perf_counter()

    execution_time = end_time - start_time
    return result, execution_time


def validate_email(email: str) -> bool:
    """Simple email validation.

    Args:
        email: Email address to validate

    Returns:
        True if email format is valid, False otherwise
    """
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def format_file_size(size_bytes: Union[int, float]) -> str:
    """Format file size in human-readable format.

    Args:
        size_bytes: Size in bytes

    Returns:
        Formatted string (e.g., "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return ".1f"
        size_bytes /= 1024.0
    return ".1f"
'''

    with open(package_dir / 'utils.py', 'w', encoding='utf-8') as f:
        f.write(utils_content)

    # Create CLI module
    cli_dir = package_dir / 'cli'
    cli_dir.mkdir(exist_ok=True)

    cli_init = '''"""CLI module for MyPackage."""'''

    with open(cli_dir / '__init__.py', 'w', encoding='utf-8') as f:
        f.write(cli_init)

    cli_main = '''"""
Command-line interface for MyPackage.
"""

import click
from ..core import MyClass
from ..utils import helper_function, generate_hash


@click.group()
@click.version_option(version="1.0.0")
def main():
    """MyPackage command-line interface."""
    pass


@main.command()
@click.argument('name')
@click.option('--value', '-v', type=int, default=0, help='Initial value')
def create(name, value):
    """Create a new MyClass instance."""
    instance = MyClass(name, value)
    click.echo(f"Created: {instance}")


@main.command()
@click.argument('text')
@click.option('--algorithm', '-a', type=click.Choice(['md5', 'sha1', 'sha256', 'sha512']),
              default='sha256', help='Hash algorithm')
def hash(text, algorithm):
    """Generate hash of text."""
    result = generate_hash(text, algorithm)
    click.echo(f"{algorithm.upper()}: {result}")


@main.command()
@click.argument('numbers', nargs=-1, type=float)
def analyze(numbers):
    """Analyze a list of numbers."""
    if not numbers:
        click.echo("No numbers provided")
        return

    result = helper_function(list(numbers))
    click.echo("Analysis Results:")
    click.echo(f"  Count: {result['count']}")
    click.echo(f"  Sum: {result['sum']}")
    click.echo(f"  Average: {result['average']}")


if __name__ == "__main__":
    main()
'''

    with open(cli_dir / 'main.py', 'w', encoding='utf-8') as f:
        f.write(cli_main)

    # Create data directory with sample files
    data_dir = package_dir / 'data'
    data_dir.mkdir(exist_ok=True)

    sample_data = {
        "package_info": {
            "name": "MyPackage",
            "version": "1.0.0",
            "description": "A comprehensive Python package example"
        },
        "features": [
            "Core functionality",
            "CLI interface",
            "Utility functions",
            "Data processing"
        ]
    }

    with open(data_dir / 'package_data.json', 'w', encoding='utf-8') as f:
        json.dump(sample_data, f, indent=2, ensure_ascii=False)

    print("Created sample package structure with modules and data")


def create_readme_and_docs():
    """Create README and documentation files."""
    print("\n=== Creating Documentation ===")

    readme_content = '''# MyPackage

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT/)
[![PyPI version](https://badge.fury.io/py/mypackage.svg)](https://pypi.org/project/mypackage/)

A comprehensive Python package example demonstrating best practices for packaging and distribution.

## Features

- **Core Functionality**: Main package classes and utilities
- **CLI Interface**: Command-line tools for common operations
- **Data Processing**: Helper functions for data manipulation
- **Type Hints**: Full type annotation support
- **Documentation**: Comprehensive docstrings and examples

## Installation

### From PyPI
```bash
pip install mypackage
```

### From Source
```bash
git clone https://github.com/yourusername/mypackage.git
cd mypackage
pip install -e .
```

### Development Installation
```bash
pip install -e ".[dev]"
```

## Usage

### Basic Usage

```python
from mypackage import MyClass, helper_function

# Create an instance
obj = MyClass("example", 42)
obj.add_data("item1")
obj.add_data("item2")

# Use utility function
result = helper_function([1, 2, 3, 4, 5])
print(result)  # {'count': 5, 'sum': 15, 'average': 3.0}
```

### Command Line Interface

```bash
# Create a new instance
mypackage-cli create myobject --value 100

# Generate hash
mypackage-cli hash "Hello World" --algorithm sha256

# Analyze numbers
mypackage-cli analyze 1 2 3 4 5
```

## Development

### Setup Development Environment

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run type checking
mypy mypackage

# Format code
black mypackage

# Lint code
flake8 mypackage
```

### Building and Publishing

```bash
# Build distribution
python -m build

# Upload to PyPI (requires API token)
twine upload dist/*
```

## Project Structure

```
mypackage/
├── __init__.py          # Package initialization
├── core.py              # Main classes and functionality
├── utils.py             # Utility functions
├── cli/                 # Command-line interface
│   ├── __init__.py
│   └── main.py
└── data/                # Package data files
    └── package_data.json
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.
'''

    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)

    # Create requirements.txt
    requirements_content = '''# Core dependencies
requests>=2.25.0
click>=8.0.0
numpy>=1.21.0

# Development dependencies
pytest>=6.0.0
black>=21.0.0
flake8>=3.9.0
mypy>=0.900
'''

    with open('requirements.txt', 'w', encoding='utf-8') as f:
        f.write(requirements_content)

    # Create LICENSE
    license_content = '''MIT License

Copyright (c) 2024 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

    with open('LICENSE', 'w', encoding='utf-8') as f:
        f.write(license_content)

    print("Created README.md, requirements.txt, and LICENSE")


def demonstrate_packaging_commands():
    """Demonstrate common packaging commands."""
    print("\n=== Packaging Commands Demonstration ===")

    commands = [
        ("Check package structure", "python -c \"import setuptools; setuptools.find_packages()\""),
        ("Validate setup.py", "python setup.py check"),
        ("Create source distribution", "python setup.py sdist"),
        ("Create wheel", "python setup.py bdist_wheel"),
        ("Show package info", "python setup.py --name --version"),
        ("List package files", "python -c \"from setuptools import find_packages; print(find_packages())\""),
    ]

    print("Common packaging commands:")
    for description, command in commands:
        print(f"  {description}:")
        print(f"    {command}")
        print()

    # Try to run some basic checks
    try:
        import setuptools
        packages = setuptools.find_packages(exclude=["tests*", "docs*"])
        print(f"Found packages: {packages}")
    except Exception as e:
        print(f"Could not check packages: {e}")

    print("\nModern packaging with build:")
    print("  pip install build")
    print("  python -m build")
    print("  # Creates both sdist and wheel in dist/")

    print("\nPublishing to PyPI:")
    print("  pip install twine")
    print("  twine check dist/*")
    print("  twine upload dist/*")


def main():
    """Run all packaging examples."""
    print("Python Packaging and Distribution Examples")
    print("=" * 50)
    print()

    # Create all packaging files
    create_setup_py_example()
    create_pyproject_toml_example()
    create_manifest_in_example()
    create_package_structure()
    create_readme_and_docs()
    demonstrate_packaging_commands()

    print("\n" + "=" * 50)
    print("Packaging examples completed!")
    print("\nCreated files:")
    print("- setup.py (traditional packaging)")
    print("- pyproject.toml (modern packaging)")
    print("- MANIFEST.in (additional files)")
    print("- mypackage/ (sample package structure)")
    print("- README.md (documentation)")
    print("- requirements.txt (dependencies)")
    print("- LICENSE (license file)")
    print("\nTo test the package:")
    print("  pip install -e .")
    print("  mypackage-cli --help")


if __name__ == "__main__":
    main()