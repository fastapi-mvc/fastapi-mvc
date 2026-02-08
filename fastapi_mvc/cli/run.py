"""Command-line interface - run command.

Attributes:
    cmd_help (str): The help string to use for this command.
    cmd_short_help (str): The short help to use for this command. This is shown on the
        command listing of the parent command.

"""

from typing import Dict, Any
from subprocess import CalledProcessError

import click
from fastapi_mvc.cli import ClickAliasedCommand
from fastapi_mvc.utils import run_shell, get_poetry_path, require_fastapi_mvc_project

cmd_short_help = "Run development uvicorn server."
cmd_help = """\
The 'fastapi-mvc run' commands runs development uvicorn server for a
fastapi-mvc project at the current working directory.
"""


@click.command(
    cls=ClickAliasedCommand,
    help=cmd_help,
    short_help=cmd_short_help,
    alias="r",
)
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
@click.option(
    "-i",
    "--install",
    help="Run poetry install.",
    is_flag=True,
)
@click.pass_context
def run(ctx: click.Context, **options: Dict[str, Any]) -> None:
    """Define command-line interface run command.

    Args:
        ctx (click.Context): Click Context class object instance.
        options (typing.Dict[str, typing.Any]): Map of command option names to their
            parsed values.

    """
    project_data = require_fastapi_mvc_project()
    poetry_path = get_poetry_path()

    if options["install"]:
        run_shell(
            cmd=[
                poetry_path,
                "install",
                "--no-interaction",
            ],
            check=True,
        )

    try:
        run_shell(
            cmd=[
                poetry_path,
                "run",
                "uvicorn",
                "--factory",
                "--host",
                f"{options['host']}",
                "--port",
                f"{options['port']}",
                "--reload",
                f"{project_data['package_name']}.app:get_application",
            ],
            check=True,
        )
    except CalledProcessError:
        click.secho("Run 'make install` to install the project.", fg="yellow")
        ctx.exit(1)
