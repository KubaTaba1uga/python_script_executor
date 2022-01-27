#!/bin/env python
"""

Usage:
        start.py
        start.py (-o | --output_input_controller) <controller_name>
        start.py (-d | --scripts_directory) <scripts_path>
        start.py (-s | --shell) <shell_name>
        start.py (-e | --errors_directory) <errors_path>
        start.py [(-o <controller_name> | --output_input_controller <controller_name>)]  [(-d <scripts_path>| --scripts_directory  <scripts_path>)]  [(-s <shell_name> | --shell <shell_name>)] [(-e <errors_path> |  --errors_directory  <errors_path>)]

Options:
        -o  <controller_name>, --output_input_controller  <controller_name>     Name of the controller which handle output and input.
        -d  <scripts_path>, --scripts_directory  <scripts_path>    Path to directory with scripts which will be executed.
        -s  <shell_name>, --shell  <shell_name>    Name of the shell in which scripts will be executed.
        -e  <errors_path>, --errors_directory <errors_path>     Directory where errors buffer will be used.

Variants:

        Controller names:
                1. terminal - print output and errors, if input is required asks for:
                         input
                         process termination
                         sleep for 30s

        Shell names:
                1. bash
"""
from pathlib import Path
import sys

from docopt import docopt
from colorama import Fore, Style

from src.app import main
from src.shell import SubShell
from src.exceptions import FileNotExecutable, FileNotFound
from src.temporary_errors_buffer import TempErrorFile
from src.output_input_controller import OutputInputController, TerminalOutputInput


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
    default_error_buffer_directory = Path("/tmp")

    output_input_controller = None
    scripts_directory = None
    errors_directory = None
    shell = None

    args = docopt(__doc__)

    print(args)

    if args["-o"] or args["--output_input_controller"]:
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
        scripts_directory = path
    else:
        scripts_directory = default_scripts_directory

    if args["-s"] or args["--shell"]:
        for shell_ in SubShell.__subclasses__():
            if args["<shell_name>"] == shell_.command_line_argument:
                try:
                    shell = shell_()
                except FileNotFound:
                    notify_mistake(
                        "Scripts shell ", f'"{shell_.path}"', " was not found!!!"
                    )
                    exit(127)
                except FileNotExecutable:
                    notify_mistake(
                        "Scripts shell ",
                        f'"{shell_.path}"',
                        " is not executable!!!",
                    )
                    exit(127)
        if not shell:
            notify_mistake(
                "Scripts shell ", f'"{args["<shell_name>"]}"', " was not found!!!"
            )
            exit(127)

    else:
        for shell_ in SubShell.__subclasses__():
            try:
                shell = shell_()
                break
            except FileNotFound:
                pass
            except FileNotExecutable:
                pass
        if not shell:
            notify_mistake(
                "There is no ", "scripts shell", " available in Your system!!!"
            )
            exit(127)

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
        errors_directory = path
    else:
        errors_directory = default_error_buffer_directory

    main(
        shell=shell,
        script_folder_path=scripts_directory,
        oi_controller=output_input_controller,
        errors_buffer_path=errors_directory,
    )
