"""Command-line interface - root."""
import logging

import click
from {{cookiecutter.package_name}}.cli.serve import serve


@click.group(
    help="""{{cookiecutter.project_name}} CLI root."""
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
    else:
        level = logging.INFO

    logging.basicConfig(
        level=level,
        format="[%(asctime)s] [%(process)s] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S %z",
    )


cli.add_command(serve)
