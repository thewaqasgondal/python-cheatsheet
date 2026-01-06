"""
Threading Introduction Example

This module demonstrates basic threading concepts in Python using the threading module.
Threading allows concurrent execution of multiple tasks, ideal for I/O-bound operations.
"""

import threading
import time


def print_numbers(thread_name: str, count: int = 5) -> None:
    """
    Print numbers with a delay to simulate work.

    Args:
        thread_name: Name identifier for the thread
        count: Number of iterations to perform
    """
    for i in range(1, count + 1):
        print(f"{thread_name}: Number {i}")
        time.sleep(1)  # Simulate I/O operation or other blocking task


def print_letters(thread_name: str, letters: list = None) -> None:
    """
    Print letters with a delay to simulate work.

    Args:
        thread_name: Name identifier for the thread
        letters: List of letters to print
    """
    if letters is None:
        letters = ['A', 'B', 'C', 'D', 'E']

    for letter in letters:
        print(f"{thread_name}: Letter {letter}")
        time.sleep(1)  # Simulate I/O operation


def worker_with_exception(thread_id: int) -> None:
    """
    Worker function that demonstrates exception handling in threads.

    Args:
        thread_id: Unique identifier for the thread
    """
    try:
        print(f"Thread {thread_id}: Starting work")
        if thread_id == 3:
            raise ValueError(f"Simulated error in thread {thread_id}")
        time.sleep(2)
        print(f"Thread {thread_id}: Work completed")
    except Exception as e:
        print(f"Thread {thread_id}: Error occurred - {e}")


def demonstrate_threading() -> None:
    """Demonstrate basic threading concepts."""
    print("=== Basic Threading Example ===")

    # Create thread objects with custom arguments
    thread1 = threading.Thread(target=print_numbers, args=("Thread-1", 3))
    thread2 = threading.Thread(target=print_letters, args=("Thread-2", ['X', 'Y', 'Z']))

    print("Starting threads...")
    thread1.start()
    thread2.start()

    # Wait for threads to complete
    thread1.join()
    thread2.join()

    print("Both threads completed.\n")


def demonstrate_thread_exceptions() -> None:
    """Demonstrate exception handling in threads."""
    print("=== Thread Exception Handling ===")

    threads = []
    for i in range(1, 4):
        thread = threading.Thread(target=worker_with_exception, args=(i,))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print("All threads completed (some with errors).\n")


def demonstrate_thread_info() -> None:
    """Show thread information and management."""
    print("=== Thread Information ===")

    def info_worker(name: str) -> None:
        print(f"Worker {name}: Thread name = {threading.current_thread().name}")
        print(f"Worker {name}: Thread ID = {threading.current_thread().ident}")
        print(f"Worker {name}: Is daemon = {threading.current_thread().daemon}")
        time.sleep(1)

    # Create threads with custom names
    thread_a = threading.Thread(target=info_worker, args=("A",), name="Worker-A")
    thread_b = threading.Thread(target=info_worker, args=("B",), name="Worker-B")

    print(f"Main thread: {threading.current_thread().name}")
    print(f"Active threads before start: {threading.active_count()}")

    thread_a.start()
    thread_b.start()

    thread_a.join()
    thread_b.join()

    print(f"Active threads after completion: {threading.active_count()}\n")


if __name__ == "__main__":
    demonstrate_threading()
    demonstrate_thread_exceptions()
    demonstrate_thread_info()
