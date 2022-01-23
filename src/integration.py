from tests.config import SCRIPTS_FOLDER
from src.script import Script
from src.shell import BashShell
from src.output_input_controller import TerminalOutputInput
from src.script_executor import ScriptExecutor

script_0 = Script("bash_output_1.sh", SCRIPTS_FOLDER)

script_1 = Script("bash_error_4.sh", SCRIPTS_FOLDER)

script_2 = Script("python_error.py", SCRIPTS_FOLDER)

scripts = [script_0, script_1, script_2]

shell = BashShell()

term_oi = TerminalOutputInput()

shell.spawn_shell()

for script in scripts:
    executor = ScriptExecutor(script, shell, term_oi)

    executor.execute_script()

# command = executor._create_execution_command()

# shell.send_command(command)

# pid = executor.pid

# # # output = shell.read_output_all(script.name)

# exit_code = executor.exit_code

# print("command", command, end="\n" * 2)

# print("Shell pid", shell.process.pid, end="\n" * 2)

# print("Subshell pid", pid, end="\n" * 2)

# print("exit_code", exit_code, end="\n" * 2)

# # print("output:")
# # print(output)


shell.terminate()
