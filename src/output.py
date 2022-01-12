import abc


class BaseDescriptor(abc.ABC):
    def __set_name__(self, cls, name):
        self.name = name

    @abc.abstractmethod
    def __set__(self, instance, value):
        instance.__dict__[self.name] = value

    @abc.abstractmethod
    def __get__(self, instance, cls):
        return instance.__dict__[self.name]


class OutputInput(abc.ABC):
    """Class responsible for receiving stdout,
    stderr and stdin.

    Use descriptors to override abstract class properties.
    """

    @abc.abstractclassmethod
    def print_success(cls, script_name: str):
        print(f"Execution of {script_name} succeed")

    @abc.abstractclassmethod
    def print_failure(cls, script_name: str):
        print(f"Execution of {script_name} failed")

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


class TerminalOutputDescriptor(BaseDescriptor):
    def __set__(self, instance, value):
        print(value)
        instance.__dict__[self.name] = value

    def __get__(self, instance, cls):
        return instance.__dict__[self.name]


class TerminalInputDescriptor(BaseDescriptor):
    def __set__(self, instance, value):
        value = input("\n" + "Input: ")
        instance.__dict__[self.name] = value

    def __get__(self, instance, cls):
        return instance.__dict__[self.name]


class TerminalErrorDescriptor(BaseDescriptor):
    def __set__(self, instance, value):

        print("ERROR\n" + " " * 4 + f"{value}" + "\nERROR")

        instance.__dict__[self.name] = value

    def __get__(self, instance, cls):
        return instance.__dict__[self.name]


class TerminalOutputInput(OutputInput):
    stdin = TerminalInputDescriptor()
    stdout = TerminalOutputDescriptor()
    stderr = TerminalErrorDescriptor()

    @classmethod
    def print_success(cls, script_name: str):
        print(f"Execution of {script_name} succeed")

    @classmethod
    def print_failure(cls, script_name: str):
        print(f"Execution of {script_name} failed")
