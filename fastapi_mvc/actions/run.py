import os

from fastapi_mvc.actions import Action
from fastapi_mvc.parsers import IniParser
from fastapi_mvc.utils import ShellUtils


class RunDevelopmentServer(Action):

    def __init__(self):
        Action.__init__(self)

    def execute(self, host, port):
        project = IniParser(os.getcwd())

        cmd = [
            "poetry",
            "run",
            "uvicorn",
            "--host",
            host,
            "--port",
            port,
            "--reload",
            "{0:s}.app.asgi:application".format(project.package_name),
        ]

        ShellUtils.run_shell(cmd)
