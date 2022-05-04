"""FastAPI MVC Generator abstract class implementation."""
from abc import ABCMeta, abstractmethod
import logging
import os

from click import Option, Argument


class Generator(object, metaclass=ABCMeta):
    """Defines the common interface for all concrete generators.

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
        cli_arguments (typing.List[click.Argument]): **(class variable)** Click
            arguments to register with this generator CLI command.
        cli_options (typing.List[click.Option]): **(class variable)** Click
            options to register with this generator CLI command.
        cli_help (typing.Optional[str]): **(class variable)** The help string to
            use for this generator CLI command.
        cli_short_help (typing.Optional[str]): **(class variable)** The short
            help to use for this generator CLI command. This is shown on the
            command listing of ``fastapi-mvc generate`` command.
        cli_deprecated (bool): **(class variable)** Issues a message indicating
            that the generator CLI command is deprecated.
        _log (logging.Logger): Logger class object instance.

    Resources:
        1. `Click Arguments`_
        2. `Click Options`_

    .. _Click Arguments:
        https://click.palletsprojects.com/en/8.1.x/arguments/

    .. _Click Options:
        https://click.palletsprojects.com/en/8.1.x/options/

    """

    __slots__ = ("_log",)

    name: str = NotImplemented
    template: str = NotImplemented
    usage: str = None
    category: str = "Other"
    cli_arguments = [
        Argument(
            param_decls=["NAME"],
            required=True,
            nargs=1,
        ),
    ]
    cli_options = [
        Option(
            param_decls=["-S", "--skip"],
            help="Skip files that already exist.",
            is_flag=True,
        ),
    ]
    cli_help = None
    cli_short_help = None
    cli_deprecated = False

    def __init__(self):
        """Initialize Generator base class object instance."""
        self._log = logging.getLogger(self.__class__.__name__)

    def __init_subclass__(cls, **kwargs):
        """Validate presence of required class variables in a subclass."""
        super().__init_subclass__(**kwargs)

        if cls.name is NotImplemented:
            cls.name = cls.__name__
        if cls.template is NotImplemented:
            raise NotImplementedError(
                "Please implement the 'template' class variable."
            )

    @classmethod
    def read_usage(cls):
        """Read and return concrete generator USAGE file contents.

        Returns:
            str: Concrete generator USAGE file contents.

        """
        if cls.usage and os.path.isfile(cls.usage):
            with open(cls.usage, "r") as f:
                return f.read()

        return None

    @abstractmethod
    def new(self, **kwargs):
        """Abstract method new for all inheriting classes.

        Args:
            **kwargs(dict): Abstract methods kwargs.

        """
        pass

    @abstractmethod
    def destroy(self, **kwargs):
        """Abstract method destroy for all inheriting classes.

        Args:
            **kwargs(dict): Abstract methods kwargs.

        """
        pass
