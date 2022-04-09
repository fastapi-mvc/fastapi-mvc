"""FastAPI MVC CLI generate command implementation."""
import click


@click.group()
@click.option(
    "-f",
    "--force",
    help="Overwrite files that already exist",
    is_flag=True,
)
@click.option(
    "-s",
    "--skip",
    help="Skip files that already exist",
    is_flag=True,
)
def generate(**options):
    print(options)


@generate.command()
@click.argument(
    "NAME",
    nargs=1,
)
@click.argument(
    "ENDPOINTS",
    nargs=-1,
    required=False,
)
def controller(**options):
    print(options)
