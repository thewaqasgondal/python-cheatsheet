import os
import sys
import shutil

# 1. Get the current working directory
print(f"Current working directory: {os.getcwd()}")

# 2. List files and directories in the current directory
print("\nList of files and directories in the current directory:")
print(os.listdir())

# 3. Create a new directory
new_dir = "test_directory"
if not os.path.exists(new_dir):
    os.mkdir(new_dir)
    print(f"\nCreated a new directory: {new_dir}")
else:
    print(f"\nDirectory {new_dir} already exists.")

# 4. Create a new file inside the newly created directory
file_path = os.path.join(new_dir, "sample.txt")
with open(file_path, "w") as f:
    f.write("This is a sample file created using the os module.")
    print(f"\nCreated a new file: {file_path}")

# 5. Rename the file
new_file_path = os.path.join(new_dir, "renamed_sample.txt")
os.rename(file_path, new_file_path)
print(f"\nRenamed file from {file_path} to {new_file_path}")

# 6. Get system information
print("\nSystem Information:")
print(f"Platform: {sys.platform}")
print(f"Python version: {sys.version}")

# 7. Get environment variables
print("\nEnvironment Variables:")
for key, value in os.environ.items():
    print(f"{key}: {value}")

# 8. Delete the renamed file
os.remove(new_file_path)
print(f"\nDeleted the file: {new_file_path}")

# 9. Remove the directory
os.rmdir(new_dir)
print(f"\nRemoved the directory: {new_dir}")

# 10. Check if a directory exists
dir_exists = os.path.exists(new_dir)
print(f"\nDoes the directory exist? {dir_exists}")

# 11. Use shutil to copy a file (if any file exists in the directory)
source_file = "sample.txt"
destination = "copied_sample.txt"
if os.path.exists(source_file):
    shutil.copy(source_file, destination)
    print(f"\nCopied file {source_file} to {destination}")
else:
    print("\nNo file to copy.")

# 12. Demonstrating Path manipulation
file_path = os.path.join("folder", "subfolder", "file.txt")
print(f"\nExample file path: {file_path}")
print(f"Parent directory: {os.path.dirname(file_path)}")
print(f"File name: {os.path.basename(file_path)}")
