# -*- coding: utf-8 -*-
"""FastAPI MVC template."""
from .application import settings
from .redis import redis
from .router import router


__all__ = (
    settings,
    redis,
    router,
)
