import pytest

from tests.fixtures import script_name_with_number, script_name_without_number


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
