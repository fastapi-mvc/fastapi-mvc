"""Fastapi-mvc generators - controller generator.

Attributes:
    cmd_help (str): The help string to use for this command.
    cmd_short_help (str): The short help to use for this command. This is shown on the
        command listing of the parent command.
    epliog (str): Like the help string but it’s printed at the end of the help page
        after everything else.

"""
import click
from fastapi_mvc import Generator


cmd_short_help = "Run fastapi-mvc controller generator."
cmd_help = """\
Creates a new controller and its endpoints. Pass the controller name
under_scored, and a list of endpoints as arguments.

This generates a controller file in app/controllers with unit test
file. Finally, edits config/router.py in order to add controller to
FastAPI router.
"""
epilog = """\
Example:
    `fastapi-mvc generate controller stock_market ticker buy:post sell:delete`

    Creates controller with URLs like /stock_market/ticker.
        Controller: app/controllers/stock_market.py
        Test:       tests/unit/app/controllers/test_stock_market.py
"""


@click.command(
    cls=Generator,
    template="https://github.com/fastapi-mvc/copier-controller.git",
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
@click.argument(
    "ENDPOINTS",
    required=False,
    nargs=-1,
)
@click.option(
    "-R",
    "--skip-routes",
    help="Do not add router entry to app/router.py.",
    is_flag=True,
)
@click.pass_context
def controller(ctx, name, endpoints, **options):
    """Define controller generator command-line interface.

    Args:
        ctx (click.Context): Click Context class object instance.
        name (str): Given controller name.
        endpoints (str): Given controller endpoints.
        options (typing.Dict[str, typing.Any]): Map of command option names to
            their parsed values.

    """
    ctx.command.ensure_project_data()
    name = name.lower().replace("-", "_")
    data = {
        "project_name": ctx.command.project_data["project_name"],
        "controller": name,
        "endpoints": {},
    }

    for entry in endpoints:
        try:
            endpoint, method = entry.split(":", maxsplit=1)
        except ValueError:
            endpoint, method = entry, "get"

        # Sanitize values
        endpoint = endpoint.lower().replace("-", "_")
        method = method.lower()

        data["endpoints"][endpoint] = method

    ctx.command.run_copy(data=data)

    if not options["skip_routes"]:
        ctx.command.insert_router_import(name)
