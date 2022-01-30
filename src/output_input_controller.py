from typing import TYPE_CHECKING
from typing import Tuple
from time import sleep
import abc
import sys

from src.process import Process
from src.utils import (
    print_error,
    print_info,
    print_success,
    print_,
)

if TYPE_CHECKING:
    from src.shell import SubShell


class BaseDescriptor(abc.ABC):
    def __set_name__(self, cls, name: str):
        self.name = name

    def __set__(self, instance, values: Tuple["SubShell", str, int]):
        """Receive shell, value and subshell PID
        to allow OutputInputController children
        for controlling processes behaviour"""

        shell, str_value, subshell_pid = values

        instance.__dict__[self.name] = str_value

    def __get__(self, instance, cls):
        return instance.__dict__[self.name]


class OutputInputController(abc.ABC):
    """Class responsible for handling terminal streams.
            Responsibilities description:

                receiving stdin and deciding what to do
                    with process that input was received from

                receiving stdout and deciding what to do
                    with process that output was received from

                receiving stderr and deciding what to do
                    with process that error was received from

    Use descriptors to override abstract class properties.
    """

    @classmethod
    def show_success(cls, script_name: str):
        print_("\n" + f"Execution of {script_name} succeed" + "\n" * 2)

    @classmethod
    def show_failure(cls, script_name: str):
        print_("\n" + f"Execution of {script_name} failed" + "\n" * 2)

    @classmethod
    def show_status(cls, script_name: str, exit_code: int):
        if exit_code == 0:
            cls.show_success(script_name)
        else:
            cls.show_failure(script_name)

    @property
    @classmethod
    def command_line_argument(cls) -> str:
        """Argument that user passes at script execution to select output input controller,
        for example: python start.py -o outputinputcontroller
        """
        return cls.__name__.lower()

    @classmethod
    @property
    @abc.abstractmethod
    def stdin(cls) -> BaseDescriptor:
        return BaseDescriptor()

    @classmethod
    @property
    @abc.abstractmethod
    def stdout(cls) -> BaseDescriptor:
        return BaseDescriptor()

    @classmethod
    @property
    @abc.abstractmethod
    def stderr(cls) -> BaseDescriptor:
        return BaseDescriptor()


class SimpleTerminalInputDescriptor(BaseDescriptor):
    def __set__(self, instance, values: Tuple["SubShell", str, int]):
        shell, str_value, subshell_pid = values

        line = sys.stdin.readline()

        shell.send_command(line)


class TerminalOutputDescriptor(BaseDescriptor):
    def __set__(self, instance, values: Tuple["SubShell", str, int]):
        _shell, str_value, subshell_pid = values

        print_(str_value)

        instance.__dict__[self.name] = str_value


class TerminalErrorDescriptor(BaseDescriptor):
    def __set__(self, instance, values: Tuple["SubShell", str, int]):
        _shell, str_value, subshell_pid = values

        double_newline = "\n" * 2

        tab = " " * 4

        print_(
            double_newline
            + "ERROR!!!"
            + double_newline
            + tab
            + f"{str_value}"
            + "\n"
            + "ERROR!!!"
            + "\n" * 2
        )

        instance.__dict__[self.name] = str_value


class TerminalOutputInput(OutputInputController):
    stdin = SimpleTerminalInputDescriptor()
    stdout = TerminalOutputDescriptor()
    stderr = TerminalErrorDescriptor()

    command_line_argument = "terminal"


class TerminalOutputDescriptorColor(BaseDescriptor):
    def __set__(self, instance, values: Tuple["SubShell", str, int]):
        _shell, str_value, subshell_pid = values

        print_info(str_value)

        instance.__dict__[self.name] = str_value


class TerminalErrorDescriptorColor(BaseDescriptor):
    def __set__(self, instance, values: Tuple["SubShell", str, int]):
        _shell, str_value, subshell_pid = values

        double_newline = "\n" * 2

        tab = " " * 4

        print_error(
            double_newline
            + "ERROR!!!"
            + double_newline
            + tab
            + f"{str_value}"
            + "\n"
            + "ERROR!!!"
            + "\n" * 2
        )

        instance.__dict__[self.name] = str_value


class TerminalOutputInputColor(OutputInputController):
    stdin = SimpleTerminalInputDescriptor()
    stdout = TerminalOutputDescriptorColor()
    stderr = TerminalErrorDescriptorColor()

    command_line_argument = "terminal&color"

    @classmethod
    def show_success(cls, script_name: str):
        print_success("\n" + f"Execution of {script_name} succeed" + "\n" * 2)

    @classmethod
    def show_failure(cls, script_name: str):
        print_error("\n" + f"Execution of {script_name} failed" + "\n" * 2)
