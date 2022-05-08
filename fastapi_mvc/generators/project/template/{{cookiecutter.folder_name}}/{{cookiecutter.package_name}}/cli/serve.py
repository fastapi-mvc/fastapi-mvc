"""Command-line interface - serve command."""
from multiprocessing import cpu_count

import click
from {{cookiecutter.package_name}}.cli.utils import validate_directory
from {{cookiecutter.package_name}}.wsgi import run_wsgi


cmd_short_help = "Run production server."
cmd_help = """\
Run production gunicorn (WSGI) server with uvicorn (ASGI) workers.
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
    type=click.INT,
    default=8000,
    required=False,
    show_default=True,
)
@click.option(
    "-w",
    "--workers",
    help="The number of worker processes for handling requests.",
    type=click.IntRange(min=1, max=cpu_count()),
    default=2,
    required=False,
    show_default=True,
)
@click.option(
    "-D",
    "--daemon",
    help="Daemonize the Gunicorn process.",
    is_flag=True,
    required=False,
)
@click.option(
    "-e",
    "--env",
    help="Set environment variables in the execution environment.",
    type=click.STRING,
    multiple=True,
    required=False,
)
@click.option(
    "-c",
    "--config",
    help="Uses a custom gunicorn.conf.py configuration",
    type=click.Path(exists=True, file_okay=True, readable=True),
    required=False,
)
@click.option(
    "--pid",
    help="Specifies the PID file.",
    type=click.Path(),
    callback=validate_directory,
    required=False,
)
def serve(**options):
    """Define command-line interface serve command.

    Args:
        options (typing.Dict[str, typing.Any]): Map of command option names to
            their parsed values.

    """
    run_wsgi(
        host=options["host"],
        port=str(options["port"]),
        workers=str(options["workers"]),
        daemon=options["daemon"],
        env=options["env"],
        config=options["config"],
        pid=options["pid"],
    )
