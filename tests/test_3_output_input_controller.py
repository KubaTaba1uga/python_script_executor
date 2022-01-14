from contextlib import contextmanager
from pathlib import Path
from io import StringIO
import sys

import pytest

from src.output_input_controller import TerminalOutputInput, OutputInputController
from src.shell import Shell


@pytest.fixture
def shell():
    shell_path = Path("/bin/bash")
    return Shell(shell_path)


@pytest.fixture
def terminal_oi():
    return TerminalOutputInput()


@contextmanager
def replace_stdin(input_string):
    org_stdin = sys.stdin
    sys.stdin = StringIO(input_string)
    yield None
    sys.stdin = org_stdin


def test_terminal_output(shell, terminal_oi):
    output_notification = "This is standard output notification"
    terminal_oi.stdout = shell, output_notification
    assert terminal_oi.stdout == output_notification


def test_terminal_error(shell, terminal_oi):
    error_notification = "This is standard error notification"
    terminal_oi.stderr = shell, error_notification
    assert terminal_oi.stderr == error_notification


def test_terminal_input(shell, terminal_oi):
    input_notification = "This is standard input"
    with replace_stdin(input_notification):
        terminal_oi.stdin = shell, None
        assert terminal_oi.stdin == input_notification
        # Prettify pytest -s formatting
        print(terminal_oi.stdin)


def test_command_line_flags():
    """Ensure each OIController subclass has
    command line flag implemented properly"""
    for cls in OutputInputController.__subclasses__():
        assert cls.command_line_flag[0] == "-"
