"""FastAPI MVC GenerateNewProject command class implementation.

The fastapi-mvc.commands submodule implements command design pattern:
https://refactoring.guru/design-patterns/command
"""
import os
from datetime import datetime

from fastapi_mvc.commands import Command
from fastapi_mvc.generators import ProjectGenerator
from fastapi_mvc.utils import ShellUtils
from fastapi_mvc.version import __version__


class GenerateNewProject(Command):
    """"""
    __slots__ = (
        "_app_path",
        "_options",
    )

    def __init__(self, app_path, options):
        """"""
        Command.__init__(self)
        self._log.debug(
            "Initialize GenerateNewProject class object instance."
        )
        self._app_path = app_path
        self._options = options

    def _get_value(self, option):
        if self._options[option]:
            return "no"
        else:
            return"yes"

    def execute(self):
        """"""
        app_name = os.path.basename(self._app_path)
        output_dir = os.path.dirname(self._app_path)

        if not output_dir:
            output_dir = "."

        author, email = ShellUtils.get_git_user_info()

        context = {
            "project_name": app_name,
            "redis": self._get_value("skip_redis"),
            "aiohttp": self._get_value("skip_aiohttp"),
            "github_actions": self._get_value("skip_actions"),
            "vagrantfile": self._get_value("skip_vagrantfile"),
            "helm": self._get_value("skip_helm"),
            "codecov": self._get_value("skip_codecov"),
            "author": author,
            "email": email,
            "license": self._options["license"],
            "repo_url": self._options["repo_url"],
            "year": datetime.today().year,
            "fastapi_mvc_version": __version__,
        }

        generator = ProjectGenerator()
        generator.new(context=context, output_dir=output_dir)
