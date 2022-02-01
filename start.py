#!/bin/env python
"""
        Usage:
                doc_opt_test.py [-s SHELL] [-d SCRIPTS_DIRECTORY] [-o OUTPUT_INPUT_CONTROLLER] [-e ERRORS_BUFFER_PATH]

        Options:
                -s SHELL                        Shell by which scripts will be executed.
                -d SCRIPTS_DIRECTORY            Directory with scripts which will be executed.
                -o OUTPUT_INPUT_CONTROLLER      Input/Output handler.
                -e ERRORS_BUFFER_PATH           Path to temporary errors file buffer.

        Variants:

                Controller names:
                        1. terminal         print output and errors and redirect stdin to user terminal.
                        2. terminalcolor    print output on green, success on blue, errors and fails on
                                               red and redirect stidn to user terminal.
                        3. terminalfile     print and save output and errors to files with redirected
                                               stdin to user terminal.
                        4. file             save output and errors to files and simulate input with 'y'
                                               to bypass all prompts with yes.

                Shell names:
                        1. bash             execute scripts by /bin/bash.

"""
from pathlib import Path
import sys

from docopt import docopt

from src.app import main
from src.cli_utils import (
    parse_cli_output_input_controller,
    parse_cli_scripts_directory,
    parse_cli_shell,
    parse_cli_errors_directory,
    find_shell,
)
from src.output_input_controller import TerminalOutputInput
from src.exceptions import FileNotFound, FileNotExecutable

if __name__ == "__main__":
    default_output_input_controller = TerminalOutputInput()

    # By default scripts are held in ./scripts directory
    default_scripts_directory = Path(sys.argv[0]).parent.joinpath("scripts")

    # By default errors buffer is used in /tmp directory
    default_error_buffer_directory = Path("/tmp")

    args = docopt(__doc__)

    output_input_controller = (
        parse_cli_output_input_controller(args) or default_output_input_controller
    )

    scripts_directory = parse_cli_scripts_directory(args) or default_scripts_directory

    shell = parse_cli_shell(args) or find_shell()

    errors_directory = (
        parse_cli_errors_directory(args) or default_error_buffer_directory
    )

    main(
        shell=shell,
        script_folder_path=scripts_directory,
        oi_controller=output_input_controller,
        errors_buffer_path=errors_directory,
    )
