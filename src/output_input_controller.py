from typing import TYPE_CHECKING
from typing import Tuple
from time import sleep
import abc

from src.process import Process
from src.utils import waiting_termination_continue_input

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

    def __init__(self):
        # Flag is responsible for skipping script execution.
        # In case a user would like to execute next script
        # without killing previous one. It is useful feature
        # for ssh loging when user would like to not terminate
        # connection and execute scripts on remote machine.
        self.continue_flag = False

    @classmethod
    def show_success(cls, script_name: str):
        print("\n" + f"Execution of {script_name} succeed" + "\n")

    @classmethod
    def show_failure(cls, script_name: str):
        print("\n" + f"Execution of {script_name} failed" + "\n")

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


class TerminalOutputDescriptor(BaseDescriptor):
    def __set__(self, instance, values: Tuple["SubShell", str, int]):
        _shell, str_value, subshell_pid = values

        print(str_value)

        instance.__dict__[self.name] = str_value


class TerminalInputDescriptor(BaseDescriptor):
    WAITING = "w"
    WAITING_PERIOD = 30
    TERMINATION = "t"
    CONTINUE = "c"

    def __set__(self, instance, values: Tuple["SubShell", str, int]):
        """Ask user for input only when process
        is sleeping. This is not ideal solution,
        however i couldn't find any better"""
        shell, str_value, subshell_pid = values

        if Process.is_sleeping(subshell_pid):
            str_value = waiting_termination_continue_input(
                self.WAITING, self.WAITING_PERIOD, self.TERMINATION, self.CONTINUE
            )

            if str_value.lower() == self.WAITING:
                sleep(self.WAITING_PERIOD)
            elif str_value.lower() == self.TERMINATION:
                Process.kill(subshell_pid)
            elif str_value.lower() == self.CONTINUE:
                instance.continue_flag = True
            else:
                shell.send_command(str_value)

        instance.__dict__[self.name] = str_value


class TerminalErrorDescriptor(BaseDescriptor):
    def __set__(self, instance, values: Tuple["SubShell", str, int]):
        _shell, str_value, subshell_pid = values

        double_newline = "\n" * 2

        tab = " " * 4

        print(
            double_newline
            + "ERROR!!!"
            + double_newline
            + tab
            + f"{str_value}"
            + double_newline
            + "ERROR!!!",
            end=double_newline,
        )

        instance.__dict__[self.name] = str_value


class TerminalOutputInput(OutputInputController):
    stdin = TerminalInputDescriptor()
    stdout = TerminalOutputDescriptor()
    stderr = TerminalErrorDescriptor()

    command_line_argument = "terminal"
