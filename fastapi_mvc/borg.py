"""Borg design pattern (or monostate if you will) implementation."""
import os
import sys
import importlib.util
import pkgutil
import logging

from fastapi_mvc.commands import Invoker
from fastapi_mvc.parsers import IniParser
from fastapi_mvc.generators import (
    Generator,
    ControllerGenerator,
    GeneratorGenerator,
)
from fastapi_mvc.version import __version__


class Borg(object):
    """We are the Borg.

    Borg design pattern (or monostate if you will) implementation.

    It is a way to implement singleton behavior, but instead of having only one
    instance of a class, there are multiple instances that share the same state.
    In other words, the focus is on sharing state instead of sharing instance
    identity.

    Note:
        I am aware that singleton and monostate do not have a good reputation
        and are often considered an anti pattern. However, a little experiment
        never killed nobody :); I'm genuinely curious how this plays out.

        Besides, it has a cool name.

    Attributes:
        _log (logging.Logger): Logger class object instance.
        _invoker (Invoker): Invoker class object instance.
        _parser (IniParser): IniParser class object instance.
            installed.
        _generators (typing.Dict[str, Generator]): Dictionary containing all
            available fastapi-mvc generators.
        _import_paths (typing.Set[str]): Set containing paths from which try to
            import custom generators.
        _imported_paths (typing.FrozenSet[str]): FrozenSet containing already
            imported paths.

    Resources:
        1. http://www.aleax.it/5ep.html
        2. https://code.activestate.com/recipes/66531/

    """

    __shared_state = dict()

    def __init__(self):
        """I am the beginning, the end, the one who is many. I am the Borg."""
        self.__dict__ = self.__shared_state

        if not getattr(self, "__borg_assimilated", False):
            setattr(self, "__borg_assimilated", True)
            self._log = logging.getLogger(self.__class__.__name__)
            self._log.debug("Initialize first Borg class object instance.")
            self._invoker = Invoker()
            self._parser = None
            self._generators = {
                ControllerGenerator.name: ControllerGenerator,
                GeneratorGenerator.name: GeneratorGenerator,
            }
            self._import_paths = {os.path.join(os.getcwd(), "lib/generators")}
            self._imported_paths = frozenset()

    def __str__(self):
        """Class custom __str__ method implementation."""
        return "We are the Borg. You will be assimilated. Resistance is futile."

    @property
    def generators(self):
        """Get loaded fastapi-mvc generators.

        Returns:
            typing.Dict[str, Generator]: Loaded fastapi-mvc generators.

        """
        return self._generators

    @property
    def import_paths(self):
        """Get generators import paths.

        Returns:
            typing.Set[str]: generators import paths.

        """
        return self._import_paths

    @property
    def parser(self):
        """Get IniParser class object instance.

        Returns:
            IniParser: IniParser class object instance if set otherwise None.

        """
        return self._parser

    @property
    def poetry_path(self):
        """Get Poetry binary abspath.

        Returns:
            str: Poetry binary abspath.

        """
        return "{0:s}/bin/poetry".format(
            os.getenv("POETRY_HOME", "{0:s}/.poetry".format(os.getenv("HOME")))
        )

    @property
    def version(self):
        """Get fastapi-mvc version.

        Returns:
            str: Fastapi-mvc version.

        """
        return __version__

    def require_project(self):
        """Require valid fastapi-mvc project."""
        if self._parser:
            return

        try:
            parser = IniParser()
        except (FileNotFoundError, PermissionError, IsADirectoryError):
            self._log.error(
                "Not a fastapi-mvc project. Try 'fastapi-mvc new --help' for "
                "details how to create one."
            )
            raise SystemExit(1)

        pkg_path = os.path.join(parser.project_root, parser.package_name)

        if not os.path.isdir(pkg_path):
            self._log.debug("{0:s} is not a directory.".format(pkg_path))
            self._log.error(
                "Could not find required project files. Most likely project or "
                "fastapi-mvc.ini is corrupted."
            )
            raise SystemExit(1)

        self._parser = parser
        self._import_paths.add(
            os.path.join(
                self._parser.project_root,
                "lib/generators",
            )
        )

    def load_generators(self):
        """Load user fastapi-mvc generators.

        Programmatically import all available user generators from known paths
        to search in.

        References:
            1. Importing programmatically

        .. _Importing programmatically:
            https://docs.python.org/3/library/importlib.html#importing-programmatically

        """
        paths = self._import_paths.difference(self._imported_paths)

        for item in pkgutil.iter_modules(paths):
            m_path = os.path.join(
                item.module_finder.path,
                item.name,
                "__init__.py",
            )
            spec = importlib.util.spec_from_file_location(
                "fastapi_mvc_generators",
                m_path,
            )
            module = importlib.util.module_from_spec(spec)
            # Register module before running `exec_module()` to make all
            # submodules in it able to find their parent package:
            # `fastapi_mvc_generators`.
            # Otherwise, the following error will be raised:
            #     ModuleNotFoundError: No module named 'fastapi_mvc_generators'
            sys.modules[spec.name] = module
            try:
                spec.loader.exec_module(module)
            except (ModuleNotFoundError, ImportError) as err:
                self._log.error(
                    "Could not load custom generator: {}".format(m_path)
                )
                self._log.error(err)
                continue

            generator = getattr(module, "__all__", None)

            if generator and issubclass(generator, Generator):
                if generator.name in self._generators:
                    generator.name = generator.__name__

                self._generators[generator.name] = generator

        self._imported_paths = self._imported_paths.union(self._import_paths)

    def enqueue(self, command):
        """Enqueue command for Invoker to execute.

        Args:
            command (Command): Command subclass object instance.

        """
        self._invoker.enqueue(command)

    def execute(self):
        """Execute enqueued Invoker commands."""
        self._invoker.execute()
