from subprocess import Popen
from time import sleep

from tests.fixtures import popen_process

from src.process import Process


def test_is_alive(popen_process):
    assert Process.is_alive(popen_process.pid) is True


def test_is_sleeping(popen_process):
    assert Process.is_sleeping(popen_process.pid) is True


def test_kill(popen_process):
    Process.kill(popen_process.pid)
    sleep(0.3)
    popen_process.poll()
    assert Process.is_alive(popen_process.pid) is False