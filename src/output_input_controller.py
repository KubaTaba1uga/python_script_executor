import abc


class BaseDescriptor(abc.ABC):
    def __set_name__(self, cls, name):
        self.name = name

    @abc.abstractmethod
    def __set__(self, instance, value_tuple):
        """Receive shell and value to allow
        OutputInputController children
        for controlling shell process"""

        shell, value = value_tuple

        instance.__dict__[self.name] = value

    @abc.abstractmethod
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
    def print_success(cls, script_name: str):
        print("\n" + f"Execution of {script_name} succeed" + "\n")

    @classmethod
    def print_failure(cls, script_name: str):
        print("\n" + f"Execution of {script_name} failed" + "\n")

    @property
    @abc.abstractclassmethod
    def stdin(cls):
        return cls.stdin

    @property
    @abc.abstractclassmethod
    def stdout(cls):
        return cls.stdout

    @property
    @abc.abstractclassmethod
    def stderr(cls):
        return cls.stderr

    @property
    @abc.abstractclassmethod
    def command_line_flag(cls):
        """Flag that user passes at script execution, example: python start.py -s
        it is used for app to know which OutputInputController should be used.
        """
        return "-s"


class TerminalOutputDescriptor(BaseDescriptor):
    def __set__(self, instance, value_tuple):
        _shell, value = value_tuple

        print(value)

        instance.__dict__[self.name] = value

    def __get__(self, instance, cls):
        return instance.__dict__[self.name]


class TerminalInputDescriptor(BaseDescriptor):
    def __set__(self, instance, value_tuple):
        """When revoked ask user for input,
        instead of using value_tuple[1] parameter"""

        value = input("\n" + "Input: ")

        instance.__dict__[self.name] = value

    def __get__(self, instance, cls):
        return instance.__dict__[self.name]


class TerminalErrorDescriptor(BaseDescriptor):
    def __set__(self, instance, value_tuple):
        _shell, value = value_tuple
        double_newline = "\n" * 2
        tab = " " * 4
        print(
            double_newline
            + "ERROR!!!"
            + double_newline
            + tab
            + f"{value}"
            + double_newline
            + "ERROR!!!",
            end=double_newline,
        )

        instance.__dict__[self.name] = value

    def __get__(self, instance, cls):
        return instance.__dict__[self.name]


class TerminalOutputInput(OutputInputController):
    stdin = TerminalInputDescriptor()
    stdout = TerminalOutputDescriptor()
    stderr = TerminalErrorDescriptor()
    command_line_flag = "-t"
