# -*- coding: utf-8 -*-
"""Application configuration."""
from pydantic import BaseSettings
from {{cookiecutter.package_name}}.version import __version__


class Application(BaseSettings):
    """Application configuration model definition.

    Constructor will attempt to determine the values of any fields not passed
    as keyword arguments by reading from the environment. Default values will
    still be used if the matching environment variable is not set.

    Environment variables:
        FASTAPI_DEBUG
        FASTAPI_PROJECT_NAME
        FASTAPI_VERSION
        FASTAPI_DOCS_URL
        FASTAPI_USE_REDIS

    Attributes:
        DEBUG(bool): FastAPI logging level. You should disable this for
            production.
        PROJECT_NAME(str): FastAPI project name.
        VERSION(str): Application version.
        DOCS_URL(str): Path where swagger ui will be served at.
        USE_REDIS(bool): Whether or not to use Redis.

    """

    DEBUG: bool = True
    PROJECT_NAME: str = "{{cookiecutter.project_name}}"
    VERSION: str = __version__
    DOCS_URL: str = "/"
    USE_REDIS: bool = False
    # All your additional application configuration should go either here or in
    # separate file in this submodule.

    class Config:
        """Config sub-class needed to customize BaseSettings settings.

        More details can be found in pydantic documentation:
        https://pydantic-docs.helpmanual.io/usage/settings/

        """

        case_sensitive = True
        env_prefix = "FASTAPI_"


settings = Application()
