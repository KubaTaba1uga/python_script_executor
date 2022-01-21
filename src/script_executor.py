from src.output_input_controller import OutputInputController
from src.temporary_errors_buffer import TempErrorFile
from src.exceptions import NoPidError, NoExitCodeError
from src.script import Script
from src.shell import Shell


class ScriptExecutor:
    errors_buffer = TempErrorFile
    pid_tag = "pid="
    exit_code_tag = "exit_code="

    def __init__(
        self, script: Script, shell: Shell, oi_controller: OutputInputController
    ):
        if not isinstance(script, Script):
            raise TypeError("script has to be Script type")

        if not isinstance(shell, Shell):
            raise TypeError("shell has to subclass of Shell")

        if not isinstance(oi_controller, OutputInputController):
            raise TypeError("oi_controller has to be subclass of OutputInputController")

        self.script = script
        self.shell = shell
        self.oi_controller = oi_controller

    @classmethod
    def _create_pid_command(cls):
        command = "$$"
        return f"echo {cls.pid_tag}{command}"

    @classmethod
    def _is_pid(cls, output: str) -> bool:
        if "$$" in output:
            # Avoid recognizing execution command as pid
            return False
        return cls.pid_tag in output

    @classmethod
    def _extract_pid(cls, output: str) -> str:
        tag_end_index = output.find(cls.pid_tag) + len(cls.pid_tag)
        pid_end_index = output.find("\r\n")
        return output[tag_end_index:pid_end_index]

    @classmethod
    def _is_exit_code(cls, output: str) -> bool:
        if "$?" in output:
            # Avoid recognizing get last exit code command as
            #   exit code itself
            return False
        return cls.exit_code_tag in output

    @classmethod
    def _extract_exit_code(cls, output: str):
        tag_end_index = output.find(cls.exit_code_tag) + len(cls.exit_code_tag)
        exit_code_end_index = output.find("\r\n")
        return output[tag_end_index:exit_code_end_index]

    def _find_pid(self) -> int:
        for line in self.shell:
            if self._is_pid(line):
                return self._extract_pid(line)
        raise NoPidError(f"No exit code found for {self.script}")

    def _find_exit_code(self) -> int:
        for line in self.shell:
            if self._is_exit_code(line):
                return self._extract_exit_code(line)
        raise NoExitCodeError(f"No exit code found for {self.script}")

    def _get_last_exit_code(self):
        """Get exit code of last executed process"""
        command = "$?"
        self.shell.send_command(f"echo {self.exit_code_tag}{command}")
        return self._find_exit_code()

    def _create_execution_command(self) -> str:
        """Create command which will generate child process
        PID and execute command under that PID.

        Generated pid will be used to recognize process status
        like:
                terminated
                hang up
                suspend
        """

        shell_path, pid_command, interpreter_path, script_path, error_redirection = (
            self.shell.path,
            self._create_pid_command(),
            self.script.find_shebang_path(),
            self.script.path,
            self.errors_buffer.create_error_redirection(),
        )

        return (
            # Execute command by shell as string
            f"{shell_path} -c"
            # Create pid before execution
            + f' "{pid_command};'
            # Execute under the pid
            + f"exec {interpreter_path} {script_path}"
            # Redirect errors to temporary file
            + f'{error_redirection}"'
        )

    def execute_script(self):
        """Execute script as another process"""

        # self._spawn_shell(script)

        # while self.process.isalive():

        #     try:
        #         # Pass shell, to allow controll of process by
        #         #       output_input.stdout
        #         output_input.stdout = self, self._read_output(timeout)
        #     except NoOutputProduced as err:
        #         output_input.stdout = self, err.args[0]

        #     if _ErrorTempFile.errors_exist():
        #         # Pass shell, to allow controll of process by
        #         #       output_input.stderr
        #         output_input.stderr = self, _ErrorTempFile.read_errors()

        #     if Process.is_sleeping(self.process.pid):
        #         # Pass shell, to allow comunication with process by
        #         #       output_input.stdin
        #         output_input.stdin = self, None

        # if self.process.status == 0:
        #     output_input.print_success(script.name)
        # else:
        #     output_input.print_failure(script.name)


from tests.config import SCRIPTS_FOLDER
from src.shell import BashShell
from src.output_input_controller import TerminalOutputInput

script = Script("bash_output_1.sh", SCRIPTS_FOLDER)

shell = BashShell()

term_oi = TerminalOutputInput()

shell.spawn_shell()

executor = ScriptExecutor(script, shell, term_oi)

command = executor._create_execution_command()

shell.send_command(command)

pid = executor._find_pid()

exit_code = executor._get_last_exit_code()


print("command", command, end="\n" * 2)

print("pid", pid, end="\n" * 2)

print("exit_code", exit_code, end="\n" * 2)


# print(shell._read_output(script.name, 2))

shell.terminate()
