"""
Environment, in which scripts will be executed in
        is precized by script first line. Example:
                #!/bin/bash - spawn shell /bin/bash
                                        before script execution

                #!/usr/bin/python - spawn shell /usr/bin/python
                                                  before script execution

"""
import os
import sys
import pathlib
from abc import ABC, abstractmethod, abstractclassmethod
import pexpect

from exceptions import (
    FileNotFoundOrNotExecutable,
    FileNotFound,
    FileNotExecutable,
    NoOutputProduced,
)


def is_executable(path: pathlib.Path) -> bool:
    return os.path.isfile(path) and os.access(path, os.X_OK)


class Shell(ABC):
    """Shell module is responsible for spawning the environment
    and for communicating with it."""

    def __init__(self, path: pathlib.Path):
        """path should be pointing to executable shell
        like /usr/bin/python3"""
        if not path.exists():
            raise FileNotFound
        if not is_executable(path):
            raise FileNotExecutable

        self.path = path
        self.process = None

    def spawn_shell(self):
        """Spawn shell using self.path"""
        try:
            self.process = pexpect.spawn(str(self.path))
        except pexpect.ExceptionPexpect as err:
            raise FileNotFoundOrNotExecutable from err

    def send_command(self, command: str):
        self.process.sendline(command)

    @abstractmethod
    def read_output(self, timeout=30) -> str:
        """Read all output lines from shell, if output is not
        recived by timeout, assume it is not exsisting"""

    @abstractmethod
    def read_line(self, timeout=30) -> str:
        """Read one line from shells output"""
        self.process.expect("\r\n", timeout=timeout)
        return self.process.before.decode("utf-8")
