"""Command-line interface - new command.

Attributes:
    cmd_help (str): The help string to use for this command.
    cmd_short_help (str): The short help to use for this command. This is shown on the
        command listing of the parent command.

"""
import logging
import os
from datetime import datetime

import click
from fastapi_mvc import Generator, VERSION
from fastapi_mvc.utils import run_shell, get_git_user_info


log = logging.getLogger(__name__)
cmd_short_help = "Create a new FastAPI application."
cmd_help = """\
The 'fastapi-mvc new' command creates a new FastAPI application with a
default directory structure and configuration at the path you specify.

Default Project template used: https://github.com/fastapi-mvc/copier-project

"""


@click.command(
    cls=Generator,
    template="https://github.com/fastapi-mvc/copier-project.git",
    vcs_ref="0.1.0",
    help=cmd_help,
    short_help=cmd_short_help,
)
@click.argument(
    "APP_PATH",
    nargs=1,
    type=click.Path(exists=False),
    required=True,
)
@click.option(
    "-R",
    "--skip-redis",
    help="Skip Redis utility files.",
    is_flag=True,
)
@click.option(
    "-A",
    "--skip-aiohttp",
    help="Skip aiohttp utility files.",
    is_flag=True,
)
@click.option(
    "-H",
    "--skip-helm",
    help="Skip Helm chart files.",
    is_flag=True,
)
@click.option(
    "-G",
    "--skip-actions",
    help="Skip GitHub actions files.",
    is_flag=True,
)
@click.option(
    "-I",
    "--skip-install",
    help="Do not run make install after project generation.",
    is_flag=True,
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
@click.option(
    "-n",
    "--no-interaction",
    help="Do not ask any interactive question.",
    is_flag=True,
)
@click.option(
    "--use-repo",
    help="Overrides fastapi-mvc copier-project repository.",
    type=click.STRING,
)
@click.option(
    "--use-version",
    help="The branch, tag or commit ID to checkout after clone.",
    type=click.STRING,
)
@click.pass_context
def new(ctx, app_path, **options):
    """Define command-line interface new command.

    Args:
        ctx (click.Context): Click Context class object instance.
        app_path (str): Destination path where to render the project.
        options (typing.Dict[str, typing.Any]): Map of command option names to their
            parsed values.

    """
    if options["use_repo"]:
        ctx.command.template = options["use_repo"]
    if options["use_version"]:
        ctx.command.vcs_ref = options["use_version"]

    author, email = get_git_user_info()
    data = {
        "project_name": os.path.basename(app_path),
        "author": author,
        "email": email,
        "copyright_date": datetime.today().year,
        "fastapi_mvc_version": VERSION,
        "nix": not options["skip_nix"],
        "redis": not options["skip_redis"],
        "aiohttp": not options["skip_aiohttp"],
        "github_actions": not options["skip_actions"],
        "helm": not options["skip_helm"],
        "license": options["license"],
        "repo_url": options["repo_url"],
        "container_image_name": os.path.basename(app_path),
        "chart_name": os.path.basename(app_path),
        "script_name": os.path.basename(app_path),
        "project_description": "This project was generated with fastapi-mvc.",
        "version": "0.1.0",
    }

    if options["no_interaction"]:
        ctx.command.run_auto(dst_path=app_path, data=data)
    else:
        ctx.command.run_auto(dst_path=app_path, user_defaults=data)

    if not options["skip_install"]:
        ctx.command.copier_printf(
            action="run",
            msg="make install",
            style="OK",
        )
        run_shell(cmd=["make", "install"], cwd=app_path)
