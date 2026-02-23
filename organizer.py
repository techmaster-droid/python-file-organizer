import os
import shutil
import logging

class FileOrganizer:
    FILE_TYPES = {
        "Images": [".jpg", ".jpeg", ".png", ".gif"],
        "Documents": [".pdf", ".docx", ".txt", ".pptx"],
        "Videos": [".mp4", ".mkv", ".avi"],
        "Music": [".mp3", ".wav"],
        "Zip": [".zip", ".rar"],
    }

    def __init__(self, base_path):
        self.base_path = base_path
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(
            filename="organizer.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def create_folders(self):
        for folder in self.FILE_TYPES.keys():
            folder_path = os.path.join(self.base_path, folder)
            os.makedirs(folder_path, exist_ok=True)
        os.makedirs(os.path.join(self.base_path, "Others"), exist_ok=True)

    def organize_files(self):
        for file_name in os.listdir(self.base_path):
            file_path = os.path.join(self.base_path, file_name)

            if not os.path.isfile(file_path):
                continue

            move = False
            _, extension = os.path.splitext(file_name.lower())

            for folder, extensions in self.FILE_TYPES.items():
                if extension in extensions:
                    destination = os.path.join(self.base_path, folder, file_name)

                    if not os.path.exists(destination):
                        shutil.move(file_path, destination)
                        print(f"Moved: {file_name} -> {folder}")

                    moved = True
                    break

            if not moved:
                destination = os.path.join(self.base_path, "Others", file_name)
                if not os.path.exists(destination):
                    shutil.move(file_path, destination)
                    print(f"Moved: {file_name} -> Others")
                    logging.info(f"Moved: {file_name} -> Others")

    def run(self):
        self.create_folders()
        self.organize_files()
        print("Files organized successfully!")
        logging.info("File organization completed.")

if __name__ == "__main__":
    path = input("Enter folder path: ")
    organizer = FileOrganizer(path)
    organizer.run()