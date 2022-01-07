import os
import pathlib

from src.app import SCRIPTS_FOLDER
from src.script import Script


class Module:
    """Collection of scripts"""

    def __init__(self, scripts_folder: pathlib.Path = SCRIPTS_FOLDER):
        self.scripts_folder = scripts_folder

    def __iter__(self):
        return (script[1] for script in self.list_sorted_scripts())

    def _list_scripts(self):
        return [Script(script) for script in os.listdir(self.scripts_folder)]

    def list_sorted_scripts(self):
        scripts_list = self._list_scripts()

        for i, script in enumerate(scripts_list):

            scripts_list[i] = (
                script.name.find_script_number(),
                script,
            )

        scripts_list.sort(key=self.get_first_element)

        return scripts_list

    @classmethod
    def get_first_element(cls, collection):
        """Get first element of collection"""
        return collection[0]
