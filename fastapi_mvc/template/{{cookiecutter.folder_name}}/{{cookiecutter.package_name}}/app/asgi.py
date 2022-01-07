# -*- coding: utf-8 -*-
"""Application Asynchronous Server Gateway Interface."""
import logging

from fastapi import FastAPI
from {{cookiecutter.package_name}}.config import router, settings
{%- if cookiecutter.redis == "yes" and cookiecutter.aiohttp == "yes" %}
from {{cookiecutter.package_name}}.app.utils import RedisClient, AiohttpClient
{%- elif cookiecutter.redis == "yes" %}
from {{cookiecutter.package_name}}.app.utils import RedisClient
{%- elif cookiecutter.aiohttp == "yes" %}
from {{cookiecutter.package_name}}.app.utils import AiohttpClient
{%- endif %}
from {{cookiecutter.package_name}}.app.exceptions import (
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
    # instances within the logic.
    {%- if cookiecutter.redis == "yes" and cookiecutter.aiohttp == "yes" %}
    if settings.USE_REDIS:
        await RedisClient.open_redis_client()

    AiohttpClient.get_aiohttp_client()
    {%- elif cookiecutter.redis == "yes" %}
    if settings.USE_REDIS:
        await RedisClient.open_redis_client()
    {%- elif cookiecutter.aiohttp == "yes" %}
    AiohttpClient.get_aiohttp_client()
    {%- else %}
    pass
    {%- endif %}


async def on_shutdown():
    """Fastapi shutdown event handler.

    Destroys RedisClient and AiohttpClient session.

    """
    log.debug("Execute FastAPI shutdown event handler.")
    # Gracefully close utilities.
    {%- if cookiecutter.redis == "yes" and cookiecutter.aiohttp == "yes" %}
    if settings.USE_REDIS:
        await RedisClient.close_redis_client()

    await AiohttpClient.close_aiohttp_client()
    {%- elif cookiecutter.redis == "yes" %}
    if settings.USE_REDIS:
        await RedisClient.close_redis_client()
    {%- elif cookiecutter.aiohttp == "yes" %}
    await AiohttpClient.close_aiohttp_client()
    {%- else %}
    pass
    {%- endif %}


def get_app():
    """Initialize FastAPI application.

    Returns:
        app (FastAPI): Application object instance.

    """
    log.debug("Initialize FastAPI application node.")
    app = FastAPI(
        title=settings.PROJECT_NAME,
        debug=settings.DEBUG,
        version=settings.VERSION,
        docs_url=settings.DOCS_URL,
        on_startup=[on_startup],
        on_shutdown=[on_shutdown],
    )
    log.debug("Add application routes.")
    app.include_router(router)
    # Register global exception handler for custom HTTPException.
    app.add_exception_handler(HTTPException, http_exception_handler)

    return app


application = get_app()
