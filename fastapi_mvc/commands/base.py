"""Command design pattern - abstract base class."""
from abc import ABCMeta, abstractmethod
import logging


class Command(object, metaclass=ABCMeta):
    """Define the common interface for all concrete commands.

    Attributes:
        _log (logging.Logger): Logger class object instance.

    """

    __slots__ = "_log"

    def __init__(self):
        """Initialize Command class object instance."""
        self._log = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def execute(self):
        """Define abstract execute method for all inheriting classes."""
        pass
