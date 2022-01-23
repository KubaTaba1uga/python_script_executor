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


class NoShebangError(Exception):
    """Error is caused by absence of shebang inside a script.
    What is shebang??
            Shebang is interpreter directive with syntax:
                    #! <interpreter path> [optional-arg]
    """


class NoPidError(Exception):
    """No pid were generated before process execution"""


class NoExitCodeError(Exception):
    """No exit code were produced by process"""
