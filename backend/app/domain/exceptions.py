class DomainError(Exception):
    def __init__(self, message: str, code: str = "domain_error"):
        self.message = message
        self.code = code
        super().__init__(message)


class NotFoundError(DomainError):
    def __init__(self, message: str = "Not found"):
        super().__init__(message, "not_found")


class ConflictError(DomainError):
    def __init__(self, message: str = "Conflict"):
        super().__init__(message, "conflict")


class UnauthorizedError(DomainError):
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message, "unauthorized")


class ForbiddenError(DomainError):
    def __init__(self, message: str = "Forbidden"):
        super().__init__(message, "forbidden")


class InsufficientFundsError(DomainError):
    def __init__(self, message: str = "Insufficient coins"):
        super().__init__(message, "insufficient_funds")


class ValidationError(DomainError):
    def __init__(self, message: str = "Validation failed"):
        super().__init__(message, "validation_error")
