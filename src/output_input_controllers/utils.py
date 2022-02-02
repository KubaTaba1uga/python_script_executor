from colorama import Fore, Style
from pathlib import Path
import functools
import sys
import os


INDENT = " " * 4
LOGS_DIR_NAME = "logs"
LOGS_DIR_PATH = Path(sys.argv[0]).parent.joinpath(LOGS_DIR_NAME)


def create_logs_dir():
    os.mkdir(LOGS_DIR_PATH)


def create_logs_directory(func):
    """Create logs directory before function execution"""

    if not LOGS_DIR_PATH.exists():
        create_logs_dir()

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

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


def format_error_output(output: str) -> str:

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


def format_info(output: str) -> str:
    """Format output on GREEN"""
    return Fore.GREEN + output + Style.RESET_ALL


def format_error(output: str) -> str:
    """Format output on RED"""
    return Fore.RED + output + Style.RESET_ALL


def format_success(output: str) -> str:
    """Format output on BLUE"""
    return Fore.BLUE + output + Style.RESET_ALL


def format_indent(output: str) -> str:
    """Add tab before output"""
    return INDENT + output


def print_(output: str):
    sys.stdout.write(Style.RESET_ALL + output + Style.RESET_ALL)
    sys.stdout.flush()


def print_info(output: str):
    """Print  informational notification on GREEN"""
    print_(format_info(output))


def print_error(output: str):
    """Print error notification on RED"""
    print_(format_error(output))


def print_success(output: str):
    """Print success notification on BLUE"""
    print_(format_success(output))
