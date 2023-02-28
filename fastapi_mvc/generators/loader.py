"""Fastapi-mvc generators - controller generator.

Attributes:
    log (logging.Logger): Logger class object instance.

"""
from typing import Dict, TYPE_CHECKING
from importlib.util import spec_from_file_location, module_from_spec
import logging
import pkgutil
import sys
import os

from .controller import controller
from .generator import generator
from .script import script


if TYPE_CHECKING:
    import click


log = logging.getLogger(__name__)


def load_generators() -> Dict[str, click.Command]:
    """Load user fastapi-mvc generators.

    Programmatically import all available user generators from known paths to search in.

    References:
        1. Importing programmatically

    .. _Importing programmatically:
        https://docs.python.org/3/library/importlib.html#importing-programmatically

    """
    unique = {controller, generator, script}
    paths = [os.path.join(os.getcwd(), "lib/generators")]

    for p in os.getenv("FMVC_PATH", "").split(":"):
        if os.path.exists(p) and os.access(p, os.R_OK):
            paths.append(p)

    for item in pkgutil.iter_modules(paths):
        m_path = os.path.join(
            item.module_finder.path,  # type: ignore
            item.name,
            "__init__.py",
        )
        spec = spec_from_file_location(
            "fastapi_mvc_generators",
            m_path,
        )

        if not spec:
            continue

        module = module_from_spec(spec)
        # Register module before running `exec_module()` to make all
        # submodules in it able to find their parent package:
        # `fastapi_mvc_generators`.
        # Otherwise, the following error will be raised:
        #     ModuleNotFoundError: No module named 'fastapi_mvc_generators'
        sys.modules[spec.name] = module
        try:
            spec.loader.exec_module(module)  # type: ignore
        except (ModuleNotFoundError, ImportError) as err:
            log.error(f"Could not load custom generator: {m_path}")
            log.error(err)
            continue

        imported = getattr(module, "generator", None)

        if imported:
            unique.add(imported)

    return {str(item.name): item for item in unique}
