"""FastAPI dynamic loader."""
import sys
import os
import importlib.util
import pkgutil

from fastapi_mvc.generators import Generator


def load_generators(paths):
    """Load user fastapi-mvc generators from provided paths.

    At given fastapi-mvc project root programmatically import all available user
    generators.

    Args:
        paths (typing.List[str]): List of paths from which try to load custom
            fastapi-mvc generators.

    Returns:
        typing.Dict[str, Generator]: Loaded fastapi-mvc generator classes.

    References:
        1. Importing programmatically

    .. _Importing programmatically:
        https://docs.python.org/3/library/importlib.html#importing-programmatically

    """
    generators = dict()

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
        # Register module before running `exec_module()` to make all submodules
        # in it able to find their parent package: `fastapi_mvc_generators`.
        # Otherwise, we will got the following error:
        #     `ModuleNotFoundError: No module named 'fastapi_mvc_generators'`
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)

        generator = getattr(module, "__all__")

        if issubclass(generator, Generator):
            generators[generator.name] = generator

    return generators
