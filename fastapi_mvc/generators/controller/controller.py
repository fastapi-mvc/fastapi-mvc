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

    def __init__(self, parser, project_root):
        Generator.__init__(self, parser, project_root)

    def new(self, name, skip, skip_routes, endpoints):
        self._context["controller_name"] = name
        self._context["controller_endpoints"] = dict()
        self._context["skip_routes"] = skip_routes

        for item in endpoints:
            try:
                endpoint, method = item.split(":", maxsplit=1)
            except ValueError:
                endpoint, method = item, "get"

            self._context["controller_endpoints"][endpoint] = method

        self._log.debug("Cookiecutter context: {0}".format(self._context))

        cookiecutter(
            self.__class__.template,
            extra_context=self._context,
            output_dir=os.path.abspath(
                os.path.join(
                    self._project_root,
                    "../",
                )
            ),
            no_input=True,
            overwrite_if_exists=True,
            skip_if_file_exists=skip,
        )

    def destroy(self, **kwargs):
        raise NotImplementedError
