
# Python Cheatsheet

A collection of useful Python code snippets, tips, and tricks for beginners and developers. This cheatsheet covers basic syntax, data structures, algorithms, essential libraries, and includes examples on **threading** and **multiprocessing** to help you understand how to run tasks concurrently in Python.

---

## Usage

Clone this repository to explore a wide range of Python examples and learn how to implement them.

```bash
git clone https://github.com/your-username/python-cheatsheet.git
cd python-cheatsheet
````

---

## Introduction to Threading

This section demonstrates the use of **threading** in Python, allowing multiple tasks to run concurrently within the same program. It uses Python's built-in `threading` module to create and manage threads.

### Python Threading Example

The script `threading_intro.py` includes two functions that print numbers and letters with delays. These functions run in parallel using threads, showing how to execute tasks concurrently.

### How It Works:

* **Thread Creation**: Two threads are created to run the functions `print_numbers()` and `print_letters()`.
* **Thread Starting**: Threads are started with the `start()` method.
* **Thread Joining**: We use `join()` to ensure the main program waits for the threads to finish before exiting.

### To Run the Program:

1. Clone or download the repository.
2. Navigate to the folder containing the `threading_intro.py` script.
3. Run the script with Python:

   ```bash
   python threading_intro.py
   ```

---

## Introduction to Multiprocessing

This section demonstrates how to use Python's built-in `multiprocessing` module to run tasks concurrently across multiple processes. This is particularly useful for **CPU-bound** tasks where threading may not be effective due to Python’s **Global Interpreter Lock (GIL)**.

### Python Multiprocessing Example

In the script `multiprocessing_intro.py`, we create two separate processes: one prints numbers from 1 to 5, and the other prints letters from A to E. Both functions include a 1-second delay, and the processes run in parallel to demonstrate how multiprocessing works.

### How It Works:

* **Processes**: Two separate processes are created to run `print_numbers()` and `print_letters()` functions.
* **Concurrency**: Both processes run at the same time, allowing for improved performance by using multiple CPU cores.
* **Synchronization**: The `join()` method ensures the main program waits until both processes are finished before it exits.

### To Run the Program:

1. Clone or download the repository.
2. Navigate to the folder containing the `multiprocessing_intro.py` script.
3. Run the script with Python:

   ```bash
   python multiprocessing_intro.py
   ```

---

## Contributing

Feel free to contribute to this repository by adding more examples, improving existing ones, or suggesting new ideas. Fork the repo and create a pull request!

---

## License

This project is licensed under the MIT License.

```

