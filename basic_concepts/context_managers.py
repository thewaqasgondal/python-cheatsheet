"""
Context Managers Examples in Python

Context managers provide a way to allocate and release resources precisely.
They ensure proper cleanup even when errors occur, using the 'with' statement.
"""

import os
import time
import tempfile
import threading
from contextlib import contextmanager, closing
from typing import Generator, Any


class FileManager:
    """Custom context manager for file operations."""

    def __init__(self, filename: str, mode: str = 'r'):
        self.filename = filename
        self.mode = mode
        self.file = None

    def __enter__(self):
        """Enter the context - open the file."""
        self.file = open(self.filename, self.mode)
        print(f"Opened file: {self.filename}")
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the context - close the file."""
        if self.file:
            self.file.close()
            print(f"Closed file: {self.filename}")

        # Return False to propagate exceptions, True to suppress them
        return False


@contextmanager
def timer_context(name: str = "operation"):
    """Context manager that times the execution of code block."""
    start_time = time.time()
    print(f"Starting {name}...")
    try:
        yield
    finally:
        end_time = time.time()
        elapsed = end_time - start_time
        print(f"{name} completed in {elapsed:.4f} seconds")


@contextmanager
def temporary_directory():
    """Context manager that creates and cleans up a temporary directory."""
    temp_dir = tempfile.mkdtemp()
    print(f"Created temporary directory: {temp_dir}")
    try:
        yield temp_dir
    finally:
        # Clean up the temporary directory
        import shutil
        shutil.rmtree(temp_dir)
        print(f"Cleaned up temporary directory: {temp_dir}")


@contextmanager
def database_connection(db_path: str):
    """Simulate a database connection context manager."""
    print(f"Connecting to database: {db_path}")
    # Simulate connection
    connection = {"connected": True, "path": db_path}

    try:
        yield connection
    except Exception as e:
        print(f"Database error: {e}")
        # Could implement rollback here
        raise
    finally:
        # Always close connection
        connection["connected"] = False
        print(f"Closed database connection: {db_path}")


class Indenter:
    """Context manager for managing indentation levels."""

    def __init__(self, indent_size: int = 4):
        self.indent_size = indent_size
        self.level = 0

    def __enter__(self):
        self.level += 1
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.level -= 1

    def print(self, text: str):
        """Print text with current indentation."""
        indent = " " * (self.level * self.indent_size)
        print(f"{indent}{text}")


@contextmanager
def redirect_stdout_to_file(filename: str):
    """Context manager to redirect stdout to a file."""
    import sys
    from io import StringIO

    # Save original stdout
    original_stdout = sys.stdout

    try:
        with open(filename, 'w') as f:
            # Redirect stdout to file
            sys.stdout = f
            yield f
    finally:
        # Restore original stdout
        sys.stdout = original_stdout


class LockManager:
    """Context manager for thread synchronization."""

    def __init__(self):
        self.lock = threading.Lock()

    def __enter__(self):
        self.lock.acquire()
        print("Lock acquired")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.lock.release()
        print("Lock released")


def demonstrate_file_manager():
    """Demonstrate custom file context manager."""
    print("=== Custom File Context Manager ===")

    # Create a test file
    test_file = "test_context.txt"
    with open(test_file, 'w') as f:
        f.write("Hello, Context Manager!")

    # Use our custom context manager
    with FileManager(test_file, 'r') as f:
        content = f.read()
        print(f"File content: {content}")

    # File is automatically closed
    print("File operations completed\n")

    # Clean up
    os.remove(test_file)


def demonstrate_timer():
    """Demonstrate timing context manager."""
    print("=== Timer Context Manager ===")

    with timer_context("file processing"):
        time.sleep(0.5)
        print("Processing files...")

    with timer_context("database query"):
        time.sleep(0.2)
        print("Querying database...")

    print()


def demonstrate_temp_directory():
    """Demonstrate temporary directory context manager."""
    print("=== Temporary Directory Context Manager ===")

    with temporary_directory() as temp_dir:
        # Create some files in the temp directory
        test_file = os.path.join(temp_dir, "test.txt")
        with open(test_file, 'w') as f:
            f.write("This will be cleaned up automatically")

        print(f"Created file in temp dir: {test_file}")
        print(f"Files in temp dir: {os.listdir(temp_dir)}")

    # Directory and files are automatically cleaned up
    print()


def demonstrate_database_simulation():
    """Demonstrate database connection simulation."""
    print("=== Database Connection Context Manager ===")

    try:
        with database_connection("mydb.sqlite") as conn:
            print(f"Connection status: {conn}")
            # Simulate some database operations
            print("Executing queries...")
            time.sleep(0.1)

            # Simulate an error
            if True:  # Change to False to see normal operation
                raise ValueError("Simulated database error")

    except ValueError as e:
        print(f"Handled error: {e}")

    print()


def demonstrate_indenter():
    """Demonstrate indentation context manager."""
    print("=== Indentation Context Manager ===")

    with Indenter() as indent:
        indent.print("Level 1")
        with Indenter():
            indent.print("Level 2")
            with Indenter():
                indent.print("Level 3")
                indent.print("Still level 3")
            indent.print("Back to level 2")
        indent.print("Back to level 1")

    print()


def demonstrate_stdout_redirect():
    """Demonstrate stdout redirection context manager."""
    print("=== Stdout Redirection Context Manager ===")

    print("This will appear in console")
    with redirect_stdout_to_file("redirected_output.txt"):
        print("This will go to the file")
        print("So will this line")

    print("This will appear in console again")

    # Read the redirected output
    with open("redirected_output.txt", 'r') as f:
        content = f.read()
        print(f"Content written to file: {repr(content)}")

    # Clean up
    os.remove("redirected_output.txt")
    print()


def demonstrate_lock_manager():
    """Demonstrate thread lock context manager."""
    print("=== Thread Lock Context Manager ===")

    lock_manager = LockManager()

    def worker_thread(thread_id: int):
        with lock_manager:
            print(f"Thread {thread_id} is working")
            time.sleep(0.5)
            print(f"Thread {thread_id} finished")

    # Create and start threads
    threads = []
    for i in range(3):
        t = threading.Thread(target=worker_thread, args=(i,))
        threads.append(t)
        t.start()

    # Wait for all threads to complete
    for t in threads:
        t.join()

    print()


def demonstrate_contextlib_closing():
    """Demonstrate contextlib.closing for objects without context managers."""
    print("=== contextlib.closing Example ===")

    class CustomResource:
        """A resource that doesn't have __enter__/__exit__ but needs cleanup."""
        def __init__(self, name: str):
            self.name = name
            print(f"Resource {name} created")

        def use(self):
            print(f"Using resource {self.name}")

        def close(self):
            print(f"Resource {self.name} closed")

    # Without context manager
    resource = CustomResource("manual")
    try:
        resource.use()
    finally:
        resource.close()

    print()

    # With contextlib.closing
    with closing(CustomResource("automatic")) as resource:
        resource.use()
    # close() is called automatically

    print()


def main():
    """Run all context manager demonstrations."""
    print("Python Context Managers Examples")
    print("=" * 40)
    print()

    demonstrate_file_manager()
    demonstrate_timer()
    demonstrate_temp_directory()
    demonstrate_database_simulation()
    demonstrate_indenter()
    demonstrate_stdout_redirect()
    demonstrate_lock_manager()
    demonstrate_contextlib_closing()


if __name__ == "__main__":
    main()