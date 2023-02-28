"""Fastapi-mvc constants.

Attributes:
    VERSION (str): Fastapi-mvc version.
    ANSWERS_FILE (str): Relative path to copier answers file.

"""
from collections import namedtuple


_Template = namedtuple("Template", "template vcs_ref")

VERSION = "0.26.0"
ANSWERS_FILE = ".fastapi-mvc.yml"
COPIER_PROJECT = _Template("https://github.com/fastapi-mvc/copier-project.git", "0.4.0")
COPIER_CONTROLLER = _Template("https://github.com/fastapi-mvc/copier-controller.git", "0.2.1")
COPIER_GENERATOR = _Template("https://github.com/fastapi-mvc/copier-generator.git", "0.2.0")
COPIER_SCRIPT = _Template("https://github.com/fastapi-mvc/copier-script.git", "0.1.1")
