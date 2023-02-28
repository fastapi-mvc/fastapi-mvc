"""fastapi-mvc."""
import logging

from fastapi_mvc.core import (
    ClickAliasedGroup,
    Command,
    Generator,
    GeneratorsMultiCommand,
)

# initialize logging
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


__all__ = (
    "ClickAliasedGroup",
    "Command",
    "Generator",
    "GeneratorsMultiCommand",
)
