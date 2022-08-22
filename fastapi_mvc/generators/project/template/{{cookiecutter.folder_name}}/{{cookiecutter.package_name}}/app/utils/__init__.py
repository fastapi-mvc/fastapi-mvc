"""Application implementation - utilities.

Resources:
    1. https://aioredis.readthedocs.io/en/latest/

"""
{%- if cookiecutter.redis == "yes" and cookiecutter.aiohttp == "yes" %}
from {{cookiecutter.package_name}}.app.utils.aiohttp_client import AiohttpClient
from {{cookiecutter.package_name}}.app.utils.redis import RedisClient


__all__ = ("AiohttpClient", "RedisClient")
{% elif cookiecutter.redis == "yes" %}
from {{cookiecutter.package_name}}.app.utils.redis import RedisClient


__all__ = ("RedisClient",)
{% elif cookiecutter.aiohttp == "yes" %}
from {{cookiecutter.package_name}}.app.utils.aiohttp_client import AiohttpClient


__all__ = ("AiohttpClient",)
{% else %}
{% endif %}