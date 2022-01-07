import pytest
from src.script import ScriptName

SCRIPT_WITH_NUMBER_NAME = "my_script_0.sh"

SCRIPT_WITHOUT_NUMBER_NAME = "my_script.sh"


@pytest.fixture
def script_name_with_number():
    return ScriptName(SCRIPT_WITH_NUMBER_NAME)


@pytest.fixture
def script_name_without_number():
    return ScriptName(SCRIPT_WITHOUT_NUMBER_NAME)


def test_find_last_underscore(script_name_with_number):
    assert script_name_with_number._find_last_underscore() == 10


def test_find_last_dot(script_name_with_number):
    assert script_name_with_number._find_last_dot() == 11


def test_find_script_number(script_name_with_number, script_name_without_number):
    assert script_name_with_number.find_script_number() == "0"
    assert script_name_without_number.find_script_number() == ""


def test_is_script_numbered(script_name_with_number, script_name_without_number):
    assert script_name_with_number.is_script_numbered() is True
    assert script_name_without_number.is_script_numbered() is False
