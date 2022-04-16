from abc import ABCMeta, abstractmethod
import logging


class Generator(object, metaclass=ABCMeta):
    """Defines the common interface for all concrete generators."""

    __slots__ = (
        "_log",
        "_parser",
        "_project_root",
        "_context",
    )

    name: str
    template: str
    usage: str
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

    def __init__(self, parser, project_root):
        """Initialize Command base class object instance."""
        self._log = logging.getLogger(self.__class__.__name__)
        self._parser = parser
        self._project_root = project_root
        self._context = {
            "package_name": self._parser.package_name,
            "folder_name": self._parser.folder_name,
        }

    @abstractmethod
    def new(self, **kwargs):
        """New abstract method for all inheriting classes."""
        pass

    @abstractmethod
    def destroy(self, **kwargs):
        """Destroy abstract method for all inheriting classes."""
        pass
