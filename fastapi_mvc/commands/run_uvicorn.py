"""FastAPI MVC RunUvicorn command class implementation.

The fastapi-mvc.commands submodule implements command design pattern:
https://refactoring.guru/design-patterns/command
"""
import os

from fastapi_mvc.commands import Command
from fastapi_mvc.utils import ShellUtils
from fastapi_mvc.parsers import IniParser


class RunUvicorn(Command):
    """Command RunUvicorn class definition."""

    __slots__ = (
        "_cmd"
    )

    def __init__(self, host, port):
        """Initialize RunUvicorn class object instance.

        Args:
            host(str): Host to bind uvicorn server to.
            port(port): Port to bind uvicorn server to.

        """
        Command.__init__(self)
        self._log.debug(
            "Initialize RunUvicorn class object instance."
        )
        parser = IniParser(os.getcwd())
        self._cmd = [
            "poetry",
            "run",
            "uvicorn",
            "--host",
            host,
            "--port",
            port,
            "--reload",
            "{0:s}.app.asgi:application".format(parser.package_name),
        ]

    def execute(self):
        """Run uvicorn development server for fastapi-mvc project."""
        ShellUtils.run_shell(self._cmd)
