"""
Environment, in which scripts will be executed in,
        it is precized by script first line. Example:
                #!/bin/bash - spawn shell /bin/bash
                                        before script execution

                #!/usr/bin/python - spawn shell /usr/bin/python
                                                  before script execution

"""
from pathlib import Path

import pexpect

from src.exceptions import (
    FileNotFound,
    FileNotExecutable,
    NoOutputProduced,
)
from src.script import Script
from src.process import Process
from src.output_input_controller import OutputInputController


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
        if not Path(cls.FILE_NAME).exists():
            return False

        # If there is any content inside temp file return True
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

    def _spawn_shell(self, script: Script):
        """Spawn shell using self.path, and execute script within it."""
        self.process = pexpect.spawn(
            str(self.path),
            args=["str(script.path) 2> {_ErrorTempFile.FILE_NAME}"],
            encoding="utf-8",
        )

    def send_command(self, command: str):
        self.process.sendline(command)

    def terminate(self):
        self.process.terminate()

    def execute_script(
        self, script: Script, output_input: OutputInputController, timeout=30
    ):
        self._spawn_shell(script)

        while self.process.isalive():

            try:
                # Pass shell, to allow controll of process by
                #       output_input.stdout
                output_input.stdout = self, self._read_output(timeout)
            except NoOutputProduced as err:
                output_input.stdout = self, err.args[0]

            if _ErrorTempFile.errors_exist():
                # Pass shell, to allow controll of process by
                #       output_input.stderr
                output_input.stderr = self, _ErrorTempFile.read_errors()

            if Process.is_sleeping(self.process.pid):
                # Pass shell, to allow comunication with process by
                #       output_input.stdin
                output_input.stdin = self, None

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
                    f"There is no output produced by {script_name}"
                ) from err

        return self.process.before
