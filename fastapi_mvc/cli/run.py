"""FastAPI MVC CLI run command implementation."""
import os

import click
from fastapi_mvc.commands import Invoker, RunUvicorn, VerifyInstall
from fastapi_mvc.parsers import IniParser


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
    parser = IniParser(os.getcwd())

    invoker = Invoker()
    invoker.on_start = VerifyInstall(script_name=parser.script_name)
    invoker.on_finish = RunUvicorn(
        host=options["host"],
        port=options["port"],
        package_name=parser.package_name,
    )
    invoker.execute()
