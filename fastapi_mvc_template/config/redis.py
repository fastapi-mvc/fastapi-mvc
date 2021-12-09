# -*- coding: utf-8 -*-
"""Redis configuration."""
from pydantic import BaseSettings


class Redis(BaseSettings):
    REDIS_HOST: str = "127.0.0.1"
    REDIS_PORT: int = 6379
    REDIS_USERNAME: str = None
    REDIS_PASSWORD: str = None
    # If provided above Redis config is for Sentinel.
    REDIS_USE_SENTINEL: bool = False

    class Config:
        case_sensitive = True
        env_prefix = "FASTAPI_"


redis = Redis()
