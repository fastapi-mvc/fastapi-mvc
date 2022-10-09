"""Fastapi-mvc generators - controller generator.

Attributes:
    log (logging.Logger): Logger class object instance.

"""
import importlib
import logging
import pkgutil
import sys
import os

from .controller import controller
from .generator import generator


log = logging.getLogger(__name__)


def load_generators():
    """Load user fastapi-mvc generators.

    Programmatically import all available user generators from known paths to search in.

    References:
        1. Importing programmatically

    .. _Importing programmatically:
        https://docs.python.org/3/library/importlib.html#importing-programmatically

    """
    paths = [os.path.join(os.getcwd(), "lib/generators")]
    unique = {controller, generator}

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
            log.error(f"Could not load custom generator: {m_path}")
            log.error(err)
            continue

        imported = getattr(module, "generator", None)

        if imported:
            unique.add(imported)

    return {item.name: item for item in unique}
