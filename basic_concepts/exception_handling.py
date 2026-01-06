"""
Exception Handling Examples in Python

This module demonstrates best practices for exception handling in Python,
including custom exceptions, proper cleanup, and error recovery patterns.
"""

import sys
import os
import json
import logging
from typing import Optional, Dict, Any


# Custom Exceptions
class ValidationError(Exception):
    """Raised when data validation fails."""
    pass


class FileOperationError(Exception):
    """Raised when file operations fail."""
    pass


class NetworkError(Exception):
    """Raised when network operations fail."""
    pass


class InsufficientFundsError(Exception):
    """Raised when account has insufficient funds."""

    def __init__(self, balance: float, required: float):
        self.balance = balance
        self.required = required
        self.shortfall = required - balance
        super().__init__(f"Insufficient funds: balance ${balance:.2f}, "
                        f"required ${required:.2f}, shortfall ${self.shortfall:.2f}")


def basic_try_except():
    """Demonstrate basic try-except blocks."""
    print("=== Basic Try-Except ===")

    # Example 1: Handling division by zero
    try:
        result = 10 / 0
        print(f"Result: {result}")
    except ZeroDivisionError as e:
        print(f"Error: Cannot divide by zero - {e}")

    # Example 2: Handling file not found
    try:
        with open("nonexistent_file.txt", "r") as f:
            content = f.read()
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")

    # Example 3: Handling multiple exception types
    try:
        data = json.loads("invalid json")
    except (json.JSONDecodeError, TypeError) as e:
        print(f"Error: Invalid JSON - {e}")

    print()


def multiple_except_blocks():
    """Demonstrate handling different exceptions differently."""
    print("=== Multiple Except Blocks ===")

    test_cases = [
        ("10 / 0", lambda: 10 / 0),
        ("int('abc')", lambda: int('abc')),
        ("open('missing.txt')", lambda: open('missing.txt')),
        ("[1,2,3][10]", lambda: [1,2,3][10]),
    ]

    for description, operation in test_cases:
        try:
            result = operation()
            print(f"{description} = {result}")
        except ZeroDivisionError:
            print(f"{description} -> ZeroDivisionError: Cannot divide by zero")
        except ValueError:
            print(f"{description} -> ValueError: Invalid value")
        except FileNotFoundError:
            print(f"{description} -> FileNotFoundError: File not found")
        except IndexError:
            print(f"{description} -> IndexError: Index out of range")
        except Exception as e:
            print(f"{description} -> {type(e).__name__}: {e}")

    print()


def try_except_else_finally():
    """Demonstrate try-except-else-finally pattern."""
    print("=== Try-Except-Else-Finally ===")

    def process_file(filename: str) -> Optional[str]:
        file = None
        try:
            file = open(filename, 'r')
            content = file.read()
            # Only executed if no exception occurred
        except FileNotFoundError:
            print(f"File '{filename}' not found")
            return None
        except PermissionError:
            print(f"Permission denied for '{filename}'")
            return None
        else:
            # This block executes only if no exception in try block
            print(f"Successfully read {len(content)} characters from '{filename}'")
            return content
        finally:
            # This block always executes, regardless of exceptions
            if file:
                file.close()
                print(f"Closed file '{filename}'")

    # Test with existing file
    with open("temp_test.txt", "w") as f:
        f.write("Hello, World!")

    result = process_file("temp_test.txt")
    print(f"Result: {result}")

    # Test with non-existing file
    result = process_file("nonexistent.txt")
    print(f"Result: {result}")

    # Clean up
    if os.path.exists("temp_test.txt"):
        os.remove("temp_test.txt")

    print()


def custom_exceptions_example():
    """Demonstrate custom exceptions."""
    print("=== Custom Exceptions ===")

    def validate_user_data(user_data: Dict[str, Any]) -> None:
        """Validate user data and raise custom exceptions."""
        if not isinstance(user_data, dict):
            raise ValidationError("User data must be a dictionary")

        required_fields = ['name', 'age', 'email']
        for field in required_fields:
            if field not in user_data:
                raise ValidationError(f"Missing required field: {field}")

        if not isinstance(user_data['age'], int) or user_data['age'] < 0:
            raise ValidationError("Age must be a positive integer")

        if '@' not in user_data['email']:
            raise ValidationError("Invalid email format")

    def create_user_account(user_data: Dict[str, Any]) -> str:
        """Create a user account with validation."""
        try:
            validate_user_data(user_data)
            # Simulate account creation
            return f"Account created for {user_data['name']}"
        except ValidationError as e:
            raise  # Re-raise custom exception

    # Test cases
    test_users = [
        {"name": "Alice", "age": 25, "email": "alice@example.com"},  # Valid
        {"name": "Bob", "age": -5, "email": "bob@example.com"},     # Invalid age
        {"name": "Charlie", "email": "charlie@example.com"},       # Missing age
        {"name": "David", "age": 30, "email": "invalid-email"},    # Invalid email
    ]

    for user in test_users:
        try:
            result = create_user_account(user)
            print(f"✓ {result}")
        except ValidationError as e:
            print(f"✗ Validation failed: {e}")

    print()


def exception_chaining():
    """Demonstrate exception chaining with 'raise from'."""
    print("=== Exception Chaining ===")

    def convert_to_int(value: str) -> int:
        """Convert string to int with proper exception chaining."""
        try:
            return int(value)
        except ValueError as e:
            raise ValueError(f"Cannot convert '{value}' to integer") from e

    def process_data(data: str) -> int:
        """Process data with exception chaining."""
        try:
            return convert_to_int(data)
        except ValueError as e:
            raise RuntimeError("Data processing failed") from e

    # Test cases
    test_values = ["123", "abc", "45.67"]

    for value in test_values:
        try:
            result = process_data(value)
            print(f"'{value}' -> {result}")
        except RuntimeError as e:
            print(f"'{value}' -> Error: {e}")
            print(f"Caused by: {e.__cause__}")

    print()


def banking_example():
    """Demonstrate exception handling in a banking scenario."""
    print("=== Banking Example with Custom Exceptions ===")

    class BankAccount:
        def __init__(self, account_id: str, balance: float = 0.0):
            self.account_id = account_id
            self.balance = balance

        def deposit(self, amount: float) -> None:
            if amount <= 0:
                raise ValueError("Deposit amount must be positive")
            self.balance += amount
            print(f"Deposited ${amount:.2f}. New balance: ${self.balance:.2f}")

        def withdraw(self, amount: float) -> None:
            if amount <= 0:
                raise ValueError("Withdrawal amount must be positive")
            if amount > self.balance:
                raise InsufficientFundsError(self.balance, amount)
            self.balance -= amount
            print(f"Withdrew ${amount:.2f}. New balance: ${self.balance:.2f}")

        def transfer(self, target_account: 'BankAccount', amount: float) -> None:
            """Transfer money between accounts with rollback on failure."""
            # Start transaction
            original_balance = self.balance
            original_target_balance = target_account.balance

            try:
                self.withdraw(amount)
                target_account.deposit(amount)
                print(f"Successfully transferred ${amount:.2f} to account {target_account.account_id}")
            except InsufficientFundsError:
                # Transaction failed, but withdrawal already happened
                # In real banking, this would be handled by transaction rollback
                print("Transfer failed due to insufficient funds")
                raise
            except Exception as e:
                # Unexpected error - rollback
                self.balance = original_balance
                target_account.balance = original_target_balance
                print(f"Transfer failed due to unexpected error: {e}")
                raise RuntimeError("Transfer failed") from e

    # Create accounts
    account1 = BankAccount("ACC001", 1000.0)
    account2 = BankAccount("ACC002", 500.0)

    print(f"Initial balances: ACC001=${account1.balance}, ACC002=${account2.balance}")

    # Test various operations
    operations = [
        ("deposit", lambda: account1.deposit(200)),
        ("withdraw", lambda: account1.withdraw(1500)),  # Insufficient funds
        ("withdraw", lambda: account1.withdraw(300)),
        ("transfer", lambda: account1.transfer(account2, 200)),
        ("transfer", lambda: account2.transfer(account1, 1000)),  # Insufficient funds
    ]

    for op_name, operation in operations:
        try:
            print(f"\nTrying {op_name}...")
            operation()
        except (ValueError, InsufficientFundsError, RuntimeError) as e:
            print(f"Operation failed: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    print(f"\nFinal balances: ACC001=${account1.balance}, ACC002=${account2.balance}")
    print()


def logging_exceptions():
    """Demonstrate logging exceptions."""
    print("=== Logging Exceptions ===")

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    def risky_operation():
        """A function that might raise exceptions."""
        import random
        if random.choice([True, False]):
            raise ValueError("Random error occurred")
        return "Operation successful"

    def safe_operation():
        """Wrap risky operation with proper exception handling and logging."""
        try:
            result = risky_operation()
            logging.info(f"Operation succeeded: {result}")
            return result
        except Exception as e:
            logging.error(f"Operation failed: {e}", exc_info=True)
            # exc_info=True includes the full traceback
            return None

    # Test the safe operation multiple times
    for i in range(5):
        print(f"Attempt {i+1}: {safe_operation()}")

    print()


def main():
    """Run all exception handling demonstrations."""
    print("Python Exception Handling Examples")
    print("=" * 40)
    print()

    basic_try_except()
    multiple_except_blocks()
    try_except_else_finally()
    custom_exceptions_example()
    exception_chaining()
    banking_example()
    logging_exceptions()


if __name__ == "__main__":
    main()