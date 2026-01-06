"""
Performance Profiling and Optimization

This module demonstrates various techniques for profiling and optimizing
Python code performance, including CPU profiling, memory profiling,
and timing measurements.
"""

import cProfile
import pstats
import time
import timeit
from functools import wraps, lru_cache
import tracemalloc
import psutil
import os
from typing import Any, Callable, List, Optional
import numpy as np
import io
import sys


def timing_decorator(func: Callable) -> Callable:
    """Decorator to time function execution."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        print(f"{func.__name__} executed in {execution_time:.6f} seconds")
        return result
    return wrapper


def memory_usage_decorator(func: Callable) -> Callable:
    """Decorator to measure memory usage."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB

        result = func(*args, **kwargs)

        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_used = final_memory - initial_memory
        print(f"{func.__name__} used {memory_used:.2f} MB of memory")
        return result
    return wrapper


def fibonacci_recursive(n: int) -> int:
    """Inefficient recursive Fibonacci implementation."""
    if n <= 1:
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)


@lru_cache(maxsize=None)
def fibonacci_memoized(n: int) -> int:
    """Memoized Fibonacci implementation."""
    if n <= 1:
        return n
    return fibonacci_memoized(n - 1) + fibonacci_memoized(n - 2)


def fibonacci_iterative(n: int) -> int:
    """Iterative Fibonacci implementation."""
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def matrix_operations_example(size: int = 1000) -> np.ndarray:
    """Example of matrix operations for profiling."""
    # Create large matrices
    A = np.random.rand(size, size)
    B = np.random.rand(size, size)

    # Perform various operations
    C = A + B
    D = np.dot(A, B)
    E = np.linalg.inv(A + np.eye(size) * 0.1)

    return E


def data_processing_example(num_items: int = 100000) -> List[dict]:
    """Example data processing function for profiling."""
    data = []

    for i in range(num_items):
        item = {
            'id': i,
            'name': f'item_{i}',
            'value': np.random.rand(),
            'category': np.random.choice(['A', 'B', 'C', 'D']),
            'timestamp': time.time() + np.random.rand() * 86400  # Random time within a day
        }
        data.append(item)

    # Process data
    processed = []
    for item in data:
        if item['value'] > 0.5:
            processed_item = item.copy()
            processed_item['processed_value'] = item['value'] * 2
            processed_item['is_high_value'] = True
            processed.append(processed_item)

    return processed


def cprofile_example():
    """Demonstrate cProfile usage for CPU profiling."""
    print("=== cProfile CPU Profiling ===")

    # Profile Fibonacci functions
    print("Profiling recursive Fibonacci (n=30)...")
    profiler = cProfile.Profile()
    profiler.enable()
    result1 = fibonacci_recursive(30)
    profiler.disable()

    # Save stats to string
    s = io.StringIO()
    stats = pstats.Stats(profiler, stream=s).sort_stats('cumulative')
    stats.print_stats(10)  # Top 10 functions
    print(s.getvalue())

    print(f"Result: {result1}")
    print()

    print("Profiling memoized Fibonacci (n=30)...")
    profiler = cProfile.Profile()
    profiler.enable()
    result2 = fibonacci_memoized(30)
    profiler.disable()

    s = io.StringIO()
    stats = pstats.Stats(profiler, stream=s).sort_stats('cumulative')
    stats.print_stats(10)
    print(s.getvalue())

    print(f"Result: {result2}")
    print()

    # Profile data processing
    print("Profiling data processing...")
    profiler = cProfile.Profile()
    profiler.enable()
    result3 = data_processing_example(10000)
    profiler.disable()

    s = io.StringIO()
    stats = pstats.Stats(profiler, stream=s).sort_stats('cumulative')
    stats.print_stats(15)
    print(s.getvalue())

    print(f"Processed {len(result3)} items")


def timeit_examples():
    """Demonstrate timeit module for precise timing."""
    print("\n=== Timeit Precise Timing ===")

    # Compare Fibonacci implementations
    print("Comparing Fibonacci implementations (n=25)...")

    # Recursive (will be slow)
    recursive_time = timeit.timeit(
        'fibonacci_recursive(25)',
        globals=globals(),
        number=1
    )
    print(".6f")

    # Memoized
    memoized_time = timeit.timeit(
        'fibonacci_memoized(25)',
        globals=globals(),
        number=10
    )
    print(".6f")

    # Iterative
    iterative_time = timeit.timeit(
        'fibonacci_iterative(25)',
        globals=globals(),
        number=100
    )
    print(".6f")

    # Calculate speedup
    print(".1f")
    print(".1f")
    print()

    # Time small code snippets
    print("Timing small code snippets...")

    setup = """
import numpy as np
a = np.random.rand(1000, 1000)
b = np.random.rand(1000, 1000)
"""

    # List comprehension vs loop
    list_comp_time = timeit.timeit(
        '[x**2 for x in range(1000)]',
        number=1000
    )

    loop_time = timeit.timeit(
        '''
result = []
for x in range(1000):
    result.append(x**2)
        ''',
        number=1000
    )

    print(".6f")
    print(".6f")
    print(".1f")
    print()

    # Numpy operations
    numpy_time = timeit.timeit(
        'np.dot(a, b)',
        setup=setup,
        number=10
    )

    python_time = timeit.timeit(
        '''
result = [[0 for _ in range(1000)] for _ in range(1000)]
for i in range(1000):
    for j in range(1000):
        for k in range(1000):
            result[i][j] += a[i][k] * b[k][j]
        ''',
        setup=setup,
        number=1
    )

    print(".6f")
    print(".6f")
    print(".0f")


def memory_profiling():
    """Demonstrate memory profiling techniques."""
    print("\n=== Memory Profiling ===")

    # Using tracemalloc
    print("Using tracemalloc for memory tracing...")

    tracemalloc.start()

    # Take initial snapshot
    snapshot1 = tracemalloc.take_snapshot()

    # Run memory-intensive operation
    result = data_processing_example(50000)

    # Take second snapshot
    snapshot2 = tracemalloc.take_snapshot()

    # Compare snapshots
    stats = snapshot2.compare_to(snapshot1, 'lineno')
    print("Top memory allocations:")
    for stat in stats[:10]:
        print(f"  {stat.traceback.format()[0]}: {stat.size_diff / 1024:.1f} KB")

    tracemalloc.stop()
    print(f"Processed {len(result)} items")
    print()

    # Using psutil for system memory
    print("System memory usage monitoring...")

    process = psutil.Process(os.getpid())

    initial_memory = process.memory_info().rss / 1024 / 1024  # MB
    print(".1f")

    # Run matrix operations
    matrix_result = matrix_operations_example(500)

    final_memory = process.memory_info().rss / 1024 / 1024  # MB
    print(".1f")
    print(".1f")
    print()

    # Memory usage over time
    print("Memory usage over time:")
    memory_usage = []

    for i in range(10):
        # Create some data
        data = [np.random.rand(1000, 1000) for _ in range(10)]
        memory_usage.append(process.memory_info().rss / 1024 / 1024)

        # Clean up
        del data

    print("Memory usage samples (MB):", [".1f" for m in memory_usage])


@timing_decorator
@memory_usage_decorator
def optimized_function_example():
    """Example of an optimized function with decorators."""
    # Simulate some work
    data = []
    for i in range(10000):
        data.append({
            'id': i,
            'value': np.sin(i * 0.01) + np.random.normal(0, 0.1),
            'category': 'A' if i % 2 == 0 else 'B'
        })

    # Process data efficiently
    values = np.array([item['value'] for item in data])
    mean_val = np.mean(values)
    std_val = np.std(values)

    # Filter data
    filtered = [item for item in data if abs(item['value'] - mean_val) < std_val]

    return len(filtered), mean_val, std_val


def line_profiler_example():
    """Demonstrate line-by-line profiling (requires line_profiler)."""
    print("\n=== Line-by-Line Profiling ===")

    try:
        from line_profiler import LineProfiler

        def function_to_profile():
            """Function to profile line by line."""
            total = 0
            for i in range(10000):
                total += i ** 2
                if i % 1000 == 0:
                    time.sleep(0.001)  # Simulate I/O or computation
            return total

        # Create profiler
        profiler = LineProfiler()
        profiled_function = profiler(function_to_profile)

        # Run and profile
        result = profiled_function()

        # Print results
        profiler.print_stats()

        print(f"Function result: {result}")

    except ImportError:
        print("line_profiler not installed. Install with: pip install line_profiler")
        print("Example usage: kernprof -l script.py && python -m line_profiler script.py.lprof")


def optimization_techniques():
    """Demonstrate various optimization techniques."""
    print("\n=== Optimization Techniques ===")

    print("1. List comprehensions vs loops:")
    # Less efficient
    start = time.time()
    result1 = []
    for i in range(100000):
        if i % 2 == 0:
            result1.append(i * 2)
    time1 = time.time() - start

    # More efficient
    start = time.time()
    result2 = [i * 2 for i in range(100000) if i % 2 == 0]
    time2 = time.time() - start

    print(".6f")
    print(".6f")
    print(".1f")
    print()

    print("2. Numpy vectorization:")
    # Python loop
    start = time.time()
    a = list(range(1000000))
    b = list(range(1000000))
    result3 = [x + y for x, y in zip(a, b)]
    time3 = time.time() - start

    # Numpy vectorized
    start = time.time()
    a_np = np.arange(1000000)
    b_np = np.arange(1000000)
    result4 = a_np + b_np
    time4 = time.time() - start

    print(".6f")
    print(".6f")
    print(".1f")
    print()

    print("3. String concatenation:")
    # Inefficient
    start = time.time()
    result5 = ""
    for i in range(10000):
        result5 += str(i)
    time5 = time.time() - start

    # Efficient
    start = time.time()
    result6 = "".join(str(i) for i in range(10000))
    time6 = time.time() - start

    print(".6f")
    print(".6f")
    print(".1f")


def main():
    """Run all performance profiling examples."""
    print("Python Performance Profiling and Optimization")
    print("=" * 55)
    print()

    try:
        cprofile_example()
        timeit_examples()
        memory_profiling()

        print("\nDecorated function example:")
        optimized_function_example()

        line_profiler_example()
        optimization_techniques()

        print("\n" + "=" * 55)
        print("Performance profiling examples completed!")
        print("\nKey takeaways:")
        print("- Use cProfile for detailed CPU profiling")
        print("- Use timeit for precise timing measurements")
        print("- Use tracemalloc for memory tracing")
        print("- Consider line_profiler for line-by-line analysis")
        print("- Optimize with vectorization, comprehensions, and efficient data structures")

    except Exception as e:
        print(f"Error running profiling examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()