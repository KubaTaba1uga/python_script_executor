from pathlib import Path

import pytest

from src.shell import Shell
from src.output_input_controller import TerminalOutputInput


@pytest.fixture
def shell():
    shell_path = Path("/bin/bash")
    return Shell(shell_path)


@pytest.fixture
def terminal_oi():
    return TerminalOutputInput()


def test_terminal_output(shell, terminal_oi):
    output_notification = "This is standard output notification"
    terminal_oi.stdout = shell, output_notification
    assert terminal_oi.stdout == output_notification
