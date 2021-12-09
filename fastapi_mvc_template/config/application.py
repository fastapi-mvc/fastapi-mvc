# -*- coding: utf-8 -*-
"""Application configuration."""
from pydantic import BaseSettings
from fastapi_mvc_template.version import __version__


class Application(BaseSettings):
    # FastAPI logging level. You should disable this for production.
    DEBUG: bool = True
    # FastAPI project name.
    PROJECT_NAME: str = "fastapi_mvc_template"
    VERSION: str = __version__
    DOCS_URL: str = "/"
    # Whether or not to use Redis.
    USE_REDIS: bool = False
    # All your additional application configuration should go either here or in
    # separate file in this submodule.

    class Config:
        case_sensitive = True
        env_prefix = "FASTAPI_"


settings = Application()
