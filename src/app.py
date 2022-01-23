from pathlib import Path

from src.shell import SubShell
from src.module import Module
from src.script_executor import ScriptExecutor
from src.output_input_controller import OutputInputController


def main(shell: SubShell, script_folder: Path, oi_controller: OutputInputController):
    with shell as sh:
        for script in Module(script_folder):
            ScriptExecutor(script, sh, oi_controller).execute_script()
