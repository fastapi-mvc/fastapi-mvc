"""Command-line interface.

The ``fastapi_mvc.cli`` submodule defines Click command-line interface root and
its commands.

Resources:
    1. `Click documentation`_

.. _Click documentation:
    https://click.palletsprojects.com/en/8.1.x/

"""

from fastapi_mvc.cli.base import (
    ClickAliasedGroup,
    ClickAliasedCommand,
    GeneratorCommand,
    GeneratorsMultiCommand,
)

__all__ = (
    "ClickAliasedGroup",
    "ClickAliasedCommand",
    "GeneratorCommand",
    "GeneratorsMultiCommand",
)
