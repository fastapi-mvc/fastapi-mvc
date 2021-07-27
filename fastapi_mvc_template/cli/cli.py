# -*- coding: utf-8 -*-
"""FastAPI MVC template CLI root."""
import logging

import click
from fastapi_mvc_template.cli.commands.serve import serve


@click.group()
@click.option(
    "-v",
    "--verbose",
    help="Enable verbose logging.",
    is_flag=True,
    default=False,
)
def cli(**options):
    """FastAPI MVC template CLI root."""
    if options['verbose']:
        level = logging.DEBUG
    else:
        level = logging.INFO

    logging.basicConfig(
        level=level,
        format="[%(asctime)s] [%(process)s] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S %z",
    )


cli.add_command(serve)
