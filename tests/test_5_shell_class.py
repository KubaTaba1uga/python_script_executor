from pathlib import Path

import pytest
from pexpect.pty_spawn import spawn
from pexpect.exceptions import TIMEOUT

from src.shell import SubShell
from src.process import Process
from src.exceptions import FileNotFound, FileNotExecutable
from tests.fixtures import (
    non_executable_path,
    non_existing_path,
    bash_shell,
    bash_output_script,
    terminal_oi,
    bash_error_script,
)


def test__init__errors(non_existing_path, non_executable_path):
    for cls in SubShell.__subclasses__():
        shell_org_path = cls.path

        cls.path = non_existing_path
        with pytest.raises(FileNotFound):
            cls()

        cls.path = non_executable_path
        with pytest.raises(FileNotExecutable):
            cls()

        cls.path = shell_org_path


def test__spawn_shell():
    for cls in SubShell.__subclasses__():
        shell = cls()
        shell.spawn_shell()
        assert isinstance(shell.process, spawn)
        Process.kill(shell.process.pid)


def test_terminate():
    for cls in SubShell.__subclasses__():
        shell = cls()
        shell.spawn_shell()
        shell.terminate()
        assert shell.process.isalive() is False


def test__ctx_manager_shell():
    for cls in SubShell.__subclasses__():
        sh = cls()
        with sh as shell:
            assert isinstance(shell.process, spawn)
        assert sh.process.isalive() is False


def test_send_command():
    for cls in SubShell.__subclasses__():
        with cls() as shell:
            notification = "This is standard output"
            shell.send_command(f"echo {notification}")
            shell.process.expect(TIMEOUT, timeout=0.2)
            assert notification in shell.process.before


def test_read_output_all():
    notification = "This is standard output"
    for cls in SubShell.__subclasses__():
        with cls() as shell:
            shell.send_command(f"echo {notification}")
            assert notification in shell.read_output_all("test read output all", 0.2)


def test_read_output_line():
    notification = "This is standard output"
    notification_found = False

    for cls in SubShell.__subclasses__():
        shell = cls()

        shell.spawn_shell(timeout=0.2)
        shell.send_command(f"echo {notification}")

        while line := shell.read_output_line():
            if notification in line:
                notification_found = True

        assert notification_found is True


def test__iter__():

    notification = "This is standard output"
    notification_found = False

    for cls in SubShell.__subclasses__():
        shell = cls()

        shell.spawn_shell(timeout=0.2)
        shell.send_command(f"echo {notification}")

        for line in shell:
            if notification in line:
                notification_found = True

        assert notification_found is True


def test_command_line_argument():
    for cls in SubShell.__subclasses__():
        assert isinstance(cls.command_line_argument, str)
