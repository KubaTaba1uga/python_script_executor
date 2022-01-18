from pathlib import Path
import pytest

from src.output_input_controller import TerminalOutputInput
from src.script import _ScriptName
from src.module import Module
from src.script import Script
from src.shell import Shell
from tests.config import SCRIPTS_FOLDER


SCRIPT_WITH_NUMBER_NAME = "my_script_0.sh"

SCRIPT_WITHOUT_NUMBER_NAME = "my_script.sh"


GOOD_SCRIPT = {"name": "bash_shebang_0.sh", "shebang_path": "/bin/bash"}

BAD_SCRIPT = {"name": "bash_no_shebang.sh", "shebang_path": ""}


OUTPUT_SCRIPT = {"name": "bash_output_1.sh"}

INPUT_SCRIPT = {"name": "bash_input_2.sh"}

BASH_SHELL_PATH = Path("/bin/bash")


@pytest.fixture
def bash_output_script():
    return Script(OUTPUT_SCRIPT["name"], SCRIPTS_FOLDER)


@pytest.fixture
def bash_input_script():
    return Script(INPUT_SCRIPT["name"], SCRIPTS_FOLDER)


@pytest.fixture
def bash_shell():
    return Shell(BASH_SHELL_PATH)


@pytest.fixture
def module():
    return Module()


@pytest.fixture
def script_name_with_number():
    return _ScriptName(SCRIPT_WITH_NUMBER_NAME)


@pytest.fixture
def script_name_without_number():
    return _ScriptName(SCRIPT_WITHOUT_NUMBER_NAME)


@pytest.fixture
def script():
    return Script(GOOD_SCRIPT["name"], SCRIPTS_FOLDER)


@pytest.fixture
def bad_script():
    return Script(BAD_SCRIPT["name"], SCRIPTS_FOLDER)


@pytest.fixture
def non_existing_path():
    path = "/xyz/cxz/zxc/xcz"
    return Path(path)


@pytest.fixture
def non_executable_path():
    path = "/bin"
    return Path(path)


@pytest.fixture
def shell():
    shell_path = Path("/bin/bash")
    return Shell(shell_path)


@pytest.fixture
def terminal_oi():
    return TerminalOutputInput()
