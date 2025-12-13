import multiprocessing
import time

# A simple function that we will run in a process
def print_numbers():
    """Function to print numbers from 1 to 5 with a delay."""
    for i in range(1, 6):
        print(f"Number: {i}")
        time.sleep(1)  # Simulate a delay (could represent I/O or CPU-bound tasks)

# Another function to print letters
def print_letters():
    """Function to print letters A to E with a delay."""
    for letter in ['A', 'B', 'C', 'D', 'E']:
        print(f"Letter: {letter}")
        time.sleep(1)  # Simulate a delay

if __name__ == "__main__":
    # Create two separate processes for concurrent execution
    process1 = multiprocessing.Process(target=print_numbers)
    process2 = multiprocessing.Process(target=print_letters)

    # Start both processes
    process1.start()
    process2.start()

    # Wait for both processes to complete before moving forward
    process1.join()  # Wait for process1 to finish
    process2.join()  # Wait for process2 to finish

    # After both processes have finished, print this message
    print("Both processes have completed.")
