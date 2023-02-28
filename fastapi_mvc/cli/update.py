"""Command-line interface - update command.

Attributes:
    cmd_help (str): The help string to use for this command.
    cmd_short_help (str): The short help to use for this command. This is shown on the
        command listing of the parent command.

"""
import os

import click
import copier
from copier.errors import UserMessageError
from fastapi_mvc.constants import ANSWERS_FILE, COPIER_PROJECT
from fastapi_mvc.cli import ClickAliasedCommand
from fastapi_mvc.utils import ensure_permissions, ensure_project_data


cmd_short_help = "Update fastapi-mvc project."
cmd_help = """\
The 'fastapi-mvc update' commands updates already generated project with the changes
from new template version.
"""


@click.command(
    cls=ClickAliasedCommand,
    help=cmd_help,
    short_help=cmd_short_help,
    alias="u",
)
@click.option(
    "-n",
    "--no-interaction",
    help="Do not ask any interactive question.",
    is_flag=True,
)
@click.option(
    "-p",
    "--pretend",
    help="Run but do not make any changes.",
    is_flag=True,
)
@click.option(
    "--use-version",
    help="The branch, tag or commit ID to checkout after clone.",
    type=click.STRING,
)
@click.pass_context
def update(ctx, **options):
    """Define command-line interface update command.

    Args:
        ctx (click.Context): Click Context class object instance.
        options (typing.Dict[str, typing.Any]): Map of command option names to their
            parsed values.

    """
    project_data = ensure_project_data()
    ensure_permissions(os.getcwd(), w=True)

    if options["no_interaction"]:
        update_kwargs = {
            "data": project_data,
            "overwrite": True,
        }
    else:
        update_kwargs = {
            "user_defaults": project_data,
        }

    try:
        copier.run_update(
            vcs_ref=options["use_version"] or COPIER_PROJECT.vcs_ref,
            answers_file=ANSWERS_FILE,
            pretend=options["pretend"],
            **update_kwargs,
        )
    except UserMessageError as ex:
        click.secho(ex, fg="yellow")
        ctx.exit(2)
