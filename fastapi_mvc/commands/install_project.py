"""FastAPI MVC command InstallProject class implementation.

The fastapi-mvc.commands submodule implements command design pattern:
https://refactoring.guru/design-patterns/command
"""
from fastapi_mvc.commands import Command
from fastapi_mvc.utils import ShellUtils


class InstallProject(Command):
    """Command InstallProject class definition."""

    __slots__ = "_app_path"

    def __init__(self, app_path):
        """Initialize InstallProject class object instance.

        Args:
            app_path(str): Path to fastapi-mvc project root.

        """
        Command.__init__(self)
        self._log.debug("Initialize InstallProject class object instance.")
        self._app_path = app_path

    def execute(self):
        """Run fastapi-mvc project installation."""
        self._log.info("Installing project")
        ShellUtils.run_shell(cmd=["make", "install"], cwd=self._app_path)
