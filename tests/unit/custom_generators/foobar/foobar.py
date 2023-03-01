"""Custom fastapi-mvc foobar generator implementation."""
import os

import click
import copier
from fastapi_mvc.cli import GeneratorCommand
from fastapi_mvc.utils import require_fastapi_mvc_project
from fastapi_mvc.constants import ANSWERS_FILE


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
    cls=GeneratorCommand,
    category="Custom",
    help=cmd_help,
    short_help=cmd_short_help,
    alias="foo",
)
@click.argument(
    "NAME",
    required=True,
    nargs=1,
)
def foobar(name):
    project_data = require_fastapi_mvc_project()
    data = {
        "project_name": project_data["project_name"],
        "name": name.lower().replace("-", "_"),
    }

    copier.run_copy(
        src_path=os.path.dirname(__file__),  # Or use repository address
        data=data,
        answers_file=ANSWERS_FILE,
    )
