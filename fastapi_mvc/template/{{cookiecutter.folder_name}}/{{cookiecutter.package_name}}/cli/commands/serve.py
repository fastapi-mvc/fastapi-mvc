# -*- coding: utf-8 -*-
"""{{cookiecutter.project_name}} CLI serve command."""
import os
from multiprocessing import cpu_count

import click
from {{cookiecutter.package_name}}.wsgi import run_wsgi


def validate_directory(ctx, param, value):
    """Verify that the value is a path which directory exists and is writable.

    Args:
        ctx(click.Context): Click Context object instance.
        param(click.Option): Click Option object instance.
        value(str): Click Option value.

    Returns:
        Original option value.

    Raises:
        click.BadParameter: If provided path value directory does not exist or
            is not writable.

    """
    if not param.required and not value:
        return value

    dirname = os.path.dirname(value)

    if not os.path.exists(dirname):
        raise click.BadParameter(
            "Directory '{dir}' does not exist.".format(dir=dirname)
        )
    elif not os.access(dirname, os.W_OK):
        raise click.BadParameter(
            "Directory '{dir}' is not writable.".format(dir=dirname)
        )

    return value


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
    """{{cookiecutter.project_name}} CLI serve command."""
    run_wsgi(
        host=options["host"],
        port=str(options["port"]),
        workers=str(options["workers"]),
        daemon=options["daemon"],
        env=options["env"],
        config=options["config"],
        pid=options["pid"],
    )
