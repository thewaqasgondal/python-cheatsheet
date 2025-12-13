# Concurrency Examples

This directory contains examples demonstrating concurrent programming in Python.

## Files

### threading_intro.py
Introduction to Python's threading module for I/O-bound concurrent tasks.

**Features:**
- Basic thread creation
- Running multiple threads concurrently
- Thread synchronization with `join()`
- Demonstrates concurrent execution of print operations

**Usage:**
```bash
python threading_intro.py
```

**When to use Threading:**
- I/O-bound operations (file operations, network requests)
- Tasks that spend time waiting
- GUI applications that need to remain responsive

---

### multiprocessing_intro.py
Introduction to Python's multiprocessing module for CPU-bound tasks.

**Features:**
- Process creation and management
- True parallel execution across multiple CPU cores
- Bypasses Python's Global Interpreter Lock (GIL)
- Process synchronization

**Usage:**
```bash
python multiprocessing_intro.py
```

**When to use Multiprocessing:**
- CPU-intensive calculations
- Tasks that benefit from parallel processing
- Need to utilize multiple CPU cores
- Avoiding GIL limitations

## Key Differences

| Threading | Multiprocessing |
|-----------|----------------|
| Shares memory space | Separate memory spaces |
| Limited by GIL | Bypasses GIL |
| Lower overhead | Higher overhead |
| Best for I/O-bound | Best for CPU-bound |
| Concurrent execution | Parallel execution |
