"""Fastapi-mvc generators - script generator.

Attributes:
    cmd_help (str): The help string to use for this command.
    cmd_short_help (str): The short help to use for this command. This is shown on the
        command listing of the parent command.
    epilog (str): Like the help string, but it’s printed at the end of the help page
        after everything else.

"""
import os.path

import click
from fastapi_mvc import Generator


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
    cls=Generator,
    template="https://github.com/fastapi-mvc/copier-script.git",
    vcs_ref="0.1.0",
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
@click.pass_context
def script(ctx, name, **options):
    """Define script generator command-line interface.

    Args:
        ctx (click.Context): Click Context class object instance.
        name (str): Given script name.
        options (typing.Dict[str, typing.Any]): Map of command option names to
            their parsed values.

    """
    ctx.command.ensure_permissions(os.getcwd(), w=True)

    # Sanitize values
    name = name.lower().replace(" ", "_")

    data = {
        "nix": options["use_nix"],
        "script": name,
    }

    ctx.command.run_copy(data=data, answers_file=None)
