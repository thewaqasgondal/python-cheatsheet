"""
Basic Python Data Structures Examples

This module demonstrates common Python data structures:
- Lists: Mutable ordered collections
- Tuples: Immutable ordered collections
- Dictionaries: Key-value mappings
- Sets: Unordered collections of unique elements
"""

# Lists - Mutable ordered collections
def list_examples():
    """Demonstrate list operations."""
    print("=== List Examples ===")

    # Creating lists
    fruits = ['apple', 'banana', 'cherry']
    numbers = [1, 2, 3, 4, 5]
    mixed = [1, 'hello', 3.14, True]

    print(f"Fruits: {fruits}")
    print(f"Numbers: {numbers}")
    print(f"Mixed: {mixed}")

    # List operations
    fruits.append('date')  # Add to end
    print(f"After append: {fruits}")

    fruits.insert(1, 'apricot')  # Insert at index
    print(f"After insert: {fruits}")

    fruits.remove('banana')  # Remove by value
    print(f"After remove: {fruits}")

    popped = fruits.pop()  # Remove and return last element
    print(f"Popped: {popped}, Remaining: {fruits}")

    # List comprehension
    squares = [x**2 for x in range(1, 6)]
    print(f"Squares: {squares}")

    # Filtering with comprehension
    even_squares = [x**2 for x in range(1, 11) if x**2 % 2 == 0]
    print(f"Even squares: {even_squares}")


# Tuples - Immutable ordered collections
def tuple_examples():
    """Demonstrate tuple operations."""
    print("\n=== Tuple Examples ===")

    # Creating tuples
    coordinates = (10, 20)
    person = ('Alice', 30, 'Engineer')
    single_element = (42,)  # Note the comma

    print(f"Coordinates: {coordinates}")
    print(f"Person: {person}")
    print(f"Single element: {single_element}")

    # Tuple unpacking
    x, y = coordinates
    print(f"Unpacked coordinates: x={x}, y={y}")

    name, age, job = person
    print(f"Unpacked person: {name}, {age}, {job}")

    # Tuples are immutable
    # coordinates[0] = 15  # This would raise TypeError

    # But you can create new tuples
    new_coordinates = (15, y)
    print(f"New coordinates: {new_coordinates}")


# Dictionaries - Key-value mappings
def dict_examples():
    """Demonstrate dictionary operations."""
    print("\n=== Dictionary Examples ===")

    # Creating dictionaries
    person = {
        'name': 'Bob',
        'age': 25,
        'city': 'New York'
    }

    # Alternative syntax
    scores = dict(math=95, science=87, english=92)

    print(f"Person dict: {person}")
    print(f"Scores dict: {scores}")

    # Accessing values
    print(f"Bob's age: {person['age']}")
    print(f"Math score: {scores.get('math')}")

    # Safe access with get()
    print(f"History score: {scores.get('history', 'Not found')}")

    # Adding/modifying values
    person['job'] = 'Developer'
    person['age'] = 26
    print(f"Updated person: {person}")

    # Dictionary comprehension
    squares_dict = {x: x**2 for x in range(1, 6)}
    print(f"Squares dict: {squares_dict}")

    # Iterating over dictionaries
    print("Person details:")
    for key, value in person.items():
        print(f"  {key}: {value}")


# Sets - Unordered collections of unique elements
def set_examples():
    """Demonstrate set operations."""
    print("\n=== Set Examples ===")

    # Creating sets
    fruits = {'apple', 'banana', 'cherry'}
    numbers = set([1, 2, 3, 3, 2])  # Duplicates removed

    print(f"Fruits set: {fruits}")
    print(f"Numbers set: {numbers}")

    # Set operations
    fruits.add('date')
    print(f"After add: {fruits}")

    fruits.remove('banana')
    print(f"After remove: {fruits}")

    # Set operations between sets
    set_a = {1, 2, 3, 4}
    set_b = {3, 4, 5, 6}

    print(f"Set A: {set_a}")
    print(f"Set B: {set_b}")
    print(f"Union: {set_a | set_b}")
    print(f"Intersection: {set_a & set_b}")
    print(f"Difference A-B: {set_a - set_b}")
    print(f"Difference B-A: {set_b - set_a}")
    print(f"Symmetric difference: {set_a ^ set_b}")


if __name__ == "__main__":
    list_examples()
    tuple_examples()
    dict_examples()
    set_examples()