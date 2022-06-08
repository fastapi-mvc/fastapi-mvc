"""Fastapi-mvc generators - abstract base class."""
from abc import ABCMeta, abstractmethod
import logging
import os

from click import Option, Argument


class Generator(object, metaclass=ABCMeta):
    """Define the common interface for all concrete generators.

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
        """Validate required class variables in a subclass."""
        super().__init_subclass__(**kwargs)

        if cls.name is NotImplemented:
            cls.name = cls.__name__
        if cls.template is NotImplemented:
            raise NotImplementedError(
                "Please implement the 'template' class variable."
            )

    @classmethod
    def read_usage(cls):
        """Return concrete generator USAGE file contents.

        Returns:
            str: Concrete generator USAGE file contents.

        """
        if cls.usage and os.path.isfile(cls.usage):
            with open(cls.usage, "r") as f:
                return f.read()

        return None

    @abstractmethod
    def new(self, **kwargs):
        """Define abstract new method for all inheriting classes.

        Args:
            **kwargs(dict): Abstract methods kwargs.

        """
        pass

    @abstractmethod
    def destroy(self, **kwargs):
        """Define abstract destroy method for all inheriting classes.

        Args:
            **kwargs(dict): Abstract methods kwargs.

        """
        pass
