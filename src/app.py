import os
import pathlib

SCRIPTS_FOLDER = pathlib.Path("./scripts/").absolute()


class Module:
    """Collection of scripts"""

    def __init__(self, scripts_folder: pathlib.Path = SCRIPTS_FOLDER):
        self.scripts_folder = scripts_folder

    def __iter__(self):
        scripts = os.listdir(self.scripts_folder)

        scripts_list = []

        for script in scripts:
            script_name = ScriptName(script)
            script = Script(script_name)
            script_number = script_name.find_script_number()

            scripts_list.append(
                (
                    script_number,
                    script,
                )
            )

        scripts_list.sort(key=self.get_first_element)

        return (script[1] for script in scripts_list)

    @classmethod
    def get_first_element(cls, collection):
        """Get first element of collection"""
        return collection[0]


if __name__ == "__main__":
    pass
