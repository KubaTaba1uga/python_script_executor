from contextlib import contextmanager
from pathlib import Path
from io import StringIO
import sys


GOOD_SCRIPTS_DIR = Path("./tests/scripts/good_scripts")

BAD_SCRIPTS_DIR = Path("./tests/scripts/bad_scripts")

ERRORS_BUFFER_DIR = Path("/tmp")

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


@contextmanager
def replace_stdin(notification):
    org_stdin = sys.stdin
    sys.stdin = StringIO(notification)
    yield None
    sys.stdin = org_stdin
