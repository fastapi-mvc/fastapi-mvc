"""Command design pattern - Invoker class."""
import logging
from collections import deque

from fastapi_mvc.commands import Command


class Invoker(object):
    """Define the common interface for executing associated commands.

    Attributes:
        _log (logging.Logger): Logger class object instance.
        _queue (collections.deque): Invoker double ended queue with commands to
            execute.

    """

    __slots__ = (
        "_log",
        "_queue",
    )

    def __init__(self):
        """Initialize Invoker class object instance."""
        self._log = logging.getLogger(self.__class__.__name__)
        self._log.debug("Initialize Invoker class object instance.")
        self._queue = deque()

    def enqueue(self, command):
        """Enqueue command to execute.

        Args:
            command (Command): Command class object instance.

        """
        if isinstance(command, Command):
            self._queue.append(command)
        else:
            self._log.warning("You can only enqueue Command subclasses.")

    def execute(self):
        """Execute enqueued Invoker commands."""
        while self._queue:
            command = self._queue.popleft()
            command.execute()
