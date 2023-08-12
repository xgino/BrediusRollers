import os
import shutil

def delete_folders(directory, folder_names):
    for root, _, _ in os.walk(directory):
        for folder_name in folder_names:
            folder_path = os.path.join(root, folder_name)
            if os.path.exists(folder_path) and os.path.isdir(folder_path):
                print(f"Deleting folder: {folder_path}")
                shutil.rmtree(folder_path)

if __name__ == "__main__":
    project_directory = os.path.dirname(os.path.abspath(__file__))
    folders_to_delete = ["__pycache__", "migrations"]

    delete_folders(project_directory, folders_to_delete)

    print("Folders deleted successfully.")