from pathlib import Path

from src.shell import SubShell
from src.module import Module
from src.script_executor import ScriptExecutor
from src.temporary_errors_buffer import TempErrorFile
from src.output_input_controller import OutputInputController


def main(
    shell: SubShell,
    script_folder_path: Path,
    oi_controller: OutputInputController,
    errors_buffer_path: Path,
):

    errors_buffer = TempErrorFile(errors_buffer_path)

    with shell as sh:
        for script in Module(script_folder_path):

            sc_ex = ScriptExecutor(script, sh, oi_controller, errors_buffer)

            sc_ex.execute_script()
