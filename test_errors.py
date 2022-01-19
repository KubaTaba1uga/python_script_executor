from pathlib import Path
from src.shell import Shell

from src.script import Script

from src.output_input_controller import TerminalOutputInput

from tests.config import SCRIPTS_FOLDER


script = Script("bash_error_4.sh", SCRIPTS_FOLDER)

oi = TerminalOutputInput()

shell = Shell(Path("/bin/bash"))
