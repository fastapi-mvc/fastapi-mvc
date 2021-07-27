# -*- coding: utf-8 -*-
"""Redis configuration."""
import os


REDIS_HOST = os.getenv('FASTAPI_REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('FASTAPI_REDIS_PORT', 6379))
REDIS_USERNAME = os.getenv('FASTAPI_REDIS_USERNAME', None)
REDIS_PASSWORD = os.getenv('FASTAPI_REDIS_PASSWORD', None)
# If provided above Redis config is for Sentinel.
REDIS_USE_SENTINEL = bool(os.getenv('FASTAPI_REDIS_USE_SENTINEL', False))
