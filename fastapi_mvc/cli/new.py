"""FastAPI MVC CLI new command implementation."""
import click
from fastapi_mvc.commands import Invoker, GenerateNewProject, InstallProject


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
    invoker = Invoker()
    invoker.on_start = GenerateNewProject(app_path=app_path, options=options)

    if not options["skip_install"]:
        invoker.on_finish = InstallProject(app_path=app_path)

    invoker.execute()
