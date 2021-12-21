# -*- coding: utf-8 -*-
"""fastapi-mvc."""
from .application import settings
from .redis import redis
from .router import router


__all__ = (
    settings,
    redis,
    router,
)
