"""FastAPI MVC CLI root implementation."""
import logging

import click
from fastapi_mvc.cli.new import new
from fastapi_mvc.cli.run import run


@click.group()
@click.option(
    "-v",
    "--verbose",
    help="Enable verbose logging.",
    is_flag=True,
    default=False,
)
def cli(**options):
    """Create and develop production grade FastAPI projects.

    Documentation: https://fastapi-mvc.netlify.app

    Source Code: https://github.com/rszamszur/fastapi-mvc
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
cli.add_command(run)
