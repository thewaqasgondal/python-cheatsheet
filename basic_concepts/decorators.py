"""
Python Decorators Examples

Decorators are functions that modify the behavior of other functions or classes.
They allow you to wrap another function to extend its behavior without permanently
modifying it.
"""

import time
import functools


def simple_decorator(func):
    """A simple decorator that prints before and after function execution."""
    def wrapper(*args, **kwargs):
        print(f"Before calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"After calling {func.__name__}")
        return result
    return wrapper


@simple_decorator
def greet(name):
    """A simple greeting function."""
    print(f"Hello, {name}!")
    return f"Greeted {name}"


def timing_decorator(func):
    """Decorator that measures and prints execution time."""
    @functools.wraps(func)  # Preserves original function metadata
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.4f} seconds to execute")
        return result
    return wrapper


@timing_decorator
def slow_function():
    """A function that takes some time to execute."""
    time.sleep(1)
    print("Slow function completed")


@timing_decorator
def fibonacci(n):
    """Calculate the nth Fibonacci number (inefficiently)."""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)


def logging_decorator(func):
    """Decorator that logs function calls with arguments."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_str = ', '.join(repr(arg) for arg in args)
        kwargs_str = ', '.join(f"{k}={v!r}" for k, v in kwargs.items())
        all_args = ', '.join(filter(None, [args_str, kwargs_str]))

        print(f"Calling {func.__name__}({all_args})")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result!r}")
        return result
    return wrapper


@logging_decorator
def add_numbers(a, b, c=0):
    """Add three numbers together."""
    return a + b + c


@logging_decorator
def multiply(a, b):
    """Multiply two numbers."""
    return a * b


def cache_decorator(func):
    """Decorator that caches function results."""
    cache = {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Create a cache key from arguments
        key = (args, tuple(sorted(kwargs.items())))

        if key in cache:
            print(f"Cache hit for {func.__name__}{key}")
            return cache[key]

        print(f"Computing {func.__name__}{key}")
        result = func(*args, **kwargs)
        cache[key] = result
        return result

    return wrapper


@cache_decorator
def expensive_computation(n):
    """Simulate an expensive computation."""
    time.sleep(0.5)  # Simulate computation time
    return n ** 2


def require_authentication(permission_level):
    """Parameterized decorator that checks permissions."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(user, *args, **kwargs):
            if user.get('permission_level', 0) < permission_level:
                raise PermissionError(f"User lacks required permission level {permission_level}")
            return func(user, *args, **kwargs)
        return wrapper
    return decorator


@require_authentication(permission_level=2)
def access_sensitive_data(user):
    """Function that requires high permission level."""
    return "Sensitive data accessed"


def class_decorator(cls):
    """Decorator that can be applied to classes."""
    # Add a class attribute
    cls.decorated = True

    # Add an instance method
    def new_method(self):
        return f"This is a new method added by decorator to {cls.__name__}"

    cls.new_method = new_method
    return cls


@class_decorator
class MyClass:
    """A simple class."""

    def __init__(self, value):
        self.value = value

    def original_method(self):
        return f"Original method with value: {self.value}"


def main():
    """Demonstrate all decorators."""

    print("=== Simple Decorator ===")
    greet("Alice")

    print("\n=== Timing Decorator ===")
    slow_function()
    print(f"Fibonacci(10): {fibonacci(10)}")

    print("\n=== Logging Decorator ===")
    result1 = add_numbers(1, 2, c=3)
    result2 = multiply(4, 5)

    print("\n=== Caching Decorator ===")
    print(f"First call: {expensive_computation(5)}")
    print(f"Second call (cached): {expensive_computation(5)}")
    print(f"Third call (different arg): {expensive_computation(6)}")

    print("\n=== Parameterized Decorator ===")
    user_low = {'name': 'Bob', 'permission_level': 1}
    user_high = {'name': 'Alice', 'permission_level': 3}

    try:
        access_sensitive_data(user_low)
    except PermissionError as e:
        print(f"Access denied: {e}")

    try:
        result = access_sensitive_data(user_high)
        print(f"Access granted: {result}")
    except PermissionError as e:
        print(f"Access denied: {e}")

    print("\n=== Class Decorator ===")
    obj = MyClass(42)
    print(obj.original_method())
    print(obj.new_method())
    print(f"Class decorated: {MyClass.decorated}")


if __name__ == "__main__":
    main()