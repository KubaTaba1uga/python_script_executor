from pathlib import Path

import pytest
from pexpect.pty_spawn import spawn

from src.shell import Shell
from src.script import Script
from src.exceptions import FileNotFound, FileNotExecutable
from tests.config import SCRIPTS_FOLDER
from tests.fixtures import (
    non_executable_path,
    non_existing_path,
    bash_shell,
    bash_output_script,
    bash_input_script,
)


def test__init__errors(
    bash_shell, bash_output_script, non_existing_path, non_executable_path
):
    with pytest.raises(FileNotFound):
        Shell(non_existing_path)

    with pytest.raises(FileNotExecutable):
        Shell(non_executable_path)


def test__spawn_shell(bash_shell, bash_output_script):
    bash_shell._spawn_shell(bash_output_script)
    assert isinstance(bash_shell.process, spawn)


def test_send_command(bash_shell, bash_input_script):
    bash_shell._spawn_shell
