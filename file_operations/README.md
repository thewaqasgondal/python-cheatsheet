# File Operations Examples

This directory contains examples for file handling and operating system operations in Python.

## Files

### file_analysis.py
Comprehensive file operations including metadata extraction and multi-format file reading.

**Features:**
- Get file metadata (size, creation time, modification time)
- Read various file formats (text, CSV, JSON)
- Copy, move, and delete files
- File and directory existence checks

**Usage:**
```bash
python file_analysis.py
```

**Functions included:**
- `get_file_metadata(file_path)` - Display file properties
- `read_file(file_path)` - Read text, CSV, or JSON files
- File manipulation utilities

---

### os_example.py
Demonstrates Python's `os` module for system-level operations.

**Features:**
- Get current working directory
- List directory contents
- Create and manage directories
- File operations (create, rename, delete)
- Path operations
- Environment variable access
- File system navigation

**Usage:**
```bash
python os_example.py
```

**Key Operations:**
- `os.getcwd()` - Get current directory
- `os.listdir()` - List directory contents
- `os.mkdir()` - Create directories
- `os.path.join()` - Join path components
- `os.rename()` - Rename files/directories
- `os.remove()` - Delete files

## Best Practices

1. Always check if files/directories exist before operations
2. Use `os.path.join()` for cross-platform path handling
3. Handle exceptions appropriately
4. Close file handles properly (use context managers)
5. Use `pathlib` for modern path operations (Python 3.4+)
