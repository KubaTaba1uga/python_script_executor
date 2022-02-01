""" Utilities for printing messages  to user"""

from colorama import Fore, Style

import sys

INDENT = " " * 4


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
