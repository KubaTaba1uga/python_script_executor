import pytest
from src.script import _ScriptName

SCRIPT_WITH_NUMBER_NAME = "my_script_0.sh"

SCRIPT_WITHOUT_NUMBER_NAME = "my_script.sh"


@pytest.fixture
def script():
    return _ScriptName(SCRIPT_WITH_NUMBER_NAME)


@pytest.fixture
def script_name_without_number():
    return _ScriptName(SCRIPT_WITHOUT_NUMBER_NAME)


def test_find_last_underscore(script):
    assert script._find_last_underscore() == 10


def test_find_last_dot(script):
    assert script._find_last_dot() == 11


def test_find_script_number(script, script_name_without_number):
    assert script.find_script_number() == "0"
    assert script_name_without_number.find_script_number() == ""


def test_is_script_numbered(script, script_name_without_number):
    assert script.is_script_numbered() is True
    assert script_name_without_number.is_script_numbered() is False
