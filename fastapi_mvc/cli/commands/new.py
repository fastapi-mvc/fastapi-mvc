"""FastAPI MVC CLI new command."""
import click


@click.command()
@click.argument(
    "APP_PATH",
    nargs=1,
    type=click.Path(exists=False, writable=True),
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
    "--license",
    help="Choose license.",
    type=click.Choice([
        "MIT",
        "BSD2",
        "BSD3",
        "ISC",
        "Apache"
    ]),
)
@click.option(
    "--author",
    help="Author information (format: <name email>).",
    type=click.Tuple((str, str)),
)
@click.option(
    "--repo-url",
    help="Repository url.",
    type=click.STRING,
)
def new(app_path, **options):
    """Create a new FastAPI application.

    The 'fastapi-mvc new' command creates a new FastAPI application with a
    default directory structure and configuration at the path you specify.

    """
    pass
