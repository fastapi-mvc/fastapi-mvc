"""FastAPI MVC RunUvicorn command class implementation.

The fastapi-mvc.commands submodule implements command design pattern:
https://refactoring.guru/design-patterns/command
"""
from fastapi_mvc.commands import Command
from fastapi_mvc.utils import ShellUtils


class RunUvicorn(Command):
    """Command RunUvicorn class definition."""

    __slots__ = "_cmd"

    def __init__(self, host, port, package_name):
        """Initialize RunUvicorn class object instance.

        Args:
            host(str): Host to bind uvicorn server to.
            port(port): Port to bind uvicorn server to.
            package_name(str): A fastapi-mvc generated project package name.

        """
        Command.__init__(self)
        self._log.debug("Initialize RunUvicorn class object instance.")
        self._cmd = [
            "poetry",
            "run",
            "uvicorn",
            "--host",
            host,
            "--port",
            port,
            "--reload",
            "{0:s}.app.asgi:application".format(package_name),
        ]

    def execute(self):
        """Run uvicorn development server for fastapi-mvc project."""
        self._log.info("Starting uvicorn development server.")
        ShellUtils.run_shell(cmd=self._cmd)
