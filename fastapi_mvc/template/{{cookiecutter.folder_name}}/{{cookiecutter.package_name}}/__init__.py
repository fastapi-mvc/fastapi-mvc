# -*- coding: utf-8 -*-
"""{{cookiecutter.project_description}}"""
import logging

from .version import __version__  # noqa: F401

# initialize logging
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())
