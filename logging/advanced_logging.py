"""
Advanced Python Logging Examples

This module demonstrates comprehensive logging techniques including
formatters, handlers, filters, configuration, and best practices.
"""

import logging
import logging.config
import json
import sys
import os
from typing import Dict, Any, Optional
from pathlib import Path
import tempfile
import yaml


class CustomFormatter(logging.Formatter):
    """Custom formatter with colored output and structured formatting."""

    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
        'RESET': '\033[0m'      # Reset
    }

    def format(self, record: logging.LogRecord) -> str:
        # Add color if outputting to terminal
        if hasattr(record, 'color') and record.color and sys.stdout.isatty():
            color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
            reset = self.COLORS['RESET']

            # Format the message with color
            formatted = super().format(record)
            return f"{color}{formatted}{reset}"

        return super().format(record)


class StructuredFormatter(logging.Formatter):
    """JSON formatter for structured logging."""

    def format(self, record: logging.LogRecord) -> str:
        # Create structured log entry
        log_entry = {
            'timestamp': self.formatTime(record),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }

        # Add any extra fields from the record
        if hasattr(record, 'extra_data'):
            log_entry['extra_data'] = record.extra_data

        # Add exception info if present
        if record.exc_info:
            log_entry['exception'] = self.formatException(record.exc_info)

        return json.dumps(log_entry)


class LevelFilter(logging.Filter):
    """Filter that only allows specific log levels."""

    def __init__(self, allowed_levels: list):
        super().__init__()
        self.allowed_levels = allowed_levels

    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelno in self.allowed_levels


class ContextFilter(logging.Filter):
    """Filter that adds context information to log records."""

    def __init__(self, context: Dict[str, Any]):
        super().__init__()
        self.context = context

    def filter(self, record: logging.LogRecord) -> bool:
        # Add context information to the record
        for key, value in self.context.items():
            if not hasattr(record, key):
                setattr(record, key, value)
        return True


def setup_basic_logging():
    """Demonstrate basic logging setup."""
    print("=== Basic Logging Setup ===")

    # Basic configuration
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    logger = logging.getLogger('basic_example')

    logger.debug("This is a debug message (won't show)")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")

    print()


def setup_colored_logging():
    """Demonstrate colored logging output."""
    print("=== Colored Logging ===")

    # Create logger
    logger = logging.getLogger('colored_example')
    logger.setLevel(logging.DEBUG)

    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Create console handler with custom formatter
    handler = logging.StreamHandler()
    formatter = CustomFormatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Add color attribute to records
    old_factory = logging.getLogRecordFactory()

    def record_factory(*args, **kwargs):
        record = old_factory(*args, **kwargs)
        record.color = True
        return record

    logging.setLogRecordFactory(record_factory)

    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")

    # Reset factory
    logging.setLogRecordFactory(old_factory)
    print()


def setup_structured_logging():
    """Demonstrate structured JSON logging."""
    print("=== Structured JSON Logging ===")

    logger = logging.getLogger('structured_example')
    logger.setLevel(logging.INFO)

    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Create handler with JSON formatter
    handler = logging.StreamHandler()
    formatter = StructuredFormatter()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Log with extra data
    logger.info("User login attempt", extra={'extra_data': {'user_id': 123, 'ip': '192.168.1.1'}})
    logger.warning("High memory usage detected", extra={'extra_data': {'memory_percent': 85}})
    logger.error("Database connection failed", extra={'extra_data': {'db_host': 'localhost', 'error_code': 1045}})

    print()


def setup_multiple_handlers():
    """Demonstrate logging to multiple destinations."""
    print("=== Multiple Handlers ===")

    logger = logging.getLogger('multi_handler_example')
    logger.setLevel(logging.DEBUG)

    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Create formatters
    simple_formatter = logging.Formatter('%(levelname)s: %(message)s')
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
    )

    # Console handler (INFO and above)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(simple_formatter)
    logger.addHandler(console_handler)

    # File handler (DEBUG and above)
    with tempfile.NamedTemporaryFile(mode='w', suffix='.log', delete=False) as f:
        log_file = f.name

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)
    logger.addHandler(file_handler)

    # Log messages
    logger.debug("This debug message goes to file only")
    logger.info("This info message goes to both console and file")
    logger.warning("This warning message goes to both console and file")

    # Read and display file contents
    with open(log_file, 'r') as f:
        file_contents = f.read()

    print("File contents:")
    print(file_contents)

    # Cleanup
    os.unlink(log_file)
    print()


def setup_filtered_logging():
    """Demonstrate logging with filters."""
    print("=== Filtered Logging ===")

    logger = logging.getLogger('filtered_example')
    logger.setLevel(logging.DEBUG)

    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Create handler
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))

    # Add level filter (only WARNING and above)
    level_filter = LevelFilter([logging.WARNING, logging.ERROR, logging.CRITICAL])
    handler.addFilter(level_filter)

    # Add context filter
    context_filter = ContextFilter({'service': 'web_app', 'version': '1.2.3'})
    handler.addFilter(context_filter)

    logger.addHandler(handler)

    logger.debug("This won't show (filtered out by level)")
    logger.info("This won't show (filtered out by level)")
    logger.warning("This warning will show with context")
    logger.error("This error will show with context")

    print()


def setup_rotating_logs():
    """Demonstrate log rotation."""
    print("=== Log Rotation ===")

    from logging.handlers import RotatingFileHandler

    logger = logging.getLogger('rotating_example')
    logger.setLevel(logging.INFO)

    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Create rotating file handler
    with tempfile.TemporaryDirectory() as temp_dir:
        log_file = os.path.join(temp_dir, 'app.log')

        # Rotate when file reaches 1KB, keep 3 backup files
        handler = RotatingFileHandler(
            log_file,
            maxBytes=1024,  # 1KB
            backupCount=3
        )
        handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        ))
        logger.addHandler(handler)

        # Generate enough logs to trigger rotation
        for i in range(20):
            logger.info(f"Log message {i+1}: {'x' * 50}")  # Each ~70 bytes

        # Check how many files were created
        log_files = [f for f in os.listdir(temp_dir) if f.startswith('app.log')]
        print(f"Created {len(log_files)} log files: {sorted(log_files)}")

    print()


def dict_config_example():
    """Demonstrate dictionary-based logging configuration."""
    print("=== Dictionary Configuration ===")

    # Logging configuration as dictionary
    config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            },
            'detailed': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'INFO',
                'formatter': 'standard',
                'stream': 'ext://sys.stdout'
            },
            'file': {
                'class': 'logging.FileHandler',
                'level': 'DEBUG',
                'formatter': 'detailed',
                'filename': 'dict_config.log',
                'mode': 'w'
            }
        },
        'loggers': {
            'dict_config_app': {
                'level': 'DEBUG',
                'handlers': ['console', 'file'],
                'propagate': False
            }
        }
    }

    # Apply configuration
    logging.config.dictConfig(config)

    logger = logging.getLogger('dict_config_app')

    logger.debug("Debug message (file only)")
    logger.info("Info message (console and file)")
    logger.warning("Warning message (console and file)")

    # Cleanup
    if os.path.exists('dict_config.log'):
        with open('dict_config.log', 'r') as f:
            print("File contents:")
            print(f.read()[:200] + "..." if len(f.read()) > 200 else f.read())
        os.unlink('dict_config.log')

    print()


def performance_logging():
    """Demonstrate performance considerations in logging."""
    print("=== Performance Logging ===")

    import time

    logger = logging.getLogger('performance_example')
    logger.setLevel(logging.INFO)

    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Add handler
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(handler)

    # Test logging performance
    start_time = time.time()

    # Log many messages
    for i in range(1000):
        logger.info(f"Message {i}")

    end_time = time.time()
    print(".4f")

    # Demonstrate lazy formatting
    expensive_data = list(range(1000))  # Expensive to create

    # Bad: Always evaluate even if not logged
    # logger.debug(f"Expensive data: {expensive_data}")

    # Good: Only evaluate when needed
    logger.debug("Expensive data: %s", expensive_data)

    print("Lazy formatting prevents unnecessary computation when debug is disabled")
    print()


def security_logging():
    """Demonstrate security considerations in logging."""
    print("=== Security Logging ===")

    logger = logging.getLogger('security_example')
    logger.setLevel(logging.INFO)

    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Add handler
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)

    # Safe logging - avoid logging sensitive data
    user_credentials = {
        'username': 'admin',
        'password': 'secret123',  # Never log this!
        'session_id': 'abc123'
    }

    # Bad: Logging sensitive data
    # logger.info(f"User login: {user_credentials}")

    # Good: Log only non-sensitive information
    logger.info(f"User login successful for username: {user_credentials['username']}")
    logger.info(f"Session created: {user_credentials['session_id']}")

    # For debugging, mask sensitive data
    safe_creds = user_credentials.copy()
    safe_creds['password'] = '***masked***'
    logger.debug(f"Debug credentials: {safe_creds}")

    print("Remember: Never log passwords, API keys, or other sensitive data!")
    print()


def main():
    """Run all logging examples."""
    print("Advanced Python Logging Examples")
    print("=" * 40)
    print()

    setup_basic_logging()
    setup_colored_logging()
    setup_structured_logging()
    setup_multiple_handlers()
    setup_filtered_logging()
    setup_rotating_logs()
    dict_config_example()
    performance_logging()
    security_logging()


if __name__ == "__main__":
    main()