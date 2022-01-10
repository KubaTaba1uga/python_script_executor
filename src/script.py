import os
import pathlib

from src.app import SCRIPTS_FOLDER
from src.exceptions import FileNotFound


class ScriptName:
    """Name of the script, wich is needed
    to organize scripts order"""

    def __init__(self, name: str):
        self.name = name

    def _find_last_underscore(self):
        return len(self.name) - self.name[::-1].find("_")

    def _find_last_dot(self):
        return len(self.name) - self.name[::-1].find(".") - 1

    def find_script_number(self) -> str:
        """Find number of the script in its name.
        If script is not numbered return empty string."""

        script_number = self.name[self._find_last_underscore() : self._find_last_dot()]

        if script_number.isdigit():
            return script_number

        return ""

    def is_script_numbered(self):
        return bool(self.find_script_number())

    def __str__(self):
        return self.name


"""
TO-DO
1. script.have_sheabang()
2. script.find_sheabang()
"""


class Script:
    """Script which know how to read itself"""

    SHEABANG = "#!"

    def __init__(self, name: str, folder_path: pathlib.Path = SCRIPTS_FOLDER):
        self.name = ScriptName(name)
        self.path = os.path.join(folder_path, pathlib.Path(str(name)))

        if not self.path.exists():
            raise FileNotFound(f"{self.path} not found")

    def __iter__(self):
        """Create generator to yield script lines"""

        with open(self.path, "r") as script_file:

            while script_line := script_file.readline():

                yield script_line

    def __str__(self):
        return str(self.name)

    def find_sheabang(self):
        """Iterate over script to find #!<executable path>
        Sheabang example:
                #!/bin/bash
        """
        for line in self:
            if self.SHEABANG in line:
                return line[line.find(self.SHEABANG) + len(self.SHEABANG) :]
        return ""

    @classmethod
    def is_sheabang(cls, line: str):
        return
