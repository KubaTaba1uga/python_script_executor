"""
Environment, in which scripts will be executed in
        is precized by script first line. Example:
                #!/bin/bash - spawn shell /bin/bash
                                        before script execution

                #!/usr/bin/python - spawn shell /usr/bin/python
                                                  before script execution

"""
from pathlib import Path

import pexpect

from src.exceptions import (
    FileNotFoundOrNotExecutable,
    FileNotFound,
    FileNotExecutable,
    TimeoutReached,
    NoOutputProduced,
)
from src.script import Script
from src.process import Process
from src.output import OutputInput


def xyz_required(question: str) -> bool:
    """Ask question until correct choice is not provided"""
    input_invalid = True
    while input_invalid:
        ask_for_input = input(question + " ([y]/n)" + " " * 2)
        if not bool(ask_for_input):
            ask_for_input = "y"
        if ask_for_input in (
            "y",
            "n",
        ):
            input_invalid = False
        else:
            print("Input invalid!!!")

    return ask_for_input == "y"


def input_required() -> bool:
    return xyz_required("Would You like to insert input into an script execution?")


def termination_required() -> bool:
    return xyz_required("Would You like to terminate script execution?")


class _ErrorTempFile:
    FILE_NAME = "errors_temp.log"

    @classmethod
    def read_errors(cls):
        """Read errors from file and clean buffer"""
        with open(cls.FILE_NAME, "r+") as temp_errors:
            error_content = temp_errors.read()
            # Move pointer to file beginning
            temp_errors.seek(0)
            # Resize file to pointer position
            temp_errors.truncate()
        return error_content

    @classmethod
    def errors_exist(cls):
        """If there is any content inside temp file return True"""
        with open(cls.FILE_NAME) as temp_errors:
            # Delete whitespaces which could be misleading
            #   for bool function
            return bool(temp_errors.read().strip())


class Shell:
    """Shell module is responsible for spawning the environment
    and for communicating with it."""

    def __init__(self, path: Path):
        """path should be pointing to executable shell
        like /usr/bin/python3"""
        if not path.exists():
            raise FileNotFound(f"{path} not found")
        if not pexpect.utils.is_executable_file(path):
            raise FileNotExecutable(f"{path} is not executable")

        self.path = path
        self.process = None
        self.script = None

    def spawn_shell(self, script: Script):
        """Spawn shell using self.path, and execute script within it."""
        self.process = pexpect.spawn(
            str(self.path),
            args=[str(script.path), f"2> {_ErrorTempFile.FILE_NAME}"],
            encoding="utf-8",
        )

    def send_command(self, command: str):
        self.process.sendline(command)

    def terminate(self):
        self.process.terminate()

    def execute_script(self, script: Script, output_input: OutputInput, timeout=30):
        self.spawn_shell(script)
        while self.process.isalive():
            try:
                # Pass shell, to allow controll of process by output_input
                #       for future output analysis extending
                output_input.stdout = (self, self._read_output(timeout))
            except NoOutputProduced as err:
                output_input.stdout = (self, err.args[0])

            if _ErrorTempFile.errors_exist():
                # Pass shell, to allow controll of process by output_input
                #       for future extending error response
                output_input.stderr = (self, _ErrorTempFile.read_errors())

        if self.process.status == 0:
            output_input.print_success(script.name)
        else:
            output_input.print_failure(script.name)

    def _read_output(self, script_name: str, timeout=30) -> str:
        """Read all output lines from shell. If output is not
        recived before timeout return what left"""
        try:
            self.process.expect(pexpect.EOF, timeout=timeout)
        except pexpect.TIMEOUT as err:
            if not self.process.before:
                raise NoOutputProduced(
                    "There is no output produced by {script_name}"
                ) from err

        return self.process.before
