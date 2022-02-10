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


def create_log_name(script_name: str) -> str:
    EXTENSION = "log"

    extension_index = len(script_name) - script_name[::-1].find(".")

    if extension_index > 0:
        return script_name[:extension_index] + EXTENSION

    return script_name + EXTENSION


def get_log_file_path(script_name: str) -> Path:
    log_name = create_log_name(script_name)
    return LOGS_DIR_PATH.joinpath(log_name)


def write_to_log(script_name: str, output: str):
    if not LOGS_DIR_PATH.exists():
        create_logs_dir()

    with open(get_log_file_path(script_name), "a") as f:
        f.write(output)


def format_error_output(output: str) -> str:

    double_newline = "\n" * 2

    return (
        double_newline
        + "ERROR!!!"
        + double_newline
        + f"{output}"
        + double_newline
        + "ERROR!!!"
        + double_newline
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


def ask_to_exit() -> bool:
    """If user would like to exit return True
    if not return False"""

    question = "Would You like to stop scripts execution? (y/[n])"

    choices = {"yes": "y", "no": "n", "default": ""}

    while True:
        anwser = input(question)
        if anwser in choices.values():
            return anwser == choices["yes"]
        else:
            print_("Wrong input value!!! Type 'y' or 'n'")
