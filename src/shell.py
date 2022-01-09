"""
Environment, in which scripts will be executed in
        is precized by script first line. Example:
                #!/bin/bash - spawn shell /bin/bash
                                        before script execution

                #!/usr/bin/python - spawn shell /usr/bin/python
                                                  before script execution

"""
import os
import pathlib
import pexpect

from src.exceptions import (
    FileNotFoundOrNotExecutable,
    FileNotFound,
    FileNotExecutable,
    TimeoutReached,
    NoOutputProduced,
)
from src.script import Script, ScriptName
from src.process import Process
from src.output import OutputInput


def xyz_required(question: str) -> bool:
    input_invalid = True
    while input_invalid:
        ask_for_input = input(question)
        if ask_for_input in (
            "y",
            "n",
        ):
            input_invalid = False
        else:
            print("Input invalid!!!")

    return ask_for_input == "y"


def input_required() -> bool:
    return xyz_required(
        "Would You like to insert input into an script execution [y/n]?"
    )


def termination_required() -> bool:
    return xyz_required("Would You like to terminate script execution [y/n]?")


class Shell:
    """Shell module is responsible for spawning the environment
    and for communicating with it."""

    def __init__(self, path: pathlib.Path):
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
        try:
            self.process = pexpect.spawn(
                str(self.path), args=[str(script.path)], encoding="utf-8"
            )
            self.script = script
        except pexpect.ExceptionPexpect as err:
            raise FileNotFoundOrNotExecutable from err

    def send_command(self, command: str):
        self.process.sendline(command)

    def execute_script(self, script: Script, output_input: OutputInput, timeout=30):
        self.spawn_shell(script)
        while self.process.isalive():
            # Read output from script
            try:
                output_input.write_output(self.read_output(timeout))
            except NoOutputProduced:
                output_input.write_output(
                    f"There where no output produced by {script.name}"
                )
            # Print output to destinations
            output_input.print_output()

            # If process is sleeping assume it needs human interaction
            if Process.is_sleeping(self.process.pid):

                if input_required():
                    output_input.ask_for_input()
                    self.send_command(output_input.std_input)
                elif termination_required():
                    self.process.terminate()

        if self.process.status == 0:
            output_input.print_success(script.name)
        else:
            output_input.print_failure(script.name)

    def read_output(self, timeout=30) -> str:
        """Read all output lines from shell. If output is not
        recived before timeout return what left"""
        try:
            self.process.expect(pexpect.EOF, timeout=timeout)
        except pexpect.TIMEOUT:
            if not self.process.before:
                raise NoOutputProduced(
                    "There is no output produced from {self.script.name}"
                )

        return self.process.before
