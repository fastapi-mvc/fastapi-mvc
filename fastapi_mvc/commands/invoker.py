"""FastAPI MVC Invoker class implementation.

The fastapi-mvc.commands submodule implements command design pattern:
https://refactoring.guru/design-patterns/command
"""
import logging

from fastapi_mvc.commands import Command


class Invoker(object):
    """Defines the common interface for executing associated commands."""

    __slots__ = (
        "_log",
        "_on_start",
        "_on_finish",
    )

    def __init__(self):
        """Initialize Invoker class object instance."""
        self._log = logging.getLogger(self.__class__.__name__)
        self._log.debug("Initialize Invoker class object instance.")
        self._on_start = None
        self._on_finish = None

    @property
    def on_start(self):
        """Class on_start property.

        Returns:
            A Command object instance.


        """
        return self._on_start

    @on_start.setter
    def on_start(self, value):
        """Class on_start setter.

        Args:
            value(Command): A Command object instance.

        """
        self._on_start = value

    @property
    def on_finish(self):
        """Class on_finish property.

        Returns:
            A Command object instance.

        """
        return self._on_finish

    @on_finish.setter
    def on_finish(self, value):
        """Class on_finish setter.

        Args:
            value(Command): A Command object instance.

        """
        self._on_finish = value

    def execute(self):
        """Execute associated Invoker commands."""
        if isinstance(self._on_start, Command):
            self._log.debug("Execute Invoker on_start command.")
            self._on_start.execute()

        if isinstance(self._on_finish, Command):
            self._log.debug("Execute Invoker on_finish command.")
            self._on_finish.execute()
