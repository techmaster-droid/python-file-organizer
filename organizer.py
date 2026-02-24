import os
import shutil
import logging
import argparse

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
            os.makedirs(os.path.join(self.base_path, folder), exist_ok=True)
        os.makedirs(os.path.join(self.base_path, "Others"), exist_ok=True)

    def organize_files(self):
        for file_name in os.listdir(self.base_path):
            file_path = os.path.join(self.base_path, file_name)

            if not os.path.isfile(file_path):
                continue

            logging.info(f"Processing file: {file_name}")

            moved = False
            _, extension = os.path.splitext(file_name.lower())

            for folder, extensions in self.FILE_TYPES.items():
                if extension in extensions:
                    destination = os.path.join(self.base_path, folder, file_name)

                    try:
                        if not os.path.exists(destination):
                            shutil.move(file_path, destination)
                            logging.info(f"Moved: {file_name} -> {folder}")
                            print(f"Moved: {file_name} -> {folder}")
                        else:
                            logging.warning(f"Skipped {file_name} (already exists)")
                    except Exception as e:
                        logging.error(f"Error moving {file_name}: {e}")
                        print(f"Error moving {file_name}")

                    moved = True
                    break
            if not moved:
                destination = os.path.join(self.base_path, "Others", file_name)
                try:
                    shutil.move(file_path, destination)
                    logging.info(f"Moved: {file_name} -> Others")
                    print(f"Moved: {file_name} -> Others")
                except Exception as e:
                    logging.error(f"Error moving {file_name}: {e}")
                    print(f"Error moving {file_name}")

    def run(self):
        logging.info("File organization started.")
        self.create_folders()
        self.organize_files()
        logging.info("File organization completed.")
        print("Process completed successfully!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Organize files by type.")
    parser.add_argument("path", help="Path of the folder to organize")

    args = parser.parse_args()

    organizer = FileOrganizer(args.path)
    organizer.run()