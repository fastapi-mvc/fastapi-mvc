"""Command-line interface - update command.

Attributes:
    cmd_help (str): The help string to use for this command.
    cmd_short_help (str): The short help to use for this command. This is shown on the
        command listing of the parent command.

"""
import os

import click
from copier.errors import UserMessageError
from fastapi_mvc import Generator


cmd_short_help = "Update fastapi-mvc project."
cmd_help = """\
The 'fastapi-mvc update' commands updates already generated project with the changes
from new template version.
"""


@click.command(
    cls=Generator,
    template="https://github.com/fastapi-mvc/copier-project.git",
    vcs_ref="0.3.0",
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
    ctx.command.ensure_project_data()
    ctx.command.ensure_permissions(os.getcwd(), w=True)

    if options["use_version"]:
        ctx.command.vcs_ref = options["use_version"]

    if options["no_interaction"]:
        update_kwargs = {
            "data": ctx.command.project_data,
            "overwrite": True,
        }
    else:
        update_kwargs = {
            "user_defaults": ctx.command.project_data,
        }

    try:
        ctx.command.run_update(**update_kwargs, pretend=options["pretend"])
    except UserMessageError as ex:
        click.secho(ex, fg="yellow")
        ctx.exit(2)
