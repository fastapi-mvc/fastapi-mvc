"""FastAPI MVC {{cookiecutter.generator_name}} generator implementation."""
import os

from cookiecutter.main import cookiecutter
from fastapi_mvc.generators import Generator


class {{cookiecutter.class_name}}(Generator):
    """{{cookiecutter.generator_name.capitalize().replace('_', ' ')}} generator implementation.

    Args:
        parser (IniParser): IniParser object instance of a fastapi-mvc project.

    Attributes:
        name (str): **(class variable)** A distinguishable generator name, that
            will be used as subcommand for ``fastapi-mvc generate`` CLI command.
        template (str): **(class variable)**  Path to generator cookiecutter
            template root directory.
        usage (typing.Optional[str]): **(class variable)** Path to generator
            usage file, that will be printed at the end of its CLI command help
            page.
        category (str): **(class variable)** Name under which generator should
            be printed in ``fastapi-mvc generate`` CLI command help page.
        _log (logging.Logger): Logger class object instance.
        _parser (IniParser): IniParser object instance for current fastapi-mvc
            project.

    Resources:
        1. `Click Arguments`_
        2. `Click Options`_
        3. `Cookiecutter Docs`_

    .. _Click Arguments:
        https://click.palletsprojects.com/en/8.1.x/arguments/

    .. _Click Options:
        https://click.palletsprojects.com/en/8.1.x/options/

    .. _Cookiecutter Docs:
        https://cookiecutter.readthedocs.io/en/1.7.2/

    """

    __slots__ = ("_parser",)

    name = "{{cookiecutter.generator_name}}"
    template = os.path.abspath(
        os.path.join(
            os.path.abspath(__file__),
            "../template",
        )
    )
    category = "MyGenerators"
    usage = os.path.join(template, "USAGE")

    def __init__(self, parser):
        """Initialize {{cookiecutter.class_name}} class object instance."""
        Generator.__init__(self)
        self._parser = parser

    def new(self, name, skip):
        """Generate a new {{cookiecutter.generator_name.replace('_', ' ')}}.

        Hint:
            Kwargs passed to this method are from generator CLI options and
            arguments. Since this generator does not override base class
            cli_options and cli_arguments class variables, defaults are used.

        Args:
            name (str): Given CLI argument - name.
            skip (bool): If True skip the files in the corresponding directories
                if they already exist.

        """
        context = {
            "package_name": self._parser.package_name,
            "folder_name": self._parser.folder_name,
            "{{cookiecutter.generator_name}}_name": name,
        }

        self._log.debug("Cookiecutter context: {0}".format(context))

        cookiecutter(
            self.template,
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
