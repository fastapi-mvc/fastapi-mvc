"""Command design pattern - run generator command."""
from fastapi_mvc.commands import Command


class RunGenerator(Command):
    """Define the common interface for running any ``fastapi-mvc`` generator.

    Args:
        generator (Generator): Concrete Generator class object instance to
            invoke.
        options (typing.Dict[str, typing.Any]): Map of generator CLI option and
            argument names to their parsed values.

    Attributes:
        _generator (Generator): Generator subclass object instance.
        _options (typing.Dict[str, typing.Any]): Map of generator CLI option and
            argument names to their parsed values.

    """

    __slots__ = ("_generator", "_options")

    def __init__(self, generator, options):
        """Initialize RunGenerator class object instance."""
        Command.__init__(self)
        self._log.debug("Initialize RunGenerator class object instance.")
        self._generator = generator
        self._options = options

    def execute(self):
        """Execute generator new method."""
        self._log.info("Running generator: {0:s}".format(self._generator.name))
        self._generator.new(**self._options)
