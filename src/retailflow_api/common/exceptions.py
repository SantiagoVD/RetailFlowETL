"""Client-safe API exceptions."""


class ApiError(Exception):
    def __init__(self, message: str, status_code: int = 400, code: str = "BAD_REQUEST") -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.code = code


class NotFoundError(ApiError):
    def __init__(self, message: str = "Recurso no encontrado") -> None:
        super().__init__(message, 404, "NOT_FOUND")
