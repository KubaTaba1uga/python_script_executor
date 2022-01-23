"""
Environment, in which scripts will be executed in,
        it is precized by script first line. Example:
                #!/bin/bash - spawn shell /bin/bash
                                        before script execution

                #!/usr/bin/python - spawn shell /usr/bin/python
                                                  before script execution

"""
from typing import Dict
from pathlib import Path
import abc
import sys
import os


import pexpect

from src.exceptions import (
    FileNotFound,
    FileNotExecutable,
    NoOutputProduced,
    NoPidError,
    NoExitCodeError,
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

    def __enter__(self):
        self.spawn_shell()
        return self

    def __exit__(self, exc_type, exc_value, exc_tryceback):
        self.terminate()

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


class SubShell(Shell):
    """All shells should inherit from this class"""

    @property
    @abc.abstractclassmethod
    def subshell(cls) -> Dict[str, str]:
        """Dictionary which has characters for starting and ending
        a subshell. It is used for creating subshell commands.
        Example:
                 {"start": "(", "end": ")"}
        """
        return cls.subshell

    @property
    @abc.abstractclassmethod
    def subshell_pid(cls) -> Dict[str, str]:
        """Dictionary which holds subshell pid tag and
        subshell pid command. It is used for generating
        and recognizing subshell PID. Example:
                 {"tag": "bash_subshell_pid=", "command": "$BASHPID"}
        """
        return cls.subshell_pid

    @property
    @abc.abstractclassmethod
    def subshell_exit_code(cls) -> Dict[str, str]:
        """Dictionary which holds subshell exit code tag and
        subshell exit code command. It is used for generating
        and recognizing subshell exit code. Example:
                {"tag": "bash_subshell_exit_code=", "command": "$?"}
        """
        return cls.subshell_exit_code

    @classmethod
    def create_subshell_command(cls, command: str) -> str:
        """Change command provided as argument to
        be executed in subshell when revoked.
        Like in bash is done by adding paranthesesis around"""
        return f"{cls.subshell['start']}{command}{cls.subshell['end']}"

    @classmethod
    def create_subshell_pid_command(cls) -> str:
        """Create command which will echo the PID
        of subshell in which it is being revoked.
        Like in sh $PPID. Adding tag before PID
        is important for later PID recognization"""
        pid_tag = cls.subshell_pid["tag"]
        pid_command = cls.subshell_pid["command"]
        return f"echo {pid_tag}{pid_command}"

    @classmethod
    def _is_subshell_pid(cls, output: str) -> bool:
        """Decide is subshell PID within the output"""
        pid_tag = cls.subshell_pid["tag"]
        pid_command = cls.subshell_pid["command"]
        return pid_tag in output and pid_command not in output

    @classmethod
    def _extract_subshell_pid(cls, output: str) -> int:
        """Extract subshell PID from output"""
        pid_tag = cls.subshell_pid["tag"]
        pid_tag_end_index = output.find(pid_tag) + len(pid_tag)
        pid_end_index = output.find("\r\n")
        return int(output[pid_tag_end_index:pid_end_index])

    @classmethod
    def _create_subshell_exit_code_command(cls) -> str:
        """Create command which will echo the exit code
        of last subshell that is no longer running. Like in
        bash $?"""
        exit_code_tag = cls.subshell_exit_code["tag"]
        exit_code_command = cls.subshell_exit_code["command"]
        return f"echo {exit_code_tag}{exit_code_command}"

    @classmethod
    def _is_subshell_exit_code(cls, output: str) -> bool:
        """Decide is subshell exit code within output"""
        exit_code_tag = cls.subshell_exit_code["tag"]
        exit_code_command = cls.subshell_exit_code["command"]
        return exit_code_tag in output and exit_code_command not in output

    @classmethod
    def _extract_subshell_exit_code(cls, output: str) -> int:
        exit_code_tag = cls.subshell_exit_code["tag"]
        exit_code_tag_end_index = output.find(exit_code_tag) + len(exit_code_tag)
        exit_code_end_index = output.find("\r\n")
        return int(output[exit_code_tag_end_index:exit_code_end_index])

    def find_subshell_pid(self) -> int:
        """Get PID of last subshell"""
        for line in self:
            if self._is_subshell_pid(line):
                return self._extract_subshell_pid(line)
        raise NoPidError(f"No pid found for {self} subshell")

    def find_subshell_exit_code(self) -> int:
        """Find exit code of last subshell"""
        for line in self:
            if self._is_subshell_exit_code(line):
                return self._extract_subshell_exit_code(line)
        raise NoExitCodeError(f"No exit code found for {self} subshell")

    def get_subshell_exit_code(self) -> int:
        command = self._create_subshell_exit_code_command()
        self.send_command(command)
        return self.find_subshell_exit_code()


class BashShell(SubShell):
    path = "/bin/bash"

    subshell = {"start": "(", "end": ")"}

    subshell_pid = {"tag": "bash_subshell_pid=", "command": "$BASHPID"}

    subshell_exit_code = {"tag": "bash_subshell_exit_code=", "command": "$?"}

    def spawn_shell(self, timeout=5):
        """Spawn bash without user preferences to get cleaner output"""
        self.process = pexpect.spawn(
            self.path, args=["--norc"], encoding="utf-8", timeout=timeout
        )
