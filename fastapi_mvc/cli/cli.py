"""FastAPI MVC CLI root implementation."""
import logging
import sys

import click
from fastapi_mvc.cli.new import new
from fastapi_mvc.cli.run import run
from fastapi_mvc.cli.generate import generate
from fastapi_mvc.utils import global_except_hook


sys.excepthook = global_except_hook


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
        fmt = "[%(asctime)s] [%(name)s:%(lineno)d] [%(levelname)s] %(message)s"
    else:
        level = logging.INFO
        fmt = "[%(levelname)s] %(message)s"

    logging.basicConfig(
        level=level,
        format=fmt,
        datefmt="%Y-%m-%d %H:%M:%S %z",
    )


cli.add_command(new)
cli.add_command(run)
cli.add_command(generate)
