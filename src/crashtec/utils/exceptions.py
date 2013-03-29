

class CtBaseException(RuntimeError):
    pass

class CtGeneralError(CtBaseException):
    pass

class CtCriticalError(CtBaseException):
    pass