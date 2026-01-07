class ARateError(Exception): ...

class ApiError(ARateError):
    def __init__(self, status: int | None, message: str, payload=None, retryable: bool = False):
        self.status = status
        self.payload = payload
        self.retryable = retryable
        super().__init__(message)

class CurrencyAPIError(ARateError):
    pass

class APIClientError(ARateError):
    pass

class RatesUnavailableError(ARateError):
    pass