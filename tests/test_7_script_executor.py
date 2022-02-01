from pathlib import Path
import os

import pytest

from tests.fixtures import (
    bash_output_script,
    bash_shell,
    terminal_oi,
    temp_err_buffer,
    script_executor,
)
from tests.config import replace_stdin
from src.script_executor import ScriptExecutor
from src.exceptions import ShellNotSpawned


def test__init__errors(bash_output_script, bash_shell, terminal_oi, temp_err_buffer):
    with pytest.raises(TypeError):
        ScriptExecutor("it is not script", bash_shell, terminal_oi, temp_err_buffer)

    with pytest.raises(TypeError):
        ScriptExecutor(
            bash_output_script, "this is not shell", terminal_oi, temp_err_buffer
        )

    with pytest.raises(TypeError):
        ScriptExecutor(
            bash_output_script,
            bash_shell,
            "this is not output input controller",
            temp_err_buffer,
        )

    with pytest.raises(ShellNotSpawned):
        ScriptExecutor(bash_output_script, bash_shell, terminal_oi, temp_err_buffer)


def test_pid(script_executor):
    pid_command = script_executor.shell.create_subshell_pid_command()
    with script_executor.shell as sh:
        sh.send_command(pid_command)
        assert isinstance(script_executor.pid, int)


def test_exit_code(script_executor):
    command = "ls"
    with script_executor.shell as sh:
        sh.send_command(command)
        assert script_executor.exit_code == 0


def test__create_execution_command(script_executor):
    command = script_executor._create_execution_command()
    with script_executor.shell as sh:
        sh.send_command(command)
        assert isinstance(script_executor.pid, int)
        assert script_executor.exit_code == 0
