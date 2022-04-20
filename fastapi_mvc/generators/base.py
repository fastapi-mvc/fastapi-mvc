"""FastAPI MVC Generate abstract class implementation."""
from abc import ABCMeta, abstractmethod
import logging


class Generator(object, metaclass=ABCMeta):
    """Defines the common interface for all concrete generators.

    Attributes:
        name (str): (class attribute) A distinguishable generator name, that
            will be used in fastapi-mvc generate CLI command
        template (str): (class attribute)  Path to generator cookiecutter
            template directory.
        usage (str): (class attribute) Path to generator usage file.
        cli_arguments (list[dict]): (class attribute) Click arguments as kwargs,
            that will be available in dynamically generated command for this
            generator.
        cli_options (list[dict]): (class attribute) Click options as kwargs,
            that will be available in dynamically generated command for this
            generator.
        _log (logging.Logger): Logger class object instance.
        _parser (fastapi_mvc.parsers.IniParser): IniParser object instance
            for current fastapi-mvc project.

    """

    __slots__ = (
        "_log",
        "_parser",
    )

    name: str
    template: str
    usage: str
    category: str
    # Usage https://click.palletsprojects.com/en/8.1.x/api/?highlight=click%20argument#click.Argument
    cli_arguments = [
        {
            "param_decls": ["NAME"],
            "required": True,
            "nargs": 1,
        }
    ]
    # Usage https://click.palletsprojects.com/en/8.1.x/api/?highlight=click%20option#click.Option
    cli_options = [
        {
            "param_decls": ["-S", "--skip"],
            "is_flag": True,
            "help": "Skip files that already exist.",
        }
    ]

    def __init__(self, parser):
        """Initialize Generator base class object instance.

        Args:
            parser (fastapi_mvc.parsers.IniParser): IniParser object instance
                for current fastapi-mvc project.

        """
        self._log = logging.getLogger(self.__class__.__name__)
        self._parser = parser

    @abstractmethod
    def new(self, **kwargs):
        """New abstract method for all inheriting classes.

        Args:
            **kwargs(dict): Abstract methods kwargs.

        """
        pass

    @abstractmethod
    def destroy(self, **kwargs):
        """Destroy abstract method for all inheriting classes.

        Args:
            **kwargs(dict): Abstract methods kwargs.

        """
        pass
