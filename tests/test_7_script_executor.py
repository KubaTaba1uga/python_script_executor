from pathlib import Path
import os

import pytest

from tests.fixtures import (
    bash_output_script,
    bash_shell,
    terminal_oi,
    temp_err_buffer,
    script_executor,
    script_create_file,
)
from src.script_executor import ScriptExecutor
from src.exceptions import ShellNotSpawned


@pytest.fixture
def executor_create_file(bash_shell, script_create_file, terminal_oi, temp_err_buffer):
    bash_shell.spawn_shell(timeout=0.2)
    return ScriptExecutor(script_create_file, bash_shell, terminal_oi, temp_err_buffer)


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


def test_execute_script(executor_create_file):
    file_path = Path("/tmp/test_file")
    with executor_create_file.shell:
        executor_create_file.execute_script()
        assert file_path.exists() is True
        os.remove(file_path)
