# -*- coding: utf-8 -*-
"""FastAPI MVC template."""
from .aiohttp_client import AiohttpClient
from .redis import RedisClient

__all__ = (
    AiohttpClient,
    RedisClient,
)
