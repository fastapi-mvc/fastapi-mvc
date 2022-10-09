"""Command-line interface - root.

Attributes:
    cmd_help (str): The help string to use for this command.

"""
import logging
import sys

import click
from fastapi_mvc.cli.run import run
from fastapi_mvc.cli.new import new
from fastapi_mvc.cli.generate import get_generate_cmd
from fastapi_mvc.utils import global_except_hook


sys.excepthook = global_except_hook
cmd_help = """\
Developer productivity tool for making high-quality FastAPI production-ready
APIs.

Documentation: https://fastapi-mvc.netlify.app

Source: https://github.com/fastapi-mvc/fastapi-mvc
"""


@click.group(
    help=cmd_help,
)
@click.option(
    "-v",
    "--verbose",
    help="Enable verbose logging.",
    is_flag=True,
    default=False,
)
def cli(**options):
    """Define command-line interface root.

    Args:
        options (typing.Dict[str, typing.Any]): Map of command option names to
            their parsed values.

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
cli.add_command(get_generate_cmd())
