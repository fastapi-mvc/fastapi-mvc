"""Command-line interface - run command."""
import click
from fastapi_mvc import Borg
from fastapi_mvc.commands import RunShell


cmd_short_help = "Run development uvicorn server."
cmd_help = """\
The 'fastapi-mvc run' commands runs development uvicorn server for a
fastapi-mvc project at the current working directory.
"""


@click.command(
    help=cmd_help,
    short_help=cmd_short_help,
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
    "-I",
    "--skip-install",
    help="Do not run poetry install.",
    is_flag=True,
)
def run(**options):
    """Define command-line interface run command.

    Args:
         options (typing.Dict[str, typing.Any]): Map of command option names to
            their parsed values.

    """
    borg = Borg()
    borg.require_project()

    if not options["skip_install"]:
        borg.enqueue(
            RunShell(
                cmd=[
                    borg.poetry_path,
                    "install",
                    "--no-interaction",
                ],
                check=True,
                cwd=borg.parser.project_root,
            )
        )

    borg.enqueue(
        RunShell(
            cmd=[
                borg.poetry_path,
                "run",
                "uvicorn",
                "--factory",
                "--host",
                options["host"],
                "--port",
                options["port"],
                "--reload",
                "{0:s}.app:get_application".format(borg.parser.package_name),
            ],
            cwd=borg.parser.project_root,
        )
    )
    borg.execute()
