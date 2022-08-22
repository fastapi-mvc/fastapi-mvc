"""fastapi-mvc."""
import logging

from .version import __version__
from .borg import Borg


# initialize logging
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


__all__ = ("Borg", "__version__")
