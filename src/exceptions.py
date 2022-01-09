from pexpect import ExceptionPexpect, TIMEOUT


class FileNotFoundOrNotExecutable(ExceptionPexpect):
    pass


class FileNotFound(FileExistsError):
    pass


class FileNotExecutable(PermissionError):
    pass


class TimeoutReached(TIMEOUT):
    pass


class NoOutputProduced(Exception):
    pass
