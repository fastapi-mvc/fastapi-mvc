# -*- coding: utf-8 -*-
"""FastAPI MVC template."""
import logging

from .version import __version__

# initialize logging
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())
