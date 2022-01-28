from colorama import Fore, Style

import sys


def print_info(output: str):
    print(Fore.GREEN + output + Style.RESET_ALL, end="")


def print_error(output: str):
    print(Fore.RED + output + Style.RESET_ALL, end="")


def print_success(output: str):
    print(Fore.BLUE + output + Style.RESET_ALL, end="")


def print_(output: str):
    sys.stdout.write(Style.RESET_ALL + output + Style.RESET_ALL)
    sys.stdout.flush()
