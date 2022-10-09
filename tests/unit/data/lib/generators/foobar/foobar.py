"""Custom fastapi-mvc foobar generator implementation."""
import click
from fastapi_mvc import Generator


cmd_short_help = "Run custom generator foobar."
cmd_help = """\
Creates a dummy hello_world.py example.
"""
epilog = """\
Example:
    `fastapi-mvc generate foobar WORLD!`

    creates an example file:
        helo_world.py

"""


@click.command(
    cls=Generator,
    # Or use repository address
    template="./.",
    category="Custom",
    help=cmd_help,
    short_help=cmd_short_help,
)
@click.argument(
    "NAME",
    required=True,
    nargs=1,
)
@click.pass_context
def foobar(ctx, name):
    # You can access Generator class object instance for this command via click.Context
    # https://click.palletsprojects.com/en/8.1.x/api/?highlight=context#click.Context.command
    ctx.command.ensure_project_data()

    data = {
        "project_name": ctx.command.project_data["project_name"],
        "name": name.lower().replace("-", "_"),
    }

    ctx.command.run_copy(data=data)
