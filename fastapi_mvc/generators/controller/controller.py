"""FastAPI MVC controller generator implementation."""
import os

from cookiecutter.main import cookiecutter
from fastapi_mvc.generators import Generator


class ControllerGenerator(Generator):
    """Controller generator implementation.

    Args:
        parser (IniParser): IniParser object instance of a fastapi-mvc project.

    Attributes:
        name (str): (class attribute) A distinguishable generator name, that
            will be used in fastapi-mvc generate CLI command
        template (str): (class attribute)  Path to generator cookiecutter
            template directory.
        usage (str): (class attribute) Path to generator usage file.
        category (str): (class attribute) Name under which generator should be
            displayed in CLI help.
        cli_arguments (typing.List[dict]): (class attribute) Click arguments as
            kwargs, that will be available in dynamically generated command for
            this generator.
        cli_options (typing.List[dict]): (class attribute) Click options as
            kwargs, that will be available in dynamically generated command for
            this generator.
        _log (logging.Logger): Logger class object instance.
        _parser (IniParser): IniParser object instance
            for current fastapi-mvc project.

    """

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
        },
    ]
    cli_options = [
        *Generator.cli_options,
        {
            "param_decls": ["-R", "--skip-routes"],
            "is_flag": True,
            "help": "Weather to skip routes entry",
        },
    ]

    def __init__(self, parser):
        """Initialize ControllerGenerator class object instance."""
        Generator.__init__(self, parser)

    def new(self, name, skip, skip_routes, endpoints):
        """Generate a new controller.

        Args:
            name (str): Given controller name.
            skip (bool): If True skip the files in the corresponding directories
                if they already exist.
            skip_routes (bool): If True do not edit `config/router.py`.
            endpoints (list): List of controller endpoints to create.

        """
        context = {
            "package_name": self._parser.package_name,
            "folder_name": self._parser.folder_name,
            "controller_name": name.lower().replace("-", "_"),
            "skip_routes": skip_routes,
            "controller_endpoints": dict(),
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
        """Not yet implemented.

        Args:
            **kwargs(dict): Abstract methods kwargs.

        """
        raise NotImplementedError
