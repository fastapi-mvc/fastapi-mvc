"""FastAPI MVC controller generator implementation."""
import os

from cookiecutter.main import cookiecutter
from fastapi_mvc.generators import Generator


class ControllerGenerator(Generator):

    name = "controller"
    template = os.path.abspath(
        os.path.join(
            os.path.abspath(__file__),
            "../template",
        )
    )
    usage = os.path.join(template, "USAGE")
    category = "Builtins"
    cli_arguments = [
        *Generator.cli_arguments,
        {
            "param_decls": ["ENDPOINTS"],
            "required": False,
            "nargs": -1,
        }
    ]
    cli_options = [
        *Generator.cli_options,
        {
            "param_decls": ["-R", "--skip-routes"],
            "is_flag": True,
            "help": "Wether to skip routes entry",
        }
    ]

    def __init__(self, parser):
        Generator.__init__(self, parser)

    def new(self, name, skip, skip_routes, endpoints):
        context = {
            "package_name": self._parser.package_name,
            "folder_name": self._parser.folder_name,
            "controller_name": name.lower().replace("-", "_"),
            "skip_routes": skip_routes,
            "controller_endpoints": dict()
        }

        for item in endpoints:
            try:
                endpoint, method = item.split(":", maxsplit=1)
            except ValueError:
                endpoint, method = item, "get"

            context["controller_endpoints"][endpoint] = method

        self._log.debug("Cookiecutter context: {0}".format(context))

        cookiecutter(
            self.__class__.template,
            extra_context=context,
            output_dir=os.path.abspath(
                os.path.join(
                    self._parser.project_root,
                    "../",
                )
            ),
            no_input=True,
            overwrite_if_exists=True,
            skip_if_file_exists=skip,
        )

    def destroy(self, **kwargs):
        raise NotImplementedError
