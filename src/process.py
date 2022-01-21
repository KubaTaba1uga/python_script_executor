import psutil


class Process(psutil.Process):
    @classmethod
    def is_alive(cls, pid: int):
        return psutil.pid_exists(pid)

    @classmethod
    def is_sleeping(cls, pid: int):
        if cls.is_alive(pid):
            return cls(pid).status() == "sleeping"
        return False

    def terminate(cls, pid: int):
        if cls.is_alive(pid):
            cls(pid).terminate()
