"""Command-line interface - serve command."""
from multiprocessing import cpu_count

import click
from {{cookiecutter.package_name}} import ApplicationLoader
from {{cookiecutter.package_name}}.app import get_application
from {{cookiecutter.package_name}}.cli.utils import validate_directory


cmd_short_help = "Run production server."
cmd_help = """\
Run production gunicorn (WSGI) server with uvicorn (ASGI) workers.
"""


@click.command(
    help=cmd_help,
    short_help=cmd_short_help,
)
@click.option(
    "--bind",
    help="""\
    The socket to bind.
    A string of the form: 'HOST', 'HOST:PORT', 'unix:PATH'.
    An IP is a valid HOST.
    """,
    type=click.STRING,
    required=False,
)
@click.option(
    "-w",
    "--workers",
    help="The number of worker processes for handling requests.",
    type=click.IntRange(min=1, max=cpu_count()),
    required=False,
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
    "raw_env",
    help="Set environment variables in the execution environment.",
    type=click.STRING,
    multiple=True,
    required=False,
)
@click.option(
    "--pid",
    "pidfile",
    help="Specifies the PID file.",
    type=click.Path(),
    callback=validate_directory,
    required=False,
)
@click.pass_context
def serve(ctx, **options):
    """Define command-line interface serve command.

    Args:
        ctx (click.Context): Click Context class object instance.
        options (typing.Dict[str, typing.Any]): Map of command option names to
            their parsed values.

    """
    overrides = dict()

    for key, value in options.items():
        if ctx.get_parameter_source(key).name == "COMMANDLINE":
            overrides[key] = value

    ApplicationLoader(
        application=get_application(),
        overrides=overrides,
    ).run()
