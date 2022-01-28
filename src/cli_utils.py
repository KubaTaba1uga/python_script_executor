from typing import Optional
from pathlib import Path

from colorama import Fore, Style

from src.shell import SubShell
from src.exceptions import FileNotExecutable, FileNotFound
from src.output_input_controller import OutputInputController, TerminalOutputInput


def _notify(output: str):
    print("\n", output, end="\n" * 2)


def notify_mistake(first: str, middle: str, last: str):
    _notify(
        Style.DIM
        + Fore.RED
        + first
        + Style.RESET_ALL
        + Fore.RED
        + Style.BRIGHT
        + middle
        + Style.DIM
        + last
        + Style.RESET_ALL
    )


def parse_cli_output_input_controller(args: dict) -> Optional[OutputInputController]:
    if args["-o"] or args["--output_input_controller"]:
        for subclass in OutputInputController.__subclasses__():
            if args["<controller_name>"] == subclass.command_line_argument:
                return subclass()

        notify_mistake(
            "Output input controller named ",
            f'"{args["<controller_name>"]}"',
            " was not found!!!",
        )

        exit(127)

    return None


def parse_cli_scripts_directory(args: dict) -> Optional[Path]:
    if args["-d"] or args["--scripts_directory"]:
        path = Path(args["<scripts_path>"])
        if not path.exists():
            notify_mistake(
                "Script directory ",
                f'"{path}"',
                " is not present inside file system!!!",
            )
            exit(127)
        elif not path.is_dir():
            notify_mistake("Script directory ", f'"{path}"', " is not a directory!!!")
            exit(127)
        return path

    return None


def parse_cli_shell(args: dict) -> SubShell:
    if args["-s"] or args["--shell"]:
        for shell in SubShell.__subclasses__():
            if args["<shell_name>"] == shell.command_line_argument:
                try:
                    shell()
                    return shell
                except FileNotFound:
                    pass
                except FileNotExecutable:
                    notify_mistake(
                        "Scripts shell ",
                        f'"{shell.path}"',
                        " is not executable!!!",
                    )
                    exit(127)

        notify_mistake(
            "Scripts shell ", f'"{args["<shell_name>"]}"', " was not found!!!"
        )
        exit(127)

    else:
        for shell in SubShell.__subclasses__():
            try:
                shell()
                return shell
                break
            except FileNotFound:
                pass
            except FileNotExecutable:
                pass

        notify_mistake("There is no ", "scripts shell", " available in Your system!!!")
        exit(127)


def parse_cli_errors_directory(args: dict) -> Optional[Path]:
    if args["-e"] or args["--errors_directory"]:
        path = Path(args["<errors_path>"])
        if not path.exists():
            notify_mistake(
                "Errors directory ",
                f'"{path}"',
                " is not present inside file system!!!",
            )
            exit(127)
        elif not path.is_dir():
            notify_mistake("Errors directory ", f'"{path}"', " is not a directory!!!")
            exit(127)
        return path
    return None