"""
Basic tests for Python Cheatsheet examples.

This module contains simple tests to verify that the example code works correctly.
Run with: python tests/test_basic.py
"""

import os
import sys


def test_basic_imports():
    """Test that basic imports work."""
    try:
        import threading
        import time
        import json
        import csv
        print("✓ Basic imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False


def test_threading_example():
    """Test that threading example can be imported and basic functions exist."""
    # Add the concurrency directory to path
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'concurrency'))

    try:
        import threading_intro
        assert hasattr(threading_intro, 'print_numbers')
        assert hasattr(threading_intro, 'print_letters')
        assert hasattr(threading_intro, 'demonstrate_threading')
        print("✓ Threading example structure OK")
        return True
    except Exception as e:
        print(f"✗ Threading example test failed: {e}")
        return False


def test_data_structures_example():
    """Test that data structures example can be imported."""
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'basic_concepts'))

    try:
        import data_structures
        assert hasattr(data_structures, 'list_examples')
        assert hasattr(data_structures, 'tuple_examples')
        assert hasattr(data_structures, 'dict_examples')
        assert hasattr(data_structures, 'set_examples')
        print("✓ Data structures example structure OK")
        return True
    except Exception as e:
        print(f"✗ Data structures example test failed: {e}")
        return False


def test_file_operations():
    """Test basic file operations functionality."""
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'file_operations'))

    try:
        import file_analysis
        assert hasattr(file_analysis, 'get_file_metadata')
        assert hasattr(file_analysis, 'read_file')
        print("✓ File operations example structure OK")
        return True
    except Exception as e:
        print(f"✗ File operations example test failed: {e}")
        return False


def test_example_files_exist():
    """Test that example files exist."""
    example_files = [
        'basic_concepts/data_structures.py',
        'basic_concepts/decorators.py',
        'basic_concepts/generators.py',
        'concurrency/threading_intro.py',
        'concurrency/multiprocessing_intro.py',
        'file_operations/file_analysis.py',
        'ocr_examples/ocr_example.py',
        'nlp_examples/my_nltk/tokenization.py',
        'tensorflow_examples/tf.py'
    ]

    all_exist = True
    for file_path in example_files:
        full_path = os.path.join(os.path.dirname(__file__), '..', file_path)
        if os.path.exists(full_path):
            print(f"✓ {file_path} exists")
        else:
            print(f"✗ {file_path} missing")
            all_exist = False

    return all_exist


def test_requirements_file():
    """Test that requirements.txt exists and is readable."""
    req_path = os.path.join(os.path.dirname(__file__), '..', 'requirements.txt')
    if not os.path.exists(req_path):
        print("✗ requirements.txt not found")
        return False

    try:
        with open(req_path, 'r') as f:
            content = f.read()
            if len(content.strip()) == 0:
                print("✗ requirements.txt is empty")
                return False
            if 'pytesseract' not in content:
                print("✗ pytesseract not in requirements")
                return False
            print("✓ requirements.txt OK")
            return True
    except Exception as e:
        print(f"✗ Error reading requirements.txt: {e}")
        return False


def main():
    """Run all tests and report results."""
    print("Running basic validation tests...\n")

    tests = [
        test_basic_imports,
        test_threading_example,
        test_data_structures_example,
        test_file_operations,
        test_example_files_exist,
        test_requirements_file,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1
        print()

    print(f"Results: {passed}/{total} tests passed")

    if passed == total:
        print("✓ All basic tests passed!")
        return 0
    else:
        print("✗ Some tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())