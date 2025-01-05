import os
import shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

# Define the directories to organize
DIRECTORIES_TO_ORGANIZE = [
    os.path.join(Path.home(), "Desktop"),
    os.path.join(Path.home(), "Downloads"),
    os.path.join(Path.home(), "Documents")
]

# Define the file categories and their corresponding extensions
FILE_CATEGORIES = {
    "Documents": [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg"],
    "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv"],
    "Music": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Executables": [".exe", ".msi", ".bat", ".sh"],
    "Code": [".py", ".java", ".c", ".cpp", ".js", ".html", ".css", ".sql"],
    "Others": []
}

# Function to handle a single file
def handle_file(file_path, base_folder):
    # Identify the file extension
    file_name = os.path.basename(file_path)
    _, file_extension = os.path.splitext(file_name)

    # Find the category for the file
    category = "Others"
    for cat, extensions in FILE_CATEGORIES.items():
        if file_extension.lower() in extensions:
            category = cat
            break

    # Create the target folder if it doesn't exist
    target_folder = os.path.join(base_folder, category)
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # Move the file to the target folder
    try:
        shutil.move(file_path, target_folder)
        print(f"Moved: {file_name} -> {target_folder}")
    except Exception as e:
        print(f"Error moving {file_name}: {e}")

# Function to remove empty folders
def remove_empty_folders(directory):
    for root, dirs, files in os.walk(directory, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            try:
                if not os.listdir(dir_path):
                    os.rmdir(dir_path)
                    print(f"Removed empty folder: {dir_path}")
            except PermissionError:
                print(f"Permission denied: {dir_path}")
            except Exception as e:
                print(f"Error removing folder {dir_path}: {e}")

# Main function to organize files
def organize_files():
    # Define the base organization folder on the desktop
    base_folder = os.path.join(Path.home(), "Desktop", "Organized")
    if not os.path.exists(base_folder):
        os.makedirs(base_folder)

    with ThreadPoolExecutor() as executor:
        for directory in DIRECTORIES_TO_ORGANIZE:
            if not os.path.exists(directory):
                print(f"Directory {directory} does not exist. Skipping.")
                continue

            for file_name in os.listdir(directory):
                file_path = os.path.join(directory, file_name)

                # Skip directories
                if os.path.isdir(file_path):
                    continue

                # Skip system-related directories or files
                if file_path.startswith(os.path.join(Path.home(), "AppData")) or \
                   file_path.startswith(os.path.join("C:\\Windows")):
                    print(f"Skipping system file or folder: {file_path}")
                    continue

                # Process files using multithreading
                executor.submit(handle_file, file_path, base_folder)

    # Remove empty folders in the specified directories
    for directory in DIRECTORIES_TO_ORGANIZE:
        remove_empty_folders(directory)

if __name__ == "__main__":
    organize_files()
