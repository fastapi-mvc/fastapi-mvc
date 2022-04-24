"""FastAPI MVC CLI run command implementation."""
import click
from fastapi_mvc import Borg
from fastapi_mvc.commands import RunShell


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
@click.option(
    "-I",
    "--skip-install",
    help="Do not run poetry install.",
    is_flag=True,
)
def run(**options):
    """Run development uvicorn server.

    The 'fastapi-mvc run' commands runs development uvicorn server for a
    fastapi-mvc project at the current working directory.
    \f

    Args:
         options (dict): CLI command options.

    """
    borg = Borg()
    borg.require_project()

    if not options["skip_install"]:
        borg.enqueue_command(
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

    borg.enqueue_command(
        RunShell(
            cmd=[
                borg.poetry_path,
                "run",
                "uvicorn",
                "--host",
                options["host"],
                "--port",
                options["port"],
                "--reload",
                "{0:s}.app.asgi:application".format(borg.parser.package_name),
            ],
            cwd=borg.parser.project_root,
        )
    )
    borg.execute()
