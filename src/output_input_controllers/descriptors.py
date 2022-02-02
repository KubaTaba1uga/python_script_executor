from typing import Tuple, TYPE_CHECKING
import sys


from src.output_input_controllers.base import BaseDescriptor
from src.output_input_controllers.utils import (
    create_logs_directory,
    get_log_file_path,
    format_error,
)
from src.utils import (
    print_error,
    print_info,
    print_,
)

if TYPE_CHECKING:
    from src.script_executor import ScriptExecutor


class SimpleTerminalInputDescriptor(BaseDescriptor):
    def __set__(self, instance, values: Tuple["ScriptExecutor", str]):
        script_executor, _ = values

        line = sys.stdin.readline()

        script_executor.shell.send_command(line)  # type:ignore

        instance.__dict__[self.name] = line


class TerminalOutputDescriptor(BaseDescriptor):
    def __set__(self, instance, values: Tuple["ScriptExecutor", str]):
        _, str_value = values

        print_(str_value)

        instance.__dict__[self.name] = str_value


class TerminalOutputDescriptorColor(BaseDescriptor):
    def __set__(self, instance, values: Tuple["ScriptExecutor", str]):
        _, str_value = values

        print_info(str_value)

        instance.__dict__[self.name] = str_value


class TerminalErrorDescriptor(BaseDescriptor):
    def __set__(self, instance, values: Tuple["ScriptExecutor", str]):
        _, str_value = values

        print_(format_error(str_value))

        instance.__dict__[self.name] = str_value


class TerminalErrorDescriptorColor(BaseDescriptor):
    def __set__(self, instance, values: Tuple["ScriptExecutor", str]):
        _, str_value = values

        print_error(format_error(str_value))

        instance.__dict__[self.name] = str_value


class TerminalFileOutputDescriptor(BaseDescriptor):
    @create_logs_directory
    def __set__(self, instance, values: Tuple["ScriptExecutor", str]):
        script_executor, str_value = values

        log_path = get_log_file_path(str(script_executor.script))

        with open(log_path, "a") as log:
            log.write(str_value)

        print_(str_value)

        instance.__dict__[self.name] = str_value


class TerminalFileErrorDescriptor(BaseDescriptor):
    @create_logs_directory
    def __set__(self, instance, values: Tuple["ScriptExecutor", str]):
        script_executor, str_value = values

        errors = format_error(str_value)

        log_path = get_log_file_path(str(script_executor.script))

        with open(log_path, "a") as log:
            log.write(errors)

        print_(errors)

        instance.__dict__[self.name] = str_value
