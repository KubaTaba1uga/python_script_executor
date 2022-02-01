from src.output_input_controllers.base import OutputInputController

from tests.config import replace_stdin


def test_terminal_output(bash_shell):
    for subclass in OutputInputController.__subclasses__():
        terminal_oi = subclass()
        with bash_shell as shell:
            output_notification = "This is standard output notification"
            terminal_oi.stdout = shell, output_notification
            assert terminal_oi.stdout == output_notification


def test_terminal_error(bash_shell):
    for subclass in OutputInputController.__subclasses__():
        terminal_oi = subclass()
        with bash_shell as shell:
            error_notification = "This is standard error notification"
            terminal_oi.stderr = shell, error_notification
            assert terminal_oi.stderr == error_notification


def test_terminal_input(bash_shell):
    input_notification = "This is standard input"
    for subclass in OutputInputController.__subclasses__():
        terminal_oi = subclass()
        with bash_shell as shell:
            with replace_stdin(input_notification):
                shell.shell = shell
                terminal_oi.stdin = shell, None
                assert terminal_oi.stdin == input_notification
                # Prettify pytest -s formatting
                print(terminal_oi.stdin)


def test_command_line_flags():
    """Ensure each OIController subclass has
    command line flag implemented properly"""
    for cls in OutputInputController.__subclasses__():
        assert cls.command_line_argument is not None
