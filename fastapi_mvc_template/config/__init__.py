# -*- coding: utf-8 -*-
"""FastAPI MVC template."""
from .application import DEBUG, PROJECT_NAME, VERSION, USE_REDIS
from .redis import (
    REDIS_HOST,
    REDIS_PORT,
    REDIS_USERNAME,
    REDIS_PASSWORD,
    REDIS_USE_SENTINEL,
)
from .router import router


__all__ = (
    DEBUG,
    PROJECT_NAME,
    VERSION,
    USE_REDIS,
    REDIS_HOST,
    REDIS_PORT,
    REDIS_USERNAME,
    REDIS_PASSWORD,
    REDIS_USE_SENTINEL,
    router
)
