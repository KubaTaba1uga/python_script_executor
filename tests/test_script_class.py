import pytest

from src.script import Script

SCRIPT_NAME = "update_apt-get_1.sh"


@pytest.fixture
def script():
    return Script(SCRIPT_NAME)


def test_script_iteration(script):
    with open(script.path) as script_file:
        for line in script:
            assert line == script_file.readline()
