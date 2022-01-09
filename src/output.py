import abc

from src.script import ScriptName


class OutputInput(abc.ABC):
    """Class responsible for printing stdout,
    and asking for user input"""

    def __init__(self):
        self.std_output = None
        self.std_input = None

    @abc.abstractmethod
    def write_output(self, output: str):
        self.std_output = output

    @abc.abstractmethod
    def print_output(self):
        print(self.std_output)

    @abc.abstractmethod
    def ask_for_input(self):
        self.std_input = input("Input: ")

    @abc.abstractclassmethod
    def print_success(cls, script_name: ScriptName):
        print(f"Execution of {script_name} succeed")

    @abc.abstractclassmethod
    def print_failure(cls, script_name: ScriptName):
        print(f"Execution of {script_name} failed")


class TerminalOutput(OutputInput):
    def write_output(self, output: str):
        self.std_output = output

    def print_output(self):
        print(self.std_output)

    def ask_for_input(self):
        self.std_input = input("Input: ")

    @classmethod
    def print_success(cls, script_name: ScriptName):
        print(f"Execution of {script_name} succeed")

    @classmethod
    def print_failure(cls, script_name: ScriptName):
        print(f"Execution of {script_name} failed")
