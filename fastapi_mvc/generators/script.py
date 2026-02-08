"""Fastapi-mvc generators - script generator.

Attributes:
    cmd_help (str): The help string to use for this command.
    cmd_short_help (str): The short help to use for this command. This is shown on the
        command listing of the parent command.
    epilog (str): Like the help string, but it’s printed at the end of the help page
        after everything else.

"""
from typing import Dict, Any
import os

import click
import copier
from fastapi_mvc.cli import GeneratorCommand
from fastapi_mvc.constants import COPIER_SCRIPT
from fastapi_mvc.utils import ensure_permissions


cmd_short_help = "Run shell script generator."
cmd_help = """\
Creates an executable shell script scaffold at the current working directory.

Generator template used: https://github.com/fastapi-mvc/copier-script
"""
epilog = """\
Example:
    `fastapi-mvc generate script example.sh`

    Or using short-cut alias:
    `fm g ss example.sh`

    creates an executable file:
        example.sh
"""


@click.command(
    cls=GeneratorCommand,
    category="Builtins",
    help=cmd_help,
    short_help=cmd_short_help,
    epilog=epilog,
    alias="ss",
)
@click.option(
    "-n",
    "--use-nix",
    help="Use nix-shell (shebang header).",
    is_flag=True,
)
@click.argument(
    "NAME",
    required=True,
    nargs=1,
)
def script(name: str, **options: Dict[str, Any]) -> None:
    """Define script generator command-line interface.

    Args:
        name (str): Given script name.
        options (typing.Dict[str, typing.Any]): Map of command option names to
            their parsed values.

    """
    ensure_permissions(os.getcwd(), w=True)
    data = {
        "nix": options["use_nix"],
        "script": name.lower().replace(" ", "_"),
    }
    copier.run_copy(
        src_path=COPIER_SCRIPT.template,
        vcs_ref=COPIER_SCRIPT.vcs_ref,
        unsafe=True,
        data=data,
    )
