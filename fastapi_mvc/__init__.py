"""fastapi-mvc."""
import logging

from fastapi_mvc.core import (
    ANSWERS_FILE,
    VERSION,
    Command,
    Generator,
    GeneratorsMultiCommand,
)

# initialize logging
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


__all__ = (
    "ANSWERS_FILE",
    "VERSION",
    "Command",
    "Generator",
    "GeneratorsMultiCommand",
)
