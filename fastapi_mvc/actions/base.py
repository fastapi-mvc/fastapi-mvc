""""""
from abc import ABCMeta, abstractmethod
import logging


class Action(object, metaclass=ABCMeta):

    def __init__(self):
        self._log = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def execute(self, *args, **kwargs):
        pass
