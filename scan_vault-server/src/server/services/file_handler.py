import os
from pathlib import Path

class FileHandler:
    @staticmethod
    def save_file(file, directory: str) -> str:
        """Save uploaded file to the specified directory."""
        Path(directory).mkdir(parents=True, exist_ok=True)
        file_path = os.path.join(directory, file.filename)
        with open(file_path, "wb") as f:
            f.write(file.file.read())
        return file_path

    @staticmethod
    def delete_file(file_path: str) -> None:
        """Delete the file from disk."""
        if os.path.exists(file_path):
            os.remove(file_path)
