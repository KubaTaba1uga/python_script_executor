"""
Environment, in which scripts will be executed in,
        it is precized by script first line. Example:
                #!/bin/bash - spawn shell /bin/bash
                                        before script execution

                #!/usr/bin/python - spawn shell /usr/bin/python
                                                  before script execution

"""
from pathlib import Path
import abc
import sys
import os


import pexpect

from src.exceptions import (
    FileNotFound,
    FileNotExecutable,
    NoOutputProduced,
)
from src.script import Script
from src.process import Process
from src.output_input_controller import OutputInputController
from src.temporary_errors_buffer import TempErrorFile


class Shell(abc.ABC):
    """Shell module is responsible for spawning the  environment
    in which scripts will be executed and for communicating with them."""

    @property
    @abc.abstractclassmethod
    def path(cls):
        """Path to shell by which all scripts will be executed, for example:
        /bin/bash
        /bin/env zsh
        /bin/sh
        """
        return cls.path

    def __init__(self):
        path = Path(self.path)

        if not path.exists():
            raise FileNotFound(f"{path} not found")
        if not pexpect.utils.is_executable_file(path):
            raise FileNotExecutable(f"{path} is not executable")

        self.process = None

    def __iter__(self):
        while line := self.read_output_line():
            yield line

    def spawn_shell(self, timeout=5):
        """Spawn shell using self.path, and execute script within it."""
        self.process = pexpect.spawn(self.path, encoding="utf-8", timeout=timeout)

    def send_command(self, command: str):
        """Send command to shell"""
        self.process.sendline(command)

    def terminate(self):
        """Terminate shell, when no scripts are left for execution"""
        self.process.terminate()

    def read_output_all(self, script_name: str) -> str:
        """Read all output lines from shell. If output is not
        recived before timeout return what has left"""
        try:
            self.process.expect(pexpect.EOF)
        except pexpect.TIMEOUT as err:
            if not self.process.before:
                raise NoOutputProduced(
                    f"There is no output produced by {script_name}"
                ) from err

        return self.process.before

    def read_output_line(self) -> str:
        try:
            return self.process.readline()
        except pexpect.TIMEOUT:
            return ""


class BashShell(Shell):
    path = "/bin/bash"
