from typing import Optional
from pathlib import Path

from colorama import Fore, Style

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
