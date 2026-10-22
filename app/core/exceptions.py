class AppError(Exception):
    status_code = 400

    def __init__(self, detail: str):
        self.detail = detail

class NotFoundError(AppError):
    status_code = 404

class AuthError(AppError):
    status_code = 401