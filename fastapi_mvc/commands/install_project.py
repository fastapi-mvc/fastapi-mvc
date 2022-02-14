"""FastAPI MVC GenerateNewProject command class implementation.

The fastapi-mvc.commands submodule implements command design pattern:
https://refactoring.guru/design-patterns/command
"""
from fastapi_mvc.commands import Command
from fastapi_mvc.utils import ShellUtils


class InstallProject(Command):
    """"""
    __slots__ = (
        "_app_path"
    )

    def __init__(self, app_path):
        """"""
        Command.__init__(self)
        self._log.debug(
            "Initialize InstallProject class object instance."
        )
        self._app_path = app_path

    def execute(self):
        """"""
        ShellUtils.run_shell(cmd=["make", "install"], cwd=self._app_path)
