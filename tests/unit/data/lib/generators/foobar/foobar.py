"""FastAPI MVC foobar generator implementation."""
import os

from cookiecutter.main import cookiecutter
from fastapi_mvc.generators import Generator


class FoobarGenerator(Generator):
    """Foobar generator implementation.

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
        category (str): (class variable) Name under which generator should be
            printed in ``fastapi-mvc generate`` CLI command help page.
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

    # In this case, slots apart from standard behavior, also ensure that class
    # variables available in object instances as object attributes are
    # read-only. They define generator CLI and cookie-cutter template and thus
    # by principle should be immutable at RunTime.
    # However, if the need arises you can still edit them should you choose.
    # To do so either remove `__slots__` or access via `__class__` magic method.
    # Removing __slots__ will make class variables default values for object
    # attributes. Editing one from the object instance will not change the value
    # of the class variable or the value in another object. Is, the other way
    # round when accessing via `__class__` magic method ex. self.__class__.name.
    # Not only it will change a class variable value, but also a object
    # attribute value for all objects created from this class. Provided, class
    # is one entry in memory. For instance, if you would deep clone it, the
    # above would only apply for the class in which the change was made. Not
    # that this is super important, because I do not see a use case where there
    # would be ever two generator class object instances. But I want you to
    # understand the difference. Who knows maybe it will be useful.
    __slots__ = ("_parser",)

    name = "foobar"
    template = os.path.abspath(
        os.path.join(
            os.path.abspath(__file__),
            "../template",
        )
    )
    category = "MyGenerators"
    usage = os.path.join(template, "USAGE")

    def __init__(self, parser):
        """Initialize FoobarGenerator class object instance."""
        Generator.__init__(self)
        self._parser = parser

    def new(self, name, skip):
        """Generate a new foobar.

        Hint:
            Kwargs passed to this method are from generator CLI options and
            arguments. Since this generator does not override base class
            cli_options and cli_arguments class variables, defaults are used.
            Documentation for generators feature will be added soon; issue:
            https://github.com/rszamszur/fastapi-mvc/issues/75

        Args:
            name (str): Given generator name.
            skip (bool): If True skip the files in the corresponding directories
                if they already exist.

        """
        context = {
            "package_name": self._parser.package_name,
            "folder_name": self._parser.folder_name,
            "foobar_name": name,
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
            skip_if_file_exists=skip,
        )

    def destroy(self, **kwargs):
        """Not yet implemented.

        Args:
            **kwargs(dict): Abstract methods kwargs.

        """
        raise NotImplementedError
