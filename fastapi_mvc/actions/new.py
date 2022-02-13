""""""
import os
from datetime import datetime

from fastapi_mvc.actions import Action
from fastapi_mvc.generators import ProjectGenerator
from fastapi_mvc.utils import ShellUtils
from fastapi_mvc.version import __version__


class GenerateNewProject(Action):

    def __init__(self):
        Action.__init__(self)

    def execute(self, app_path, options):
        app_name = os.path.basename(app_path)
        output_dir = os.path.dirname(app_path)

        if not output_dir:
            output_dir = "."

        author, email = ShellUtils.get_git_user_info()

        cookiecutter_context = {
            "project_name": app_name,
            "redis": "no" if options["skip_redis"] else "yes",
            "aiohttp": "no" if options["skip_aiohttp"] else "yes",
            "github_actions": "no" if options["skip_actions"] else "yes",
            "vagrantfile": "no" if options["skip_vagrantfile"] else "yes",
            "helm": "no" if options["skip_helm"] else "yes",
            "codecov": "no" if options["skip_codecov"] else "yes",
            "author": author,
            "email": email,
            "license": options["license"],
            "repo_url": options["repo_url"],
            "year": datetime.today().year,
            "fastapi_mvc_version": __version__,
        }

        generator = ProjectGenerator()
        generator.new(context=cookiecutter_context, output_dir=output_dir)

        if not options["skip_install"]:
            ShellUtils.run_shell(cmd=["make", "install"], cwd=app_path)
