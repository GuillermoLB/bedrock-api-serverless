from .codes import Errors, Warnings


class CustomException(Exception):
    def __init__(self, error: Errors | Warnings, code: int):
        self.error = error
        self.code = code

    def __str__(self):
        return self.error


# change for more general classes like validationerror
class UserException(CustomException):

    """
    All User' related exceptions with specific error codes
    """
    # TODO: add  status code


class AuthenticationException(CustomException):

    """
    All User' related exceptions with specific error codes
    """
