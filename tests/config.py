from pathlib import Path
import sys
import os

GOOD_SCRIPTS_DIR = Path("./tests/scripts/good_scripts")

BAD_SCRIPTS_DIR = Path("./tests/scripts/bad_scripts")

ERRORS_BUFFER_DIR = Path("/tmp")


class replace_stdin:
    def __init__(self, input_string):
        file_name = "input_simulation"
        self.file_path = ERRORS_BUFFER_DIR.joinpath(file_name)
        self.input_string = input_string

    def __enter__(self):
        # sys.stdin has to be file because select
        #   in script executor need fileno method
        #   to create event loop

        self.org_stdin = sys.stdin

        with open(self.file_path, "w") as f:
            f.write(self.input_string)

        f = open(self.file_path)

        sys.stdin = f

        return self

    def __exit__(self, _exc_type, _exc_value, _exc_tryceback):

        sys.stdin.close()

        sys.stdin = self.org_stdin

        os.remove(self.file_path)
