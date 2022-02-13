"""FastAPI MVC CLI run command implementation."""
import click
from fastapi_mvc.actions import Context, RunDevelopmentServer


@click.command()
@click.option(
    "--host",
    help="Host to bind.",
    type=click.STRING,
    default="127.0.0.1",
    required=False,
    show_default=True,
)
@click.option(
    "-p",
    "--port",
    help="Port to bind.",
    type=click.STRING,
    default="8000",
    required=False,
    show_default=True,
)
def run(**options):
    """Run development uvicorn server.

    The 'fastapi-mvc run' commands runs development uvicorn server for a
    fastapi-mvc project at the current working directory.
    \f

    Args:
         options(dict): CLI command options.

    """
    context = Context(action=RunDevelopmentServer())
    context.execute(host=options["host"], port=options["port"])
