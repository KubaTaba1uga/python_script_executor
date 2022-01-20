from psutil import Process as PsutilProcess
from psutil import NoSuchProcess


class Process(PsutilProcess):
    @classmethod
    def is_alive(cls, pid: int):
        return cls.pid_exists(pid)

    @classmethod
    def is_sleeping(cls, pid: int):
        if cls.is_alive(pid):
            return cls(pid).status() == "sleeping"
        return False

    def terminate(cls, pid: int):
        if cls.is_alive(pid):
            cls(pid).terminate()
