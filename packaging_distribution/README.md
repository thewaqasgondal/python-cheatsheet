# Packaging and Distribution Examples

This directory contains comprehensive examples of Python packaging and distribution practices.

## Files

- `setup_pyproject_examples.py` - Complete packaging tutorial covering setup.py, pyproject.toml, and distribution

## Prerequisites

```bash
pip install setuptools>=61.0
pip install wheel>=0.37.0
pip install build>=0.8.0  # For modern builds
pip install twine>=4.0.0  # For PyPI uploads
```

## Topics Covered

### setup_pyproject_examples.py

#### Traditional Packaging (setup.py)
- Complete setup.py with all configuration options
- Package metadata and classifiers
- Dependencies and optional dependencies
- Entry points for console scripts
- Package data inclusion/exclusion
- License and author information

#### Modern Packaging (pyproject.toml)
- PEP 621 project metadata
- Build system configuration
- Tool configurations (black, isort, mypy, pytest, coverage)
- Optional dependencies groups
- Entry points and scripts
- Package discovery and data inclusion

#### Package Structure
- Proper package layout with __init__.py
- Module organization (core, utils, cli)
- Package data directories
- CLI module structure

#### Distribution Files
- MANIFEST.in for additional file inclusion
- README.md with comprehensive documentation
- requirements.txt for dependencies
- LICENSE file

#### Packaging Commands
- Building source distributions and wheels
- Validation and testing
- PyPI upload procedures
- Development workflow commands

## Running the Examples

```bash
python packaging_distribution/setup_pyproject_examples.py
```

This will create a complete sample package structure with:
- `setup.py` - Traditional packaging configuration
- `pyproject.toml` - Modern packaging standards
- `MANIFEST.in` - Additional file inclusion rules
- `mypackage/` - Sample package with modules and data
- `README.md` - Package documentation
- `requirements.txt` - Dependencies
- `LICENSE` - License file

## Key Concepts

### Package Structure
```
myproject/
├── pyproject.toml          # Modern packaging config
├── setup.py               # Traditional packaging (optional)
├── MANIFEST.in            # Additional files
├── README.md              # Documentation
├── LICENSE                # License
├── requirements.txt       # Dependencies
└── mypackage/             # Package directory
    ├── __init__.py        # Package init
    ├── core.py            # Main functionality
    ├── utils.py           # Utilities
    ├── cli/               # CLI modules
    │   ├── __init__.py
    │   └── main.py
    └── data/              # Package data
        └── config.json
```

### Build Systems

#### setuptools (Traditional)
```python
from setuptools import setup, find_packages

setup(
    name="mypackage",
    version="1.0.0",
    packages=find_packages(),
    install_requires=["requests"],
    entry_points={"console_scripts": ["mycli=mypackage.cli:main"]},
)
```

#### Modern (pyproject.toml)
```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "mypackage"
version = "1.0.0"
dependencies = ["requests"]
```

### Entry Points
```toml
[project.scripts]
mycli = "mypackage.cli:main"

[project.gui-scripts]  # For GUI apps on Windows
mygui = "mypackage.gui:main"
```

### Tool Configurations
```toml
[tool.black]
line-length = 88
target-version = ['py38']

[tool.mypy]
python_version = "3.8"
disallow_untyped_defs = true

[tool.pytest.ini_options]
addopts = "-ra -q --cov=mypackage"
```

## Building and Distributing

### Local Development
```bash
# Install in development mode
pip install -e .

# Install with development dependencies
pip install -e ".[dev]"

# Install with all optional dependencies
pip install -e ".[dev,docs,test]"
```

### Building Distributions
```bash
# Modern build (recommended)
pip install build
python -m build

# Traditional build
python setup.py sdist bdist_wheel
```

### Publishing to PyPI
```bash
# Install twine
pip install twine

# Check distributions
twine check dist/*

# Upload to PyPI
twine upload dist/*

# Upload to Test PyPI first
twine upload --repository testpypi dist/*
```

## Best Practices

1. **Use pyproject.toml** for new projects (PEP 621)
2. **Include comprehensive metadata** (description, classifiers, keywords)
3. **Specify Python version requirements** with `python_requires`
4. **Use entry points** for console scripts instead of scripts
5. **Include package data** properly with `include_package_data`
6. **Test your package** before publishing
7. **Use semantic versioning** (MAJOR.MINOR.PATCH)
8. **Keep dependencies minimal** and version-pinned appropriately

## Common Issues and Solutions

### Package Not Found
- Ensure `__init__.py` files exist in all package directories
- Check `packages` configuration in setup.py/pyproject.toml

### Data Files Not Included
- Use `include_package_data = true` in pyproject.toml
- Or configure `package_data` in setup.py
- Use MANIFEST.in for non-Python files

### Import Errors After Installation
- Test imports in a virtual environment
- Check for circular imports
- Ensure all dependencies are listed

### PyPI Upload Issues
- Use `twine check` before uploading
- Ensure version is unique
- Check for required metadata fields

## Advanced Topics

- **Namespace packages** for splitting large packages
- **Plugin systems** using entry points
- **Conditional dependencies** based on Python version/platform
- **Extension modules** with Cython/C extensions
- **Platform-specific wheels** for compiled extensions