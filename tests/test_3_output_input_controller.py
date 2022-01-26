from contextlib import contextmanager
from pathlib import Path
from io import StringIO
import sys

import pytest

from tests.config import replace_stdin
from tests.fixtures import bash_shell, terminal_oi
from src.output_input_controller import OutputInputController


def test_terminal_output(bash_shell, terminal_oi):
    with bash_shell as shell:
        output_notification = "This is standard output notification"
        terminal_oi.stdout = shell, output_notification, 0
        assert terminal_oi.stdout == output_notification


def test_terminal_error(bash_shell, terminal_oi):
    with bash_shell as shell:
        error_notification = "This is standard error notification"
        terminal_oi.stderr = shell, error_notification, 0
        assert terminal_oi.stderr == error_notification


def test_terminal_input(bash_shell, terminal_oi):
    input_notification = "This is standard input"
    with bash_shell as shell:
        with replace_stdin(input_notification):
            terminal_oi.stdin = shell, None, -1
            assert terminal_oi.stdin == input_notification
            # Prettify pytest -s formatting
            print(terminal_oi.stdin)


def test_command_line_flags():
    """Ensure each OIController subclass has
    command line flag implemented properly"""
    for cls in OutputInputController.__subclasses__():
        assert cls.command_line_argument is not None
