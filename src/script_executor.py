from src.output_input_controller import OutputInputController
from src.temporary_errors_buffer import TempErrorFile
from src.exceptions import NoPidError, NoExitCodeError, NoOutputProduced
from src.process import Process
from src.script import Script
from src.shell import SubShell


class ScriptExecutor:
    errors_buffer = TempErrorFile()
    pid_tag = "pid="
    exit_code_tag = "exit_code="

    def __init__(
        self, script: Script, shell: SubShell, oi_controller: OutputInputController
    ):
        if not isinstance(script, Script):
            raise TypeError("script has to be Script type")

        if not isinstance(shell, SubShell):
            raise TypeError("shell has to subclass of SubShell")

        if not isinstance(oi_controller, OutputInputController):
            raise TypeError("oi_controller has to be subclass of OutputInputController")

        self.script = script
        self.shell = shell
        self.oi_controller = oi_controller

    @property
    def pid(self) -> int:
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
            "("
            # Create pid before execution
            + f"{pid_command} && "
            # Execute under the pid
            + f"exec {interpreter_path} "
            # Script which will be executed
            + f"{script_path}"
            # Redirect errors to temporary file
            + f"{error_redirection}"
            # SubShell char end
            + ")"
        )

    def get_output(self, subshell_pid):
        try:
            output = self.shell, self.shell.read_output_all(self.script)
        except NoOutputProduced as err:
            output = self.shell, err.args[0]
        self.oi_controller.stdout = output

    def get_errors(self, subshell_pid):
        if self.errors_buffer.exist():
            self.oi_controller.stderr = self.shell, self.errors_buffer.read()

    def get_input(self, subshell_pid):
        if Process.is_sleeping(subshell_pid):
            self.oi_controller.stdin = self.shell, None

    def execute_script(self):
        """Execute script as another process"""
        if not self.shell.process:
            self.shell.spawn_shell()

        command = self._create_execution_command()

        self.shell.send_command(command)

        pid = self.pid

        while Process.is_alive(pid):
            self.get_output(pid)
            self.get_errors(pid)
            self.get_input(pid)

        if self.exit_code == 0:
            self.oi_controller.print_success(self.script)
        else:
            self.oi_controller.print_failure(self.script)


from tests.config import SCRIPTS_FOLDER
from src.shell import BashShell
from src.output_input_controller import TerminalOutputInput

script = Script("bash_output_1.sh", SCRIPTS_FOLDER)

script = Script("bash_error_4.sh", SCRIPTS_FOLDER)

shell = BashShell()

term_oi = TerminalOutputInput()

shell.spawn_shell()

executor = ScriptExecutor(script, shell, term_oi)

executor.execute_script()

command = executor._create_execution_command()

# shell.send_command(command)

# pid = executor.pid

# # # output = shell.read_output_all(script.name)

# exit_code = executor.exit_code


print("command", command, end="\n" * 2)

# print("Shell pid", shell.process.pid, end="\n" * 2)

# print("Subshell pid", pid, end="\n" * 2)

# print("exit_code", exit_code, end="\n" * 2)

# # print("output:")
# # print(output)


shell.terminate()
