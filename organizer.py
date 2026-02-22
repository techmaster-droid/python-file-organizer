import os 
import shutil

#Path to the folder you want to organize
SOURCE_FOLDER = input("Enter folder path: ")
print("File Organize Tool Started")

#File type mapping
FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".docx", ".txt", ".pptx"],
    "Videos": [".mp4", ".mkv", ".avi"],
    "Music": [".mp3", ".wav"],
    "Zip": [".zip", ".rar"],
}

def create_folders(base_path):
    for folder in FILE_TYPES.keys():
        folder_path = os.path.join(base_path, folder)
        os.makedirs(folder_path, exist_ok=True)
    os.makedirs(os.path.join(base_path, "Others"), exist_ok=True)

def organize_files(base_path):
    for file_name in os.listdir(base_path):
        file_path = os.path.join(base_path, file_name)

        # Skip folders
        if not os.path.isfile(file_path):
            continue
        moved = False

        for folder, extensions in FILE_TYPES.items():
            if file_name.lower().endswith(tuple(extensions)):
                destination = os.path.join(base_path, folder, file_name)

                if not os.path.exists(destination):
                    shutil.move(file_path, destination)
                    print(f"Moved: {file_name} -> {folder}")
                    moved = True
                    break

        if not moved:
            destination = os.path.join(base_path, "Others", file_name)
            if not os.path.exists(destination):
                shutil.move(file_path, destination)
                print(f"Moved: {file_name} -> Others")

def main():
    create_folders(SOURCE_FOLDER)
    organize_files(SOURCE_FOLDER)
    print("Files organized successfully!")

if __name__ == "__main__":
    main()
