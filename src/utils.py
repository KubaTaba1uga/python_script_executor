from colorama import Fore, Style


def print_info(output: str):
    print(Fore.GREEN + output + Style.RESET_ALL, end="")


def print_error(output: str):
    print(Fore.RED + output + Style.RESET_ALL, end="")


def print_success(output: str):
    print(Fore.BLUE + output + Style.RESET_ALL, end="")


def print_(output: str):
    print(Style.RESET_ALL + output + Style.RESET_ALL, end="")
