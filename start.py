#!/bin/env python
"""

Usage:
        start.py
        start.py (-o | --output_input_controller) <controller_name>
        start.py (-d | --scripts_directory) <scripts_path>
        start.py (-s | --shell) <shell_name>
        start.py [options]  [<controller_name>]  [<scripts_path>]  [<shell_name>]

Options:
        -o  <controller_name>, --output_input_controller  <controller_name>     Name of the controller which handle output and input.

        -d  <scripts_path>, --scripts_directory  <scripts_path>    Path to directory with scripts which will be executed.

        -s  <shell_name>, --shell  <shell_name>    Name of the shell in which scripts will be executed.

Variants:

        Controller names:
                1. terminaloutputinput

        Shell names:
                1. bash
"""
from pathlib import Path
import sys

from docopt import docopt
from colorama import Fore, Style

from src.output_input_controller import OutputInputController, TerminalOutputInput
from src.shell import SubShell


def notify(output: str):
    print("\n", output, end="\n" * 2)


def notify_mistake(first: str, middle: str, last: str):
    notify(
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


if __name__ == "__main__":
    default_output_input_controller = TerminalOutputInput()
    # By default scripts are held in ./scripts directory
    default_scripts_directory = Path(sys.argv[0]).parent.joinpath("scripts")
    # By default errors buffer is in ./scripts directory
    default_error_buffer_directory = Path(sys.argv[0]).parent.joinpath("scripts")

    output_input_controller = None
    scripts_directory = None
    error_buffer_directory = None

    args = docopt(__doc__)

    if args["-o"]:
        for subclass in OutputInputController.__subclasses__():
            if args["<controller_name>"] == subclass.command_line_argument:
                output_input_controller = subclass()

        if not output_input_controller:
            notify_mistake(
                "Output input controller named ",
                f'"{args["<controller_name>"]}"',
                " was not found!!!",
            )

            exit(127)
    else:
        output_input_controller = default_output_input_controller

    if args["-d"]:
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
        scripts_directory = path
    else:
        scripts_directory = default_scripts_directory

    from pprint import pprint

    pprint(args)
