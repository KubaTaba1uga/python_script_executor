from src.output_input_controller import OutputInputController
from src.temporary_errors_buffer import TempErrorFile
from src.exceptions import NoPidError, NoExitCodeError, NoOutputProduced
from src.process import Process
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
        command = "$BASHPID"
        return f"echo {cls.pid_tag}{command}"

    @classmethod
    def _is_pid(cls, output: str) -> bool:
        if "$BASHPID" in output:
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
        raise NoPidError(f"No pid found for {self.script}")

    def _find_exit_code(self) -> int:
        for line in self.shell:
            if self._is_exit_code(line):
                return self._extract_exit_code(line)
        raise NoExitCodeError(f"No exit code found for {self.script}")

    @property
    def pid(self) -> int:
        return int(self._find_pid())

    @property
    def exit_code(self) -> int:
        """Get exit code of last executed process"""
        command = "$?"
        self.shell.send_command(f"echo {self.exit_code_tag}{command}")
        return int(self._find_exit_code())

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
            self._create_pid_command(),
            self.script.find_shebang_path(),
            self.script.path,
            self.errors_buffer.create_error_redirection(),
        )

        return (
            # Subshell char start
            "("
            # Create pid before execution
            + f"{pid_command} && "
            # Execute under the pid
            + f"exec {interpreter_path} {script_path}"
            # Redirect errors to temporary file
            + f"{error_redirection}"
            # Subshell char end
            + ")"
            # Disable user settings to get clean output
            # + " --norc"
        )

    def get_output(self):
        try:
            output = self.shell, self.shell.read_output_all(self.script)
        except NoOutputProduced as err:
            output = self.shell, err.args[0]
        self.oi_controller.stdout = output

    def execute_script(self):
        """Execute script as another process"""
        if not self.shell.process:
            self.shell.spawn_shell()

        command = self._create_execution_command()

        self.shell.send_command(command)

        pid = self.pid

        while Process.is_alive(pid):
            # self.get_output()
            print(pid, "\n")
            print(self.shell.process.pid)
            from time import sleep

            sleep(100)
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

executor.execute_script()

command = executor._create_execution_command()

# shell.send_command(command)

# pid = executor.pid

# output = shell.read_output_all(script.name)

# exit_code = executor.exit_code


print("command", command, end="\n" * 2)

# print("pid", pid, end="\n" * 2)

# print("exit_code", exit_code, end="\n" * 2)

# print("output:")
# print(output)


shell.terminate()
