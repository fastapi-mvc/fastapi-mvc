"""FastAPI MVC custom exceptions."""


class RootException(Exception):
    """FastAPI MVC root exception for all inheriting concrete exceptions.

    Args:
        message (str): Reason for the exception.

    Attributes:
        code (int): (class attribute) The exit status of this exception.
        message (str): The error message that is passed to the constructor.

    """

    code = 1

    def __init__(self, message):
        """Initialize RootException class object instance."""
        Exception.__init__(self, message)
        self.message = message

    def __str__(self):
        """Class custom __str__ method implementation."""
        return self.message


class FileError(RootException):
    """Custom fastapi-mvc FileError exception class definition."""

    pass
