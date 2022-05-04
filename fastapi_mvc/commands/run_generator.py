"""FastAPI MVC command RunGenerator class implementation.

The fastapi-mvc.commands submodule implements command design pattern:
https://refactoring.guru/design-patterns/command
"""
from fastapi_mvc.commands import Command


class RunGenerator(Command):
    """Defines the common interface for running any ``fastapi-mvc`` generator.

    Args:
        generator(Generator): Concrete Generator class object instance to
            invoke.
        options(dict): CLI options and arguments for the generator.

    Attributes:
        _log (logging.Logger): Logger class object instance.
        _generator (Generator): Generator subclass object instance.
        _options (dict): CLI options and arguments for the generator.

    """

    __slots__ = ("_generator", "_options")

    def __init__(self, generator, options):
        """Initialize RunGenerator class object instance."""
        Command.__init__(self)
        self._log.debug("Initialize RunGenerator class object instance.")
        self._generator = generator
        self._options = options

    def execute(self):
        """Execute RunGenerator command."""
        self._log.info("Running {0:s} generator".format(self._generator.name))
        self._generator.new(**self._options)
