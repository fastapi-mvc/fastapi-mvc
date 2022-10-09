"""Fastapi-mvc generators - generator generator.

Attributes:
    cmd_help (str): The help string to use for this command.
    cmd_short_help (str): The short help to use for this command. This is shown on the
        command listing of the parent command.
    epliog (str): Like the help string but it’s printed at the end of the help page
        after everything else.

"""
from datetime import datetime

import click
from fastapi_mvc import Generator


cmd_short_help = "Run fastapi-mvc generator generator."
cmd_help = """\
Creates a new generator at lib/generators. Pass the generator name
under_scored.
"""
epilog = """\
Example:
    `fastapi-mvc generate generator awesome`

    creates a standard awesome generator:
        lib/generators/awesome/.envrc
        lib/generators/awesome/.gitignore
        lib/generators/awesome/CHANGELOG.md
        lib/generators/awesome/LICENSE
        lib/generators/awesome/README.md
        lib/generators/awesome/__init__.py
        lib/generators/awesome/poetry.lock
        lib/generators/awesome/pyproject.toml
        lib/generators/awesome/template
        lib/generators/awesome/template/{{package_name}}
        lib/generators/awesome/template/{{package_name}}/hello_world.py
        lib/generators/awesome/update.sh
        lib/generators/awesome/default.nix
        lib/generators/awesome/shell.nix
        lib/generators/awesome/.fastapi-mvc.yml
        lib/generators/awesome/awesome.py
"""


@click.command(
    cls=Generator,
    template="https://github.com/fastapi-mvc/copier-generator.git",
    vcs_ref="0.1.0",
    category="Builtins",
    help=cmd_help,
    short_help=cmd_short_help,
    epilog=epilog,
)
@click.argument(
    "NAME",
    required=True,
    nargs=1,
)
@click.option(
    "-N",
    "--skip-nix",
    help="Skip nix expression files.",
    is_flag=True,
)
@click.option(
    "--license",
    help="Choose license.",
    type=click.Choice(
        [
            "MIT",
            "BSD2",
            "BSD3",
            "ISC",
            "Apache2.0",
            "LGPLv3+",
            "LGPLv3",
            "LGPLv2+",
            "LGPLv2",
            "no",
        ]
    ),
    default="MIT",
    show_default=True,
)
@click.option(
    "--repo-url",
    help="New project repository url.",
    type=click.STRING,
    envvar="REPO_URL",
    default="https://your.repo.url.here",
)
@click.pass_context
def generator(ctx, name, **options):
    """Define generator generator command-line interface.

    Args:
        ctx (click.Context): Click Context class object instance.
        name (str): Given generator name.
        options (typing.Dict[str, typing.Any]): Map of command option names to
            their parsed values.

    """
    ctx.command.ensure_project_data()

    # Sanitize value
    name = name.lower().replace("-", "_").replace(" ", "_")

    data = {
        "generator": name,
        "nix": not options["skip_nix"],
        "repo_url": options["repo_url"],
        "license": options["license"],
        "copyright_date": datetime.today().year,
    }

    ctx.command.run_copy(
        dst_path=f"./lib/generators/{name}",
        data=data,
        answers_file=".generator.yml",
    )
