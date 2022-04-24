"""FastAPI MVC generator generator implementation."""
import os
import sys

from cookiecutter.main import cookiecutter
from fastapi_mvc.generators import Generator


class GeneratorGenerator(Generator):
    """Generator generator implementation.

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
        _builtins (typing.List[str]): List of builtins generator names.

    """

    __slots__ = "_builtins"

    name = "generator"
    template = os.path.abspath(
        os.path.join(
            os.path.abspath(__file__),
            "../template",
        )
    )
    usage = os.path.join(template, "USAGE")
    category = "Builtins"

    def __init__(self, parser):
        """Initialize GeneratorGenerator class object instance."""
        Generator.__init__(self, parser)
        self._builtins = ["controller", "generator"]

    def new(self, name, skip):
        """Generate a new generator.

        Args:
            name (str): Given generator name.
            skip (bool): If True skip the files in the corresponding directories
                if they already exist.

        """
        if name in self._builtins:
            self._log.error("Shadows built-in generator: {0:s}".format(name))
            sys.exit(1)

        words = name.replace("-", " ").replace("_", " ").split()
        class_name = "".join(w.capitalize() for w in words)

        context = {
            "package_name": self._parser.package_name,
            "folder_name": self._parser.folder_name,
            "generator_name": name.lower().replace("-", "_"),
            "class_name": "{0:s}Generator".format(class_name),
        }

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
