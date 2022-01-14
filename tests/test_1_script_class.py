import pytest

from src.script import Script
from src.exceptions import NoShebangError, FileNotFound
from tests.config import SCRIPTS_FOLDER
from tests.fixtures import non_existing_path

GOOD_SCRIPT = {"name": "bash_shebang_0.sh", "shebang_path": "/bin/bash"}

BAD_SCRIPT = {"name": "bash_no_shebang.sh", "shebang_path": ""}


@pytest.fixture
def script():
    return Script(GOOD_SCRIPT["name"], SCRIPTS_FOLDER)


@pytest.fixture
def bad_script():
    return Script(BAD_SCRIPT["name"], SCRIPTS_FOLDER)


def test_script__init__error(non_existing_path):
    with pytest.raises(FileNotFound):
        Script(GOOD_SCRIPT["name"], non_existing_path)


def test_script_iteration(script):
    """Check is object iterable"""
    with open(script.path) as script_file:
        for line in script:
            assert line == script_file.readline()


def test_script_find_shebang_path(script):
    assert script.find_shebang_path() == GOOD_SCRIPT["shebang_path"]


def test_script_cant_find_shebang_path(bad_script):
    with pytest.raises(NoShebangError):
        bad_script.find_shebang_path()
