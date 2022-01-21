from pathlib import Path
import sys


class TempErrorFile:
    FILE_NAME = "errors_temp.log"
    ERROR_DIRECTORY = Path(sys.argv[0]).parent

    @classmethod
    def read_errors(cls):
        """Read errors from file and clean buffer"""
        with open(cls.FILE_NAME, "r+") as temp_errors:
            error_content = temp_errors.read()
            # Move pointer to file beginning
            temp_errors.seek(0)
            # Resize file to pointer position
            temp_errors.truncate()
        return error_content

    @classmethod
    def errors_exist(cls):
        if not Path(cls.FILE_NAME).exists():
            return False

        # If there is any content inside temp file return True
        with open(cls.FILE_NAME) as temp_errors:
            # Delete whitespaces which could be misleading
            #   for bool function
            return bool(temp_errors.read().strip())

    @classmethod
    def _create_error_log_path(cls) -> str:
        return cls.ERROR_DIRECTORY.joinpath(cls.FILE_NAME)

    @classmethod
    def create_error_redirection(cls):
        error_log_path = cls._create_error_log_path()
        return f" 2> {error_log_path}"
