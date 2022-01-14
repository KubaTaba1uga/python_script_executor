import os

import pytest

from src.app import SCRIPTS_FOLDER
from src.script import Script
from src.module import Module


@pytest.fixture
def module():
    return Module()


def test_sorted_scripts(module):
    script_list = module.list_sorted_scripts()
    for i, script in enumerate(module):
        assert script.name.find_script_number() == script_list[i][0]
