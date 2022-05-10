"""Application implementation - ASGI."""
import logging

from fastapi import FastAPI
from {{cookiecutter.package_name}}.config import settings
from {{cookiecutter.package_name}}.app.router import root_api_router
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
    """Define FastAPI startup event handler.

    Resources:
        1. https://fastapi.tiangolo.com/advanced/events/#startup-event

    """
    log.debug("Execute FastAPI startup event handler.")
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
    """Define FastAPI shutdown event handler.

    Resources:
        1. https://fastapi.tiangolo.com/advanced/events/#shutdown-event

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


def get_application():
    """Initialize FastAPI application.

    Returns:
       FastAPI: Application object instance.

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
    app.include_router(root_api_router)
    log.debug("Register global exception handler for custom HTTPException.")
    app.add_exception_handler(HTTPException, http_exception_handler)

    return app
