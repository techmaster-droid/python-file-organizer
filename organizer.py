import os
import shutil
import logging
import argparse


class InvalidPathError(Exception):
    """Custom exception for invalid directory paths."""
    pass


class FileOrganizer:
    FILE_TYPES = {
        "Images": [".jpg", ".jpeg", ".png", ".gif"],
        "Documents": [".pdf", ".docx", ".txt", ".pptx"],
        "Videos": [".mp4", ".mkv", ".avi"],
        "Music": [".mp3", ".wav"],
        "Zip": [".zip", ".rar"],
    }

    def __init__(self, base_path, overwrite=False, dry_run=False, log_level="INFO"):
        self.base_path = base_path
        self.overwrite = overwrite
        self.dry_run = dry_run
        self.setup_logging(log_level)
        self.validate_path()

    def setup_logging(self, log_level):
        level = getattr(logging, log_level.upper(), logging.INFO)
        logging.basicConfig(
            filename="organizer.log",
            level=level,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def validate_path(self):
        if not os.path.exists(self.base_path):
            raise InvalidPathError(f"Path does not exist: {self.base_path}")
        
        if not os.path.isdir(self.base_path):
            raise InvalidPathError(f"Not a directory: {self.base_path}")
        
    def create_folders(self):
        for folder in self.FILE_TYPES.keys():
            os.makedirs(os.path.join(self.base_path, folder), exist_ok=True)
        os.makedirs(os.path.join(self.base_path, "Others"), exist_ok=True)

    def move_file(self, source, destination, file_name):
        if self.dry_run:
            print(f"[DRY RUN] Would move: {file_name}")
            logging.info(f"[DRY RUN] Would move: {file_name}")
            return
        
        try:
            if not os.path.exists(destination) or self.overwrite:
                shutil.move(source, destination)
                logging.info(f"Moved: {file_name}")
                print(f"Moved: {file_name}")
            else:
                logging.warning(f"Skipped {file_name} (already exists)")
                print(f"Skipped: {file_name}")
        except Exception as e:
            logging.error(f"Error moving {file_name}: {e}")
            print(f"Error moving {file_name}")

    def organize_files(self):
        for file_name in os.listdir(self.base_path):
            file_path = os.path.join(self.base_path, file_name)

            if not os.path.isfile(file_path):
                continue

            _, extension = os.path.splitext(file_name.lower())
            moved = False

            for folder, extensions in self.FILE_TYPES.items():
                if extension in extensions:
                    destination = os.path.join(self.base_path, folder, file_name)
                    self.move_file(file_path, destination, file_name)
                    moved = True
                    break

            if not moved:
                destination = os.path.join(self.base_path, "Others", file_name)
                self.move_file(file_path, destination, file_name)

    def run(self):
        logging.info("Organizetion started")
        self.create_folders()
        self.organize_files()
        logging.info("Organization completed")
        print("Process finished.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advanced File Organizer")
    parser.add_argument("path", help="Path to organize")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing files")
    parser.add_argument("--dry-run", action="store_true", help="Simulate without moving files")
    parser.add_argument("--log-level", default="INFO", help="Logging level (INFO, WARNING, ERROR, DEBUG)")

    args = parser.parse_args()

    try:
        organizer = FileOrganizer(
            args.path,
            overwrite=args.overwrite,
            dry_run=args.dry_run,
            log_level=args.log_level
        )
        organizer.run()
    except InvalidPathError as e:
        logging.error(e)
        print(f"Invalid path error: {e}")
