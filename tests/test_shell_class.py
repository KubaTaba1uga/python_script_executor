from pathlib import Path

import pytest
from pexpect.pty_spawn import spawn

from src.shell import Shell
from src.script import Script
from src.exceptions import FileNotFound, FileNotExecutable
from tests.config import SCRIPTS_FOLDER
from tests.fixtures import non_executable_path, non_existing_path

BASH_SCRIPTS = {"shebang": "bash_shebang_0.sh", "output": "bash_output_1.sh"}
BASH_SHELL_PATH = Path("/bin/bash")


PYTHON_SHELL_PATH = Path("/usr/bin/python")


@pytest.fixture
def bash_output_script():
    return Script(BASH_SCRIPTS["output"], SCRIPTS_FOLDER)


@pytest.fixture
def bash_shell():
    return Shell(BASH_SHELL_PATH)


def test_shell__init__errors(
    bash_shell, bash_output_script, non_existing_path, non_executable_path
):
    with pytest.raises(FileNotFound):
        Shell(non_existing_path)

    with pytest.raises(FileNotExecutable):
        Shell(non_executable_path)


def test_spawn_shell(bash_shell, bash_output_script):
    bash_shell.spawn_shell(bash_output_script)
    assert isinstance(bash_shell.process, spawn)
