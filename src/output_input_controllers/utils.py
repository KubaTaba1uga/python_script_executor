from pathlib import Path
import functools
import sys
import os


LOGS_DIR_NAME = "logs"
LOGS_DIR_PATH = Path(sys.argv[0]).parent.joinpath(LOGS_DIR_NAME)


def create_logs_dir():
    os.mkdir(LOGS_DIR_PATH)


def create_logs_directory(func):
    """Create logs directory before function execution"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    if not LOGS_DIR_PATH.exists():
        create_logs_dir()

    return wrapper


def create_log_name(script_name: str) -> str:
    EXTENSION = "log"

    extension_index = len(script_name) - script_name[::-1].find(".")

    if extension_index > 0:
        return script_name[:extension_index] + EXTENSION

    return script_name + EXTENSION


def get_log_file_path(script_name: str) -> Path:
    log_name = create_log_name(script_name)
    return LOGS_DIR_PATH.joinpath(log_name)


def format_error(output: str) -> str:

    double_newline = "\n" * 2

    tab = " " * 4

    return (
        double_newline
        + "ERROR!!!"
        + double_newline
        + tab
        + f"{output}"
        + "\n"
        + "ERROR!!!"
        + "\n"
    )
