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

        -d  <scripts_path>, --scripts_directory  <scripts_path>                 Path to directory with scripts which will be executed. 
                                                                                Directory should have only scripts files inside, 
                                                                                without directories or non executable files.

        -s  <shell_name>, --shell  <shell_name>                                 Name of the shell in which scripts will be executed.

        -e  <errors_path>, --errors_directory <errors_path>                     Directory where errors buffer will placed.

Variants:

        Controller names:
                1. terminal - print output and errors and redirect stdin
                2. terminal&color - print output on green, success on blue, errors and fails on red
                3. terminal&file - print and save to files output and errors and redirect stdin
                4. file - save output and errors to files and simulate input with 'y' to bypass all prompts with yes

        Shell names:
                1. bash
"""
from pathlib import Path
import sys

from docopt import docopt

from src.app import main
from src.shell import SubShell
from src.cli_utils import (
    notify_mistake,
    parse_cli_output_input_controller,
    parse_cli_scripts_directory,
)
from src.exceptions import FileNotExecutable, FileNotFound
from src.temporary_errors_buffer import TempErrorFile
from src.output_input_controller import OutputInputController, TerminalOutputInput


if __name__ == "__main__":
    default_output_input_controller = TerminalOutputInput()
    # By default scripts are held in ./scripts directory
    default_scripts_directory = Path(sys.argv[0]).parent.joinpath("scripts")
    # By default errors buffer is in ./scripts directory
    default_error_buffer_directory = Path("/tmp")

    errors_directory = None
    shell_class = None

    args = docopt(__doc__)

    output_input_controller = (
        parse_cli_output_input_controller(args) or default_output_input_controller
    )

    scripts_directory = parse_cli_scripts_directory(args) or default_scripts_directory

    if args["-s"] or args["--shell"]:
        for shell_ in SubShell.__subclasses__():
            if args["<shell_name>"] == shell_.command_line_argument:
                try:
                    shell_class = shell_()
                    shell_class = shell_
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
        if not shell_class:
            notify_mistake(
                "Scripts shell ", f'"{args["<shell_name>"]}"', " was not found!!!"
            )
            exit(127)

    else:
        for shell_ in SubShell.__subclasses__():
            try:
                shell_class = shell_()
                shell_class = shell_
                break
            except FileNotFound:
                pass
            except FileNotExecutable:
                pass
        if not shell_class:
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
        shell=shell_class,
        script_folder_path=scripts_directory,
        oi_controller=output_input_controller,
        errors_buffer_path=errors_directory,
    )
