from contextlib import contextmanager
from pathlib import Path
from io import StringIO
import sys

GOOD_SCRIPTS_DIR = Path("./tests/scripts/good_scripts")

BAD_SCRIPTS_DIR = Path("./tests/scripts/bad_scripts")

ERRORS_BUFFER_DIR = Path("/tmp")


@contextmanager
def replace_stdin(input_string):
    org_stdin = sys.stdin
    sys.stdin = StringIO(input_string)
    yield None
    sys.stdin = org_stdin
