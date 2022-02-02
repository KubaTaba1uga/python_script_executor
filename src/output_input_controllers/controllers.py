from src.output_input_controllers.base import OutputInputController
from src.output_input_controllers.descriptors import (
    SimpleTerminalInputDescriptor,
    TerminalOutputDescriptor,
    TerminalErrorDescriptor,
    TerminalFileOutputDescriptor,
    TerminalFileErrorDescriptor,
    TerminalOutputDescriptorColor,
    TerminalErrorDescriptorColor,
)
from src.utils import (
    format_indent,
    print_error,
    print_success,
)


class TerminalOutputInput(OutputInputController):
    stdin = SimpleTerminalInputDescriptor()
    stdout = TerminalOutputDescriptor()
    stderr = TerminalErrorDescriptor()

    command_line_argument = "terminal"


class TerminalOutputInputColor(OutputInputController):
    stdin = SimpleTerminalInputDescriptor()
    stdout = TerminalOutputDescriptorColor()
    stderr = TerminalErrorDescriptorColor()

    command_line_argument = "terminalcolor"

    @classmethod
    def show_success(cls, script_name: str):
        print_success(format_indent(f"Execution of {script_name} succeed" + "\n"))

    @classmethod
    def show_failure(cls, script_name: str):
        print_error(format_indent(f"Execution of {script_name} failed" + "\n"))


class TerminalFileOutputInput(OutputInputController):
    stdin = SimpleTerminalInputDescriptor()
    stdout = TerminalFileOutputDescriptor()
    stderr = TerminalFileErrorDescriptor()

    command_line_argument = "terminalfile"
