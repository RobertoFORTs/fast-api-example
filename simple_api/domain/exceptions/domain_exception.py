class DomainException(Exception):

    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class NotFoundException(DomainException):
    def __init__(self, message="Resource not found"):
        super().__init__(message, status_code=404)


class ValidationException(DomainException):
    def __init__(self, message="Validation error"):
        super().__init__(message, status_code=400)


class ConflictException(DomainException):
    def __init__(self, message="Conflict error"):
        super().__init__(message, status_code=409)
