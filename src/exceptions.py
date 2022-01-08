from pexpect import ExceptionPexpect, TIMEOUT


class FileNotFoundOrNotExecutable(ExceptionPexpect):
    pass


class FileNotFound(FileExistsError):
    pass


class FileNotExecutable(PermissionError):
    pass


class NoOutputProduced(TIMEOUT):
    """If timeout is reached there are no more output from the commend"""

    pass
