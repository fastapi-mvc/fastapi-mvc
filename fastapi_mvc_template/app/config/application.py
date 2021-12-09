# -*- coding: utf-8 -*-
"""Application configuration."""
import os

from fastapi_mvc_template.version import __version__


# FastAPI logging level. You should disable this for production.
DEBUG = os.getenv("FASTAPI_DEBUG", True)
# FastAPI project name.
PROJECT_NAME = "fastapi_mvc_template"
VERSION = __version__
# Whether or not to use Redis.
USE_REDIS = os.getenv("FASTAPI_USE_REDIS", True)
# All your additional application configuration should go either here or in
# separate file in this submodule.
