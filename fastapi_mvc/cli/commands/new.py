"""FastAPI MVC CLI new command implementation."""
import os
from datetime import datetime

import click
from fastapi_mvc.generators import ProjectGenerator
from fastapi_mvc.utils import ShellUtils
from fastapi_mvc.version import __version__


@click.command()
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
    "-V",
    "--skip-vagrantfile",
    help="Skip Vagrantfile.",
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
    "-C",
    "--skip-codecov",
    help="Skip codecov in GitHub actions.",
    is_flag=True,
)
@click.option(
    "-I",
    "--skip-install",
    help="Dont run make install",
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
    envvar="LICENSE",
)
@click.option(
    "--repo-url",
    help="Repository url.",
    type=click.STRING,
    envvar="REPO_URL",
    default="https://your.repo.url.here",
)
def new(app_path, **options):
    """Create a new FastAPI application.

    The 'fastapi-mvc new' command creates a new FastAPI application with a
    default directory structure and configuration at the path you specify.
    \f

    Args:
        app_path(str): CLI command argument - new application path.
        options(dict): CLI command options.

    """
    app_name = os.path.basename(app_path)
    output_dir = os.path.dirname(app_path)

    if not output_dir:
        output_dir = "."

    author, email = ShellUtils.get_git_user_info()

    context = {
        "project_name": app_name,
        "redis": "no" if options["skip_redis"] else "yes",
        "aiohttp": "no" if options["skip_aiohttp"] else "yes",
        "github_actions": "no" if options["skip_actions"] else "yes",
        "vagrantfile": "no" if options["skip_vagrantfile"] else "yes",
        "helm": "no" if options["skip_helm"] else "yes",
        "codecov": "no" if options["skip_codecov"] else "yes",
        "author": author,
        "email": email,
        "repo_url": options["repo_url"],
        "year": datetime.today().year,
        "fastapi_mvc_version": __version__,
    }

    generator = ProjectGenerator()
    generator.new(context=context, output_dir=output_dir)

    if not options["skip_install"]:
        ShellUtils.run_project_install(app_path)
