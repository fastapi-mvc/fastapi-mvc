# -*- coding: utf-8 -*-
"""Application Asynchronous Server Gateway Interface."""
import logging

from fastapi import FastAPI
from fastapi_mvc_template.config import (
    DEBUG,
    PROJECT_NAME,
    VERSION,
    USE_REDIS,
    router,
)
from fastapi_mvc_template.app.utils import RedisClient, AiohttpClient
from fastapi_mvc_template.app.exceptions import (
    HTTPException,
    http_exception_handler,
)

log = logging.getLogger(__name__)


async def on_startup():
    """Fastapi startup event handler.

    Creates RedisClient and AiohttpClient session.

    """
    log.debug("Execute FastAPI startup event handler.")
    # Initialize utilities for whole FastAPI application without passing object
    # instances within the logic. Feel free to disable it if you don't need it.
    if USE_REDIS:
        RedisClient.open_redis_client()

    AiohttpClient.get_aiohttp_client()


async def on_shutdown():
    """Fastapi shutdown event handler.

    Destroys RedisClient and AiohttpClient session.

    """
    log.debug("Execute FastAPI shutdown event handler.")
    # Gracefully close utilities.
    if USE_REDIS:
        await RedisClient.close_redis_client()

    await AiohttpClient.close_aiohttp_client()


def get_app():
    """Initialize FastAPI application.

    Returns:
        app (FastAPI): Application object instance.

    """
    log.debug("Initialize FastAPI application node.")
    app = FastAPI(
        title=PROJECT_NAME,
        debug=DEBUG,
        version=VERSION,
        docs_url="/",
        on_startup=[on_startup],
        on_shutdown=[on_shutdown],
    )
    log.debug("Add application routes.")
    app.include_router(router)
    # Register global exception handler for custom HTTPException.
    app.add_exception_handler(HTTPException, http_exception_handler)

    return app


application = get_app()
