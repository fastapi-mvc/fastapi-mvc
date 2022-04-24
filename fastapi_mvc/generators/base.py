"""FastAPI MVC Generator abstract class implementation."""
from abc import ABCMeta, abstractmethod
import logging


class Generator(object, metaclass=ABCMeta):
    """Defines the common interface for all concrete generators.

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

    __slots__ = (
        "_log",
        "_parser",
    )

    name: str
    template: str
    usage: str
    category: str
    cli_arguments = [
        {
            "param_decls": ["NAME"],
            "required": True,
            "nargs": 1,
        }
    ]
    cli_options = [
        {
            "param_decls": ["-S", "--skip"],
            "is_flag": True,
            "help": "Skip files that already exist.",
        }
    ]

    def __init__(self, parser):
        """Initialize Generator base class object instance."""
        self._log = logging.getLogger(self.__class__.__name__)
        self._parser = parser

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
