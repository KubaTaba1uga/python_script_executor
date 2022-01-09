from psutil import Process as PsutilProcess
from psutil import NoSuchProcess


class Process(PsutilProcess):
    @classmethod
    def is_alive(cls, pid: int):
        is_alive = True
        try:
            cls(pid)
        except NoSuchProcess:
            is_alive = False
        return is_alive

    @classmethod
    def is_sleeping(cls, pid: int):
        if cls.is_alive(pid):
            return cls(pid).status() == "sleeping"
        return False
