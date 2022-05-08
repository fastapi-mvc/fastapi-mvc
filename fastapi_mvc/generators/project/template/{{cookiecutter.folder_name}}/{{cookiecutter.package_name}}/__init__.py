"""This project was generated with fastapi-mvc."""
import logging

from {{cookiecutter.package_name}}.version import __version__  # noqa: F401

# initialize logging
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())
