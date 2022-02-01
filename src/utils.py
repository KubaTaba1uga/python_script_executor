from colorama import Fore, Style

import sys


def format_info(output: str) -> str:
    return Fore.GREEN + output + Style.RESET_ALL


def format_error(output: str) -> str:
    return Fore.RED + output + Style.RESET_ALL


def format_success(output: str) -> str:
    return Fore.BLUE + output + Style.RESET_ALL


def format_indent(output: str) -> str:
    return " " * 4 + output


def print_(output: str):
    sys.stdout.write(Style.RESET_ALL + output + Style.RESET_ALL)
    sys.stdout.flush()


def print_info(output: str):
    print_(format_info(output))


def print_error(output: str):
    print_(format_error(output))


def print_success(output: str):
    print_(format_success(output))
