from pathlib import Path
import pytest

from src.shell import Shell
from src.script import Script

BASH_SHELL_PATH = Path("/bin/bash")

PYTHON_SHELL_PATH = Path("/usr/bin/python")


@pytest.fixture
def bash_shell():
    return Shell(BASH_SHELL_PATH)


@pytest.fixture
def python_shell():
    return Shell(PYTHON_SHELL_PATH)
