"""
Command-Line Argument Parsing with argparse

This module demonstrates comprehensive usage of Python's argparse module
for building command-line interfaces.
"""

import argparse
import sys
import os
from typing import List, Optional, Any


def basic_argument_parser():
    """Demonstrate basic argument parsing."""
    print("=== Basic Argument Parser ===")

    # Create parser
    parser = argparse.ArgumentParser(
        description="A simple command-line tool",
        epilog="Example: python script.py --name Alice --count 5"
    )

    # Add arguments
    parser.add_argument('--name', '-n',
                       type=str,
                       default='World',
                       help='Name to greet (default: World)')

    parser.add_argument('--count', '-c',
                       type=int,
                       default=1,
                       help='Number of times to greet (default: 1)')

    parser.add_argument('--verbose', '-v',
                       action='store_true',
                       help='Enable verbose output')

    # Parse arguments (in real script, use sys.argv)
    test_args = ['--name', 'Alice', '--count', '3', '--verbose']
    args = parser.parse_args(test_args)

    print(f"Parsed arguments: name='{args.name}', count={args.count}, verbose={args.verbose}")

    # Use the arguments
    for i in range(args.count):
        greeting = f"Hello, {args.name}!"
        if args.verbose:
            greeting += f" (greeting #{i+1})"
        print(greeting)

    print()


def positional_arguments():
    """Demonstrate positional arguments."""
    print("=== Positional Arguments ===")

    parser = argparse.ArgumentParser(description="Calculator tool")

    # Positional arguments
    parser.add_argument('operation',
                       choices=['add', 'subtract', 'multiply', 'divide'],
                       help='Mathematical operation to perform')

    parser.add_argument('numbers',
                       nargs='+',  # One or more numbers
                       type=float,
                       help='Numbers to operate on')

    # Parse test arguments
    test_args = ['add', '10', '20', '5']
    args = parser.parse_args(test_args)

    print(f"Operation: {args.operation}")
    print(f"Numbers: {args.numbers}")

    # Perform calculation
    if args.operation == 'add':
        result = sum(args.numbers)
    elif args.operation == 'subtract':
        result = args.numbers[0] - sum(args.numbers[1:])
    elif args.operation == 'multiply':
        result = 1
        for num in args.numbers:
            result *= num
    elif args.operation == 'divide':
        result = args.numbers[0]
        for num in args.numbers[1:]:
            if num == 0:
                print("Error: Division by zero!")
                return
            result /= num

    print(f"Result: {result}")
    print()


def file_arguments():
    """Demonstrate file path arguments with validation."""
    print("=== File Arguments ===")

    parser = argparse.ArgumentParser(description="File processing tool")

    parser.add_argument('input_file',
                       type=str,
                       help='Input file path')

    parser.add_argument('--output', '-o',
                       type=str,
                       help='Output file path (default: input_file.out)')

    parser.add_argument('--force', '-f',
                       action='store_true',
                       help='Overwrite output file if it exists')

    # Custom validation function
    def validate_file(path: str) -> str:
        """Validate that file exists and is readable."""
        if not os.path.exists(path):
            raise argparse.ArgumentTypeError(f"File does not exist: {path}")
        if not os.path.isfile(path):
            raise argparse.ArgumentTypeError(f"Path is not a file: {path}")
        if not os.access(path, os.R_OK):
            raise argparse.ArgumentTypeError(f"File is not readable: {path}")
        return path

    # Reconfigure parser with validation
    parser = argparse.ArgumentParser(description="File processing tool")
    parser.add_argument('input_file',
                       type=validate_file,
                       help='Input file path')

    parser.add_argument('--output', '-o',
                       type=str,
                       help='Output file path')

    parser.add_argument('--force', '-f',
                       action='store_true',
                       help='Overwrite output file if it exists')

    # Create a test file
    test_file = 'test_input.txt'
    with open(test_file, 'w') as f:
        f.write("This is test content.\nLine 2\nLine 3")

    try:
        # Test with valid file
        test_args = [test_file, '--output', 'output.txt']
        args = parser.parse_args(test_args)

        print(f"Input file: {args.input_file}")
        print(f"Output file: {args.output or args.input_file + '.out'}")
        print(f"Force overwrite: {args.force}")

        # Simulate file processing
        with open(args.input_file, 'r') as f:
            content = f.read()
            print(f"Read {len(content)} characters from input file")

    except SystemExit:
        print("Argument parsing failed")
    finally:
        # Cleanup
        if os.path.exists(test_file):
            os.remove(test_file)

    print()


def mutually_exclusive_groups():
    """Demonstrate mutually exclusive argument groups."""
    print("=== Mutually Exclusive Groups ===")

    parser = argparse.ArgumentParser(description="Data processing tool")

    # Add regular arguments
    parser.add_argument('--input', '-i',
                       type=str,
                       help='Input file')

    parser.add_argument('--verbose', '-v',
                       action='store_true',
                       help='Enable verbose output')

    # Create mutually exclusive group
    group = parser.add_mutually_exclusive_group()

    group.add_argument('--quiet', '-q',
                      action='store_true',
                      help='Suppress all output')

    group.add_argument('--debug',
                      action='store_true',
                      help='Enable debug output')

    # Test valid combinations
    test_cases = [
        ['--input', 'data.txt', '--verbose'],
        ['--input', 'data.txt', '--quiet'],
        ['--input', 'data.txt', '--debug'],
        # This would fail: ['--input', 'data.txt', '--quiet', '--debug']
    ]

    for test_args in test_cases:
        try:
            args = parser.parse_args(test_args)
            print(f"✓ Valid: {test_args}")
            print(f"  quiet={args.quiet}, debug={args.debug}, verbose={args.verbose}")
        except SystemExit:
            print(f"✗ Invalid: {test_args}")

    print()


def subparsers_example():
    """Demonstrate subcommands with subparsers."""
    print("=== Subcommands with Subparsers ===")

    # Create main parser
    parser = argparse.ArgumentParser(description="Task management tool")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Create parser for "add" command
    add_parser = subparsers.add_parser('add', help='Add a new task')
    add_parser.add_argument('title', help='Task title')
    add_parser.add_argument('--priority', '-p',
                           choices=['low', 'medium', 'high'],
                           default='medium',
                           help='Task priority')
    add_parser.add_argument('--due-date',
                           help='Due date (YYYY-MM-DD)')

    # Create parser for "list" command
    list_parser = subparsers.add_parser('list', help='List tasks')
    list_parser.add_argument('--status',
                            choices=['pending', 'completed', 'all'],
                            default='all',
                            help='Filter by status')
    list_parser.add_argument('--priority',
                            help='Filter by priority')

    # Create parser for "complete" command
    complete_parser = subparsers.add_parser('complete', help='Mark task as completed')
    complete_parser.add_argument('task_id',
                                type=int,
                                help='Task ID to complete')

    # Test different commands
    test_commands = [
        ['add', 'Write documentation', '--priority', 'high'],
        ['list', '--status', 'pending'],
        ['complete', '1'],
        ['list'],  # Default command
    ]

    for test_args in test_commands:
        try:
            args = parser.parse_args(test_args)
            print(f"Command: {args.command}")
            print(f"Arguments: {vars(args)}")
            print()
        except SystemExit:
            print(f"Failed to parse: {test_args}")
            print()


def custom_actions():
    """Demonstrate custom argument actions."""
    print("=== Custom Actions ===")

    class ValidateRange(argparse.Action):
        """Custom action to validate numeric range."""

        def __init__(self, option_strings, dest, min_val=None, max_val=None, **kwargs):
            self.min_val = min_val
            self.max_val = max_val
            super().__init__(option_strings, dest, **kwargs)

        def __call__(self, parser, namespace, values, option_string=None):
            # Validate the value
            if self.min_val is not None and values < self.min_val:
                raise argparse.ArgumentError(self, f"Value must be >= {self.min_val}")
            if self.max_val is not None and values > self.max_val:
                raise argparse.ArgumentError(self, f"Value must be <= {self.max_val}")

            # Store the value
            setattr(namespace, self.dest, values)

    parser = argparse.ArgumentParser(description="Custom action example")

    parser.add_argument('--port', '-p',
                       action=ValidateRange,
                       type=int,
                       min_val=1024,
                       max_val=65535,
                       default=8080,
                       help='Port number (1024-65535)')

    parser.add_argument('--count',
                       action=ValidateRange,
                       type=int,
                       min_val=1,
                       max_val=100,
                       default=10,
                       help='Count (1-100)')

    # Test valid and invalid values
    test_cases = [
        (['--port', '8080', '--count', '5'], "Valid values"),
        (['--port', '80'], "Invalid port (too low)"),
        (['--count', '150'], "Invalid count (too high)"),
    ]

    for test_args, description in test_cases:
        try:
            args = parser.parse_args(test_args)
            print(f"✓ {description}: port={args.port}, count={args.count}")
        except SystemExit:
            print(f"✗ {description}: {test_args}")

    print()


def configuration_files():
    """Demonstrate loading configuration from files."""
    print("=== Configuration Files ===")

    import configparser

    # Create a sample config file
    config_content = """
[DEFAULT]
verbose = false
output_dir = ./output

[database]
host = localhost
port = 5432
name = myapp

[logging]
level = INFO
file = app.log
"""

    config_file = 'example.ini'
    with open(config_file, 'w') as f:
        f.write(config_content.strip())

    try:
        # Read config
        config = configparser.ConfigParser()
        config.read(config_file)

        # Create parser with config defaults
        parser = argparse.ArgumentParser(description="Config-aware application")

        # Database options
        parser.add_argument('--db-host',
                           default=config.get('database', 'host'),
                           help='Database host')

        parser.add_argument('--db-port',
                           type=int,
                           default=config.getint('database', 'port'),
                           help='Database port')

        parser.add_argument('--db-name',
                           default=config.get('database', 'name'),
                           help='Database name')

        # Logging options
        parser.add_argument('--log-level',
                           default=config.get('logging', 'level'),
                           choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                           help='Logging level')

        parser.add_argument('--log-file',
                           default=config.get('logging', 'file'),
                           help='Log file path')

        # Override options
        parser.add_argument('--verbose', '-v',
                           action='store_true',
                           help='Enable verbose output')

        # Parse with some overrides
        test_args = ['--db-port', '3306', '--log-level', 'DEBUG']
        args = parser.parse_args(test_args)

        print("Configuration (with command-line overrides):")
        print(f"  Database: {args.db_host}:{args.db_port}/{args.db_name}")
        print(f"  Logging: {args.log_level} -> {args.log_file}")
        print(f"  Verbose: {args.verbose}")

    finally:
        # Cleanup
        if os.path.exists(config_file):
            os.remove(config_file)

    print()


def main():
    """Run all argparse examples."""
    print("Python argparse Examples")
    print("=" * 40)
    print()

    basic_argument_parser()
    positional_arguments()
    file_arguments()
    mutually_exclusive_groups()
    subparsers_example()
    custom_actions()
    configuration_files()


if __name__ == "__main__":
    main()