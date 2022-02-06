"""FastAPI MVC CLI run command implementation."""
import os
import sys
import configparser
from multiprocessing import cpu_count

import click
import uvicorn


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
    default=1,
    required=False,
    show_default=True,
)
@click.option(
    "--no-reload",
    help="Disable auto-reload.",
    is_flag=True,
    required=False,
)
def run(**options):
    """Run development uvicorn server.

    The 'fastapi-mvc run' commands runs development uvicorn server for a
    fastapi-mvc project at the current working directory.
    \f

    Args:
         options(dict): CLI command options.

    """
    cwd = os.getcwd()
    ini_file = os.path.join(cwd, "fastapi-mvc.ini")

    if not os.path.exists(ini_file) and not os.path.isfile(ini_file):
        click.echo(
            "Not a fastapi-mvc project, fastapi-mvc.ini does not exist.",
        )
        sys.exit(1)

    if not os.access(ini_file, os.R_OK):
        click.echo("File fastapi-mvc.ini is not readable.")
        sys.exit(1)

    config = configparser.ConfigParser()
    config.read(ini_file)
    package_name = config["project"]["package_name"]

    sys.exit(
        uvicorn.run(
            "{0:s}.app.asgi:application".format(package_name),
            host=options["host"],
            port=options["port"],
            reload=True if not options["no_reload"] else False,
            workers=options["workers"],
            log_config=None,
            access_log=True,
        )
    )
