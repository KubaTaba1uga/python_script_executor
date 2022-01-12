import pytest

from src.script import Script
from src.exceptions import NoSheabangError
from tests.config import SCRIPTS_FOLDER

GOOD_SCRIPT = {"name": "bash_sheabang_0.sh", "sheabang_path": "/bin/bash"}

BAD_SCRIPT = {"name": "bash_no_sheabang.sh", "sheabang_path": ""}


@pytest.fixture
def script():
    return Script(GOOD_SCRIPT["name"], SCRIPTS_FOLDER)


@pytest.fixture
def bad_script():
    return Script(BAD_SCRIPT["name"], SCRIPTS_FOLDER)


def test_script_iteration(script):
    """Check is object iterable"""
    with open(script.path) as script_file:
        for line in script:
            assert line == script_file.readline()


def test_script_find_sheabang_path(script):
    assert script.find_sheabang_path() == GOOD_SCRIPT["sheabang_path"]


def test_script_cant_find_sheabang_path(bad_script):
    with pytest.raises(NoSheabangError):
        bad_script.find_sheabang_path()
