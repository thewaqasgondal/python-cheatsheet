"""
Python Generators Examples

Generators are special functions that return an iterator that yields values one at a time,
instead of returning all values at once. This is memory-efficient for large datasets.
"""

import sys


def simple_generator():
    """A simple generator function."""
    print("Generator started")
    yield 1
    print("After first yield")
    yield 2
    print("After second yield")
    yield 3
    print("Generator finished")


def fibonacci_generator(limit):
    """Generator that yields Fibonacci numbers up to a limit."""
    a, b = 0, 1
    count = 0
    while count < limit:
        yield a
        a, b = b, a + b
        count += 1


def prime_generator():
    """Generator that yields prime numbers indefinitely."""
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True

    n = 2
    while True:
        if is_prime(n):
            yield n
        n += 1


def file_line_generator(filename):
    """Generator that yields lines from a file one at a time."""
    try:
        with open(filename, 'r') as file:
            for line in file:
                yield line.strip()
    except FileNotFoundError:
        yield f"Error: File '{filename}' not found"


def countdown_generator(n):
    """Generator that counts down from n to 0."""
    while n >= 0:
        yield n
        n -= 1


def memory_efficient_range(start, end, step=1):
    """Memory-efficient range generator."""
    current = start
    while current < end:
        yield current
        current += step


def generator_with_send():
    """Generator that can receive values via send()."""
    value = yield "Ready to receive"
    print(f"Received: {value}")

    value = yield f"Processed {value}"
    print(f"Received again: {value}")

    return "Generator finished"


def generator_pipeline():
    """Demonstrate generator pipelines (chaining generators)."""

    def numbers():
        for i in range(1, 11):
            yield i

    def squares(nums):
        for num in nums:
            yield num ** 2

    def even_only(nums):
        for num in nums:
            if num % 2 == 0:
                yield num

    # Create pipeline
    nums = numbers()
    squared = squares(nums)
    even_squared = even_only(squared)

    return list(even_squared)


def generator_expressions():
    """Demonstrate generator expressions (similar to list comprehensions)."""
    print("=== Generator Expressions ===")

    # Generator expression (parentheses instead of brackets)
    squares_gen = (x**2 for x in range(1, 6))
    print(f"Generator expression: {list(squares_gen)}")

    # Compare memory usage
    list_comp = [x**2 for x in range(1000)]
    gen_expr = (x**2 for x in range(1000))

    print(f"List comprehension size: {sys.getsizeof(list_comp)} bytes")
    print(f"Generator expression size: {sys.getsizeof(gen_expr)} bytes")

    # Filtering with generator expression
    even_squares = (x**2 for x in range(1, 11) if x**2 % 2 == 0)
    print(f"Even squares: {list(even_squares)}")

    # Multiple generators
    nested_gen = (y for x in range(3) for y in range(x*2, x*2 + 2))
    print(f"Nested generator: {list(nested_gen)}")


def demonstrate_memory_efficiency():
    """Show memory efficiency of generators vs lists."""
    print("\n=== Memory Efficiency Demo ===")

    # Large list (consumes more memory)
    large_list = [x**2 for x in range(100000)]
    print(f"Large list memory: {sys.getsizeof(large_list)} bytes")

    # Generator (memory efficient)
    large_gen = (x**2 for x in range(100000))
    print(f"Large generator memory: {sys.getsizeof(large_gen)} bytes")

    # Sum using list
    list_sum = sum([x**2 for x in range(100000)])
    print(f"Sum using list: {list_sum}")

    # Sum using generator
    gen_sum = sum(x**2 for x in range(100000))
    print(f"Sum using generator: {gen_sum}")


def main():
    """Demonstrate generator concepts."""

    print("=== Simple Generator ===")
    gen = simple_generator()
    print(f"Generator object: {gen}")

    print("Iterating through generator:")
    for value in gen:
        print(f"Received: {value}")

    print("\n=== Fibonacci Generator ===")
    fib_gen = fibonacci_generator(10)
    print(f"First 10 Fibonacci numbers: {list(fib_gen)}")

    print("\n=== Prime Generator ===")
    prime_gen = prime_generator()
    primes = []
    for _ in range(10):
        primes.append(next(prime_gen))
    print(f"First 10 primes: {primes}")

    print("\n=== Countdown Generator ===")
    countdown = countdown_generator(5)
    print(f"Countdown: {list(countdown)}")

    print("\n=== Memory Efficient Range ===")
    mem_range = memory_efficient_range(0, 10, 2)
    print(f"Even numbers 0-10: {list(mem_range)}")

    print("\n=== Generator with Send ===")
    gen_send = generator_with_send()
    print(next(gen_send))  # Start generator
    print(gen_send.send("Hello"))
    try:
        gen_send.send("World")
    except StopIteration as e:
        print(f"Generator returned: {e.value}")

    print("\n=== Generator Pipeline ===")
    pipeline_result = generator_pipeline()
    print(f"Pipeline result: {pipeline_result}")

    generator_expressions()
    demonstrate_memory_efficiency()

    print("\n=== File Line Generator ===")
    # Create a small test file
    with open('test_file.txt', 'w') as f:
        f.write("Line 1\nLine 2\nLine 3\n")

    for line in file_line_generator('test_file.txt'):
        print(f"File line: {line}")

    # Clean up
    import os
    os.remove('test_file.txt')


if __name__ == "__main__":
    main()