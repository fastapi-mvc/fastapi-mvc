"""FastAPI MVC CLI run command implementation."""
import os
import sys

import click
from fastapi_mvc.parsers import IniParser
from fastapi_mvc.utils import ShellUtils


@click.command()
@click.option(
    "--host",
    help="Host to bind.",
    type=click.STRING,
    default="127.0.0.1",
    required=False,
    show_default=True,
)
@click.option(
    "-p",
    "--port",
    help="Port to bind.",
    type=click.STRING,
    default="8000",
    required=False,
    show_default=True,
)
def run(**options):
    """Run development uvicorn server.

    The 'fastapi-mvc run' commands runs development uvicorn server for a
    fastapi-mvc project at the current working directory.
    \f

    Args:
         options(dict): CLI command options.

    """
    project = IniParser(os.getcwd())

    cmd = [
        "poetry",
        "run",
        "uvicorn",
        "--host",
        options["host"],
        "--port",
        options["port"],
        "--reload",
        "{0:s}.app.asgi:application".format(project.package_name),
    ]

    ShellUtils.run_shell(cmd)
