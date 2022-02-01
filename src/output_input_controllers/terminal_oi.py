from src.output_input_controllers.base import OutputInputController
from src.output_input_controllers.descriptors import (
    SimpleTerminalInputDescriptor,
    TerminalOutputDescriptor,
    TerminalErrorDescriptor,
)


class TerminalOutputInput(OutputInputController):
    stdin = SimpleTerminalInputDescriptor()
    stdout = TerminalOutputDescriptor()
    stderr = TerminalErrorDescriptor()

    command_line_argument = "terminal"
