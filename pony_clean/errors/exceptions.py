class PonyError(Exception):
    pass

class PonyAPIError(PonyError):
    pass

class PonyServError(PonyError):
    pass

class PonyConfigError(PonyError):
    pass

class PonyValidationError(PonyError):
    pass

class PonyInfraError(PonyError):
    pass