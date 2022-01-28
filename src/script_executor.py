from threading import Thread
from select import select
from time import sleep
import sys

from src.exceptions import NoOutputProduced, ShellNotSpawned
from src.output_input_controller import OutputInputController
from src.temporary_errors_buffer import TempErrorFile
from src.process import Process
from src.script import Script
from src.shell import SubShell


class ScriptExecutor:
    def __init__(
        self,
        script: Script,
        shell: SubShell,
        oi_controller: OutputInputController,
        errors_buffer: TempErrorFile,
    ):
        if not isinstance(script, Script):
            raise TypeError("script has to be Script type")

        if not isinstance(shell, SubShell):
            raise TypeError("shell has to subclass of SubShell")

        if not isinstance(oi_controller, OutputInputController):
            raise TypeError("oi_controller has to be subclass of OutputInputController")

        if not shell.process:
            raise ShellNotSpawned(f"Passed not spawned shell for {script} execution")

        self.script = script
        self.shell = shell
        self.oi_controller = oi_controller
        self.errors_buffer = errors_buffer

    @property
    def pid(self) -> int:
        """Get PID of script in shell output"""
        return self.shell.find_subshell_pid()

    @property
    def exit_code(self) -> int:
        """Get exit code of last executed process"""
        return self.shell.get_subshell_exit_code()

    def _create_execution_command(self) -> str:
        """Create subshell and return its PID. Script
        will be executed within a subshell by command
        syntax.
        Because of subshell child PID will be different
        than parent shell PID.

        Generated PID will be used to recognize process status
        like:
                terminated
                hang up
                suspend
        """

        pid_command, interpreter_path, script_path, error_redirection = (
            self.shell.create_subshell_pid_command(),
            self.script.find_shebang_path(),
            self.script.path,
            self.errors_buffer.create_error_redirection(),
        )

        return (
            # SubShell char start
            self.shell.subshell["start"]
            # Create pid before execution
            + f"{pid_command} && "
            # Execute under the pid
            + f"exec {interpreter_path} "
            # Script which will be executed
            + f"{script_path}"
            # Redirect errors to temporary file
            + f"{error_redirection}"
            # SubShell char end
            + self.shell.subshell["end"]
        )

    def get_output(self, subshell_pid: int, stop):
        """Get output from shell and pass it to
        output input controller"""
        while stop():
            output = self.shell.read_output_line()
            self.oi_controller.stdout = self.shell, output, subshell_pid  # type:ignore

    def get_errors(self, subshell_pid: int, stop):
        """Get errors from errors temporary file
        and pass it to output input controller"""
        while stop():
            if self.errors_buffer.exist():
                self.oi_controller.stderr = (  # type:ignore
                    self.shell,
                    self.errors_buffer.read(),
                    subshell_pid,
                )

    def get_input(self, subshell_pid: int, stop):
        """Get input from user and pass it to shell"""
        while stop():
            # Create event loop, which will expire after 1s
            #   it is needed for case when input is blocking
            #   execution but is not required by script
            readers, _, _ = select([sys.stdin], [], [], 1)
            for reader in readers:
                self.oi_controller.stdin = (
                    self.shell,
                    "",
                    subshell_pid,
                )

    def execute_script(self):
        """Execute script as separeted process"""

        command = self._create_execution_command()

        threads_alive = True

        self.shell.send_command(command)

        pid = self.pid

        with self.errors_buffer:
            Thread(target=self.get_output, args=[pid, lambda: threads_alive]).start()
            Thread(target=self.get_input, args=[pid, lambda: threads_alive]).start()
            Thread(target=self.get_errors, args=[pid, lambda: threads_alive]).start()

            while Process.is_alive(pid) and not self.oi_controller.continue_flag:
                pass
            else:
                # Wait for all output to be gatherd
                sleep(1)
                # Kill threads
                threads_alive = False

            if not self.oi_controller.continue_flag:
                self.oi_controller.show_status(self.script, self.exit_code)
