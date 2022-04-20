"""FastAPI MVC custom exceptions implementation"""


class RootException(Exception):

    code = 1

    def __init__(self, message):
        Exception.__init__(self, message)
        self.message = message

    def __str__(self):
        return self.message


class FileError(RootException):
    """Custom fastapi-mvc FileError exception class definition."""

    pass
