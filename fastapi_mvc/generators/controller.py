"""Fastapi-mvc generators - controller generator.

Attributes:
    cmd_help (str): The help string to use for this command.
    cmd_short_help (str): The short help to use for this command. This is shown on the
        command listing of the parent command.
    epilog (str): Like the help string, but it’s printed at the end of the help page
        after everything else.

"""

from typing import List, Dict, Any
import os

import click
import copier
from fastapi_mvc.cli import GeneratorCommand
from fastapi_mvc.constants import COPIER_CONTROLLER
from fastapi_mvc.utils import require_fastapi_mvc_project

cmd_short_help = "Run fastapi-mvc controller generator."
cmd_help = """\
Creates a new controller and its endpoints. Pass the controller name
under_scored, and a list of endpoints as arguments.

This generates a controller file in app/controllers with unit test
file. Finally, edits config/router.py in order to add controller to
FastAPI router.

Generator template used: https://github.com/fastapi-mvc/copier-controller
"""
epilog = """\
Example:
    `fastapi-mvc generate controller stock_market ticker buy:post sell:delete`

    Or using short-cut alias:
    `fm g ctl stock_market ticker buy:post sell:delete`

    Creates controller with URLs like /stock_market/ticker.
        Controller: app/controllers/stock_market.py
        Test:       tests/unit/app/controllers/test_stock_market.py
"""


def insert_router_import(package_name: str, controller_name: str) -> None:
    """Insert import and router entry into ``app/router.py`` file.

    Args:
        package_name (str): Given fastapi-mvc project Python package name.
        controller_name (str): Given controller name.

    """
    router = os.path.join(os.getcwd(), f"{package_name}/app/router.py")
    import_str = f"from {package_name}.app.controllers import {controller_name}\n"

    with open(router, "r") as f:
        lines = f.readlines()

    if import_str in lines:
        return

    for i in range(len(lines)):
        if lines[i].strip() == "from fastapi import APIRouter":
            index = i + 1
            break
    else:
        index = 0

    lines.insert(index, import_str)
    lines.append(f"root_api_router.include_router({controller_name}.router)\n")

    with open(router, "w") as f:
        f.writelines(lines)


@click.command(
    cls=GeneratorCommand,
    category="Builtins",
    help=cmd_help,
    short_help=cmd_short_help,
    epilog=epilog,
    alias="ctl",
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
def controller(name: str, endpoints: List[str], **options: Dict[str, Any]) -> None:
    """Define controller generator command-line interface.

    Args:
        name (str): Given controller name.
        endpoints (typing.List[str]): Given controller endpoints.
        options (typing.Dict[str, typing.Any]): Map of command option names to
            their parsed values.

    """
    project_data = require_fastapi_mvc_project()
    name = name.lower().replace("-", "_")
    data = {
        "project_name": project_data["project_name"],
        "controller": name,
        "endpoints": {},
    }

    for entry in endpoints:
        try:
            endpoint, method = entry.split(":", maxsplit=1)
        except ValueError:
            endpoint, method = entry, "get"

        endpoint = endpoint.lower().replace("-", "_")
        method = method.lower()

        data["endpoints"][endpoint] = method

    copier.run_copy(
        src_path=COPIER_CONTROLLER.template,
        vcs_ref=COPIER_CONTROLLER.vcs_ref,
        dst_path=os.getcwd(),
        data=data,
    )

    if not options["skip_routes"]:
        insert_router_import(project_data["package_name"], name)
