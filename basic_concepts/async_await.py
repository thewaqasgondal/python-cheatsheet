"""
Async/Await Examples in Python

This module demonstrates asynchronous programming in Python using asyncio.
Async programming allows for concurrent execution without blocking threads.
"""

import asyncio
import time
import aiohttp
import requests
from typing import List, Dict, Any


async def simple_async_function():
    """A simple async function that simulates I/O operation."""
    print("Starting async task...")
    await asyncio.sleep(1)  # Non-blocking sleep
    print("Async task completed!")
    return "Async result"


def synchronous_example():
    """Demonstrate synchronous execution."""
    print("=== Synchronous Execution ===")

    async def task(name: str, delay: float):
        print(f"Task {name} starting...")
        await asyncio.sleep(delay)
        print(f"Task {name} completed!")
        return f"Result from {name}"

    # Run synchronously (one after another)
    start_time = time.time()

    # This won't work as expected - we need asyncio.run()
    # But for demonstration, we'll show the concept
    print("Synchronous tasks would take ~3 seconds total")
    print("(Each task waits for the previous to complete)")


async def concurrent_tasks():
    """Demonstrate running multiple async tasks concurrently."""
    print("\n=== Concurrent Async Tasks ===")

    async def download_file(url: str, filename: str):
        """Simulate downloading a file."""
        print(f"Starting download: {filename}")
        await asyncio.sleep(2)  # Simulate download time
        print(f"Completed download: {filename}")
        return f"Downloaded {filename}"

    # Create multiple concurrent tasks
    tasks = [
        download_file("https://example.com/file1.txt", "file1.txt"),
        download_file("https://example.com/file2.txt", "file2.txt"),
        download_file("https://example.com/file3.txt", "file3.txt"),
    ]

    # Run all tasks concurrently
    start_time = time.time()
    results = await asyncio.gather(*tasks)
    end_time = time.time()

    print(f"All downloads completed in {end_time - start_time:.2f} seconds")
    print(f"Results: {results}")


async def async_with_timeout():
    """Demonstrate async operations with timeouts."""
    print("\n=== Async Operations with Timeouts ===")

    async def slow_operation(name: str, delay: float):
        print(f"Starting {name}...")
        await asyncio.sleep(delay)
        print(f"Completed {name}!")
        return f"Result from {name}"

    try:
        # Set a timeout for the operation
        result = await asyncio.wait_for(
            slow_operation("timeout_test", 3),
            timeout=2  # 2 second timeout
        )
        print(f"Success: {result}")
    except asyncio.TimeoutError:
        print("Operation timed out!")


async def producer_consumer_pattern():
    """Demonstrate producer-consumer pattern with async queues."""
    print("\n=== Producer-Consumer Pattern ===")

    async def producer(queue: asyncio.Queue, items: List[str]):
        """Produce items and put them in the queue."""
        for item in items:
            print(f"Producing: {item}")
            await queue.put(item)
            await asyncio.sleep(0.5)  # Simulate production time
        await queue.put(None)  # Signal end of production

    async def consumer(queue: asyncio.Queue, consumer_id: int):
        """Consume items from the queue."""
        while True:
            item = await queue.get()
            if item is None:  # End signal
                queue.put_nowait(None)  # Put back for other consumers
                break
            print(f"Consumer {consumer_id} processing: {item}")
            await asyncio.sleep(1)  # Simulate processing time

    # Create queue and tasks
    queue = asyncio.Queue()
    items = ["Task 1", "Task 2", "Task 3", "Task 4", "Task 5"]

    producer_task = producer(queue, items)
    consumer_tasks = [consumer(queue, i) for i in range(1, 3)]  # 2 consumers

    # Run producer and consumers concurrently
    await asyncio.gather(producer_task, *consumer_tasks)


async def async_comprehension():
    """Demonstrate async comprehensions (Python 3.6+)."""
    print("\n=== Async Comprehensions ===")

    async def async_square(n: int):
        await asyncio.sleep(0.1)  # Simulate async operation
        return n ** 2

    # Async list comprehension
    numbers = [1, 2, 3, 4, 5]
    squares = [await async_square(n) for n in numbers]
    print(f"Squares: {squares}")

    # Async generator expression
    async def async_range(n: int):
        for i in range(n):
            yield i
            await asyncio.sleep(0.1)

    # Collect results from async generator
    async_gen_squares = [x ** 2 async for x in async_range(5)]
    print(f"Async generator squares: {async_gen_squares}")


async def http_requests_example():
    """Demonstrate async HTTP requests."""
    print("\n=== Async HTTP Requests ===")

    async def fetch_url(session: aiohttp.ClientSession, url: str) -> Dict[str, Any]:
        """Fetch a URL asynchronously."""
        try:
            async with session.get(url) as response:
                return {
                    'url': url,
                    'status': response.status,
                    'content_length': len(await response.text())
                }
        except Exception as e:
            return {'url': url, 'error': str(e)}

    urls = [
        'https://httpbin.org/get',
        'https://httpbin.org/delay/1',
        'https://httpbin.org/delay/1',
    ]

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)

        for result in results:
            if 'error' in result:
                print(f"Error fetching {result['url']}: {result['error']}")
            else:
                print(f"Successfully fetched {result['url']}: "
                      f"Status {result['status']}, "
                      f"{result['content_length']} bytes")


async def main():
    """Main function to run all async examples."""
    print("Python Async/Await Examples")
    print("=" * 40)

    # Note: synchronous_example() is just for explanation
    synchronous_example()

    await concurrent_tasks()
    await async_with_timeout()
    await producer_consumer_pattern()
    await async_comprehension()

    # HTTP requests example (requires aiohttp)
    try:
        await http_requests_example()
    except ImportError:
        print("\n=== Async HTTP Requests ===")
        print("aiohttp not installed. Install with: pip install aiohttp")
        print("Example would demonstrate concurrent HTTP requests.")


if __name__ == "__main__":
    # Run the async examples
    asyncio.run(main())