"""FastAPI MVC command VerifyInstall class implementation.

The fastapi-mvc.commands submodule implements command design pattern:
https://refactoring.guru/design-patterns/command
"""
from subprocess import DEVNULL

from fastapi_mvc.commands import Command
from fastapi_mvc.utils import ShellUtils
from fastapi_mvc.exceptions import CommandException


class VerifyInstall(Command):
    """Command VerifyInstall class definition."""

    __slots__ = "_cmd"

    def __init__(self, script_name):
        """Initialize VerifyInstall class object instance.

        Args:
            script_name(str): Generated fastapi-mvc project CLI script name.

        """
        Command.__init__(self)
        self._log.debug("Initialize VerifyInstall class object instance.")
        self._cmd = [
            "poetry",
            "run",
            script_name,
            "--help",
        ]

    def execute(self):
        """Verify if fastapi-mvc project is installed."""
        self._log.debug("Verifying if fastapi-mvc project is installed.")
        process = ShellUtils.run_shell(
            cmd=self._cmd,
            stdout=DEVNULL,
            stderr=DEVNULL,
        )

        if process.returncode != 0:
            self._log.error(
                "Project is not installed. To install run: $ make install"
            )
            raise CommandException("Project is not installed.")
