import pytest

from src.app import main
from tests.fixtures import bash_shell, terminal_oi
from tests.config import replace_stdin, GOOD_SCRIPTS_DIR, ERRORS_BUFFER_DIR


def test_app_integration(bash_shell, terminal_oi):
    notification = "This is standard input notification"
    with replace_stdin(notification):
        main(bash_shell, GOOD_SCRIPTS_DIR, terminal_oi, ERRORS_BUFFER_DIR)
