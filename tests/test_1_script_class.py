import pytest

from src.script import Script
from src.exceptions import NoShebangError, FileNotFound
from tests.fixtures import non_existing_path, script, bad_script, GOOD_SCRIPT


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
