"""FastAPI MVC RunUvicorn command class implementation.

The fastapi-mvc.commands submodule implements command design pattern:
https://refactoring.guru/design-patterns/command
"""
import os

from fastapi_mvc.commands import Command
from fastapi_mvc.utils import ShellUtils
from fastapi_mvc.parsers import IniParser


class RunUvicorn(Command):
    """"""
    __slots__ = (
        "_cmd"
    )

    def __init__(self, host, port):
        """"""
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
        """"""
        ShellUtils.run_shell(self._cmd)
