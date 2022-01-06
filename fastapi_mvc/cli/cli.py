"""FastAPI MVC CLI root implementation."""
import logging

import click
from fastapi_mvc.cli.commands.new import new


@click.group()
@click.option(
    "-v",
    "--verbose",
    help="Enable verbose logging.",
    is_flag=True,
    default=False,
)
def cli(**options):
    """Generate and manage fastapi-mvc projects. # noqa: D205,D400

    \f

    Args:
        options(dict): CLI command options.

    """
    if options["verbose"]:
        level = logging.DEBUG
    else:
        level = logging.INFO

    logging.basicConfig(
        level=level,
        format="[%(asctime)s] [%(process)s] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S %z",
    )


cli.add_command(new)
