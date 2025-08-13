import os
import shutil
import json
import csv
from datetime import datetime

# Utility to print file metadata
def get_file_metadata(file_path):
    try:
        # File size in bytes
        file_size = os.path.getsize(file_path)
        
        # Last modified and creation time
        mod_time = os.path.getmtime(file_path)
        create_time = os.path.getctime(file_path)
        
        # Convert to readable format
        mod_time = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M:%S')
        create_time = datetime.fromtimestamp(create_time).strftime('%Y-%m-%d %H:%M:%S')

        print(f"File: {file_path}")
        print(f"Size: {file_size} bytes")
        print(f"Created: {create_time}")
        print(f"Last Modified: {mod_time}")
    except FileNotFoundError:
        print(f"File {file_path} not found.")

# Utility to read a file (text, csv, or json)
def read_file(file_path):
    try:
        if file_path.endswith('.txt'):
            with open(file_path, 'r') as file:
                print(f"Contents of {file_path}:")
                print(file.read())
        elif file_path.endswith('.csv'):
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                print(f"Contents of {file_path}:")
                for row in reader:
                    print(row)
        elif file_path.endswith('.json'):
            with open(file_path, 'r') as file:
                data = json.load(file)
                print(f"Contents of {file_path}:")
                print(json.dumps(data, indent=4))
        else:
            print(f"Unsupported file format: {file_path}")
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

# List files in a directory
def list_files(directory):
    print(f"\nListing files in directory: {directory}")
    try:
        for file_name in os.listdir(directory):
            file_path = os.path.join(directory, file_name)
            if os.path.isfile(file_path):
                get_file_metadata(file_path)
    except FileNotFoundError:
        print(f"Directory {directory} not found.")

# File operation functions
def copy_file(src, dest):
    try:
        shutil.copy(src, dest)
        print(f"Copied {src} to {dest}")
    except FileNotFoundError:
        print(f"File {src} not found.")
    except Exception as e:
        print(f"Error copying file: {e}")

def rename_file(src, dest):
    try:
        os.rename(src, dest)
        print(f"Renamed {src} to {dest}")
    except FileNotFoundError:
        print(f"File {src} not found.")
    except Exception as e:
        print(f"Error renaming file: {e}")

def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"Deleted {file_path}")
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except Exception as e:
        print(f"Error deleting file: {e}")

# Read large files in chunks
def read_large_file(file_path, chunk_size=1024):
    try:
        with open(file_path, 'r') as file:
            print(f"Reading {file_path} in chunks:")
            while chunk := file.read(chunk_size):
                print(chunk)
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except Exception as e:
        print(f"Error reading large file {file_path}: {e}")

# Main function
def main():
    # File operations
    directory = "example_directory"  # Change to your test directory
    list_files(directory)
    
    # Read a text file
    text_file = "example_directory/example.txt"  # Change to your test text file
    read_file(text_file)
    
    # Read a CSV file
    csv_file = "example_directory/data.csv"  # Change to your test CSV file
    read_file(csv_file)
    
    # Read a JSON file
    json_file = "example_directory/data.json"  # Change to your test JSON file
    read_file(json_file)
    
    # File operations: Copy, Rename, Delete
    source_file = "example_directory/source.txt"  # Change to your source file
    destination_file = "example_directory/copied.txt"  # Change to your destination file
    copy_file(source_file, destination_file)

    renamed_file = "example_directory/renamed.txt"  # Change to your renamed file
    rename_file(source_file, renamed_file)

    delete_file(renamed_file)
    
    # Large file reading (example with chunking)
    large_file = "example_directory/large_file.txt"  # Change to a large file you want to test
    read_large_file(large_file)

if __name__ == "__main__":
    main()
