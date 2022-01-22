from pathlib import Path
import sys


class TempErrorFile:
    FILE_NAME = "errors_temp.log"

    def __init__(self, directory: Path = Path(sys.argv[0]).parent):
        self.directory = directory
        self.path = directory.joinpath(self.FILE_NAME)

    def read(self):
        """Read errors from file and clean buffer"""
        with open(self.path, "r+") as temp_errors:
            error_content = temp_errors.read()
            # Move pointer to file beginning
            temp_errors.seek(0)
            # Resize file to pointer position
            temp_errors.truncate()
        return error_content

    def exist(self):
        if not self.path.exists():
            return False

        # If there is any content inside temp file return True
        with open(self.path) as temp_errors:
            # Delete whitespaces which could be misleading
            #   for bool function
            return bool(temp_errors.read().strip())

    def create_error_redirection(self):
        return f" 2> {self.path}"
