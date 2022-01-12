from pathlib import Path
import pytest

from src.shell import Shell
from src.script import Script
from tests.config import SCRIPTS_FOLDER

BASH_SCRIPT_NAME = ""

PYTHON_SHELL_PATH = Path("/usr/bin/python")


@pytest.fixture
def bash_shell():
    pass


@pytest.fixture
def python_shell():
    return Shell(PYTHON_SHELL_PATH)


@pytest.fixture
def python_script_output():
    return Script
