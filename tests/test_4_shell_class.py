from pathlib import Path

import pytest
from pexpect.pty_spawn import spawn
from pexpect.exceptions import TIMEOUT

from src.shell import Shell
from src.exceptions import FileNotFound, FileNotExecutable
from tests.fixtures import (
    non_executable_path,
    non_existing_path,
    bash_shell,
    bash_output_script,
    bash_shell_script,
    terminal_oi,
    bash_error_script,
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


def test__spawn_shell_error(bash_shell, bash_error_script):
    bash_shell._spawn_shell(bash_error_script)


def test__read_output(bash_shell, bash_output_script):
    bash_shell._spawn_shell(bash_output_script)
    output_content = bash_shell._read_output(str(bash_output_script.name))
    desired_output_content = (
        "\r\n".join([str(i) for i in range(1, 11)]) + "\r\n" + "All done" + "\r\n"
    )
    assert desired_output_content == output_content


def test_send_command(bash_shell, bash_shell_script):
    notification = "This is standard notification"
    bash_shell._spawn_shell(bash_shell_script)
    bash_shell.send_command(f"echo {notification}")
    bash_shell.process.expect(TIMEOUT, timeout=0.3)
    assert notification in bash_shell.process.before
    bash_shell.process.terminate()


def test_terminate(bash_shell, bash_shell_script):
    bash_shell._spawn_shell(bash_shell_script)
    bash_shell.terminate()
    assert bash_shell.process.isalive() is False


def test_execute_script_error(bash_shell, bash_error_script, terminal_oi):
    bash_shell.execute_script(bash_error_script, terminal_oi)
