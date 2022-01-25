from subprocess import Popen
from pathlib import Path
import pytest

from src.output_input_controller import TerminalOutputInput
from src.temporary_errors_buffer import TempErrorFile
from src.script_executor import ScriptExecutor
from src.script import _ScriptName
from src.shell import BashShell
from src.module import Module
from src.script import Script

from tests.config import GOOD_SCRIPTS_DIR, BAD_SCRIPTS_DIR


SCRIPT_WITH_NUMBER_NAME = "my_script_0.sh"

SCRIPT_WITHOUT_NUMBER_NAME = "my_script.sh"


GOOD_SCRIPTS = {
    "shebang": {"name": "bash_shebang_0.sh", "shebang_path": "/bin/bash"},
    "output": {"name": "bash_output_1.sh"},
    "input": {"name": "bash_input_2.sh"},
    "error": {"name": "bash_error_4.sh"},
    "dir_path": GOOD_SCRIPTS_DIR,
}

BAD_SCRIPTS = {
    "no_shebang": {"name": "bash_no_shebang.sh", "shebang_path": ""},
    "create_file": {"name": "create_file.sh"},
    "dir_path": BAD_SCRIPTS_DIR,
}

BASH_SHELL_PATH = Path("/bin/bash")


@pytest.fixture
def bash_error_script():
    return Script(GOOD_SCRIPTS["error"]["name"], GOOD_SCRIPTS["dir_path"])


@pytest.fixture
def bash_output_script():
    return Script(GOOD_SCRIPTS["output"]["name"], GOOD_SCRIPTS["dir_path"])


@pytest.fixture
def bash_input_script():
    return Script(GOOD_SCRIPTS["input"]["name"], GOOD_SCRIPTS["dir_path"])


@pytest.fixture
def script_shebang():
    return Script(GOOD_SCRIPTS["shebang"]["name"], GOOD_SCRIPTS["dir_path"])


@pytest.fixture
def bash_shell():
    return BashShell()


@pytest.fixture
def popen_process():
    return Popen(args=["/usr/bin/sleep", "10"])


@pytest.fixture
def module():
    return Module(GOOD_SCRIPTS["dir_path"])


@pytest.fixture
def script_name_with_number():
    return _ScriptName(SCRIPT_WITH_NUMBER_NAME)


@pytest.fixture
def script_name_without_number():
    return _ScriptName(SCRIPT_WITHOUT_NUMBER_NAME)


@pytest.fixture
def bad_script():
    return Script(BAD_SCRIPTS["no_shebang"]["name"], BAD_SCRIPTS["dir_path"])


@pytest.fixture
def script_create_file():
    return Script(BAD_SCRIPTS["create_file"]["name"], BAD_SCRIPTS["dir_path"])


@pytest.fixture
def non_existing_path():
    path = "/xyz/cxz/zxc/xcz"
    return Path(path)


@pytest.fixture
def non_executable_path():
    path = "/bin"
    return Path(path)


@pytest.fixture
def terminal_oi():
    return TerminalOutputInput()


@pytest.fixture
def temp_err_buffer():
    path = Path("/tmp")
    return TempErrorFile(path)


@pytest.fixture
def script_executor(bash_shell, bash_output_script, terminal_oi, temp_err_buffer):
    bash_shell.spawn_shell(timeout=0.2)
    return ScriptExecutor(bash_output_script, bash_shell, terminal_oi, temp_err_buffer)
