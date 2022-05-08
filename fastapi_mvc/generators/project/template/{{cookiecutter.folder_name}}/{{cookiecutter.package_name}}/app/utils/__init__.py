"""Application implementation - utilities.

Resources:
    1. https://aioredis.readthedocs.io/en/latest/

"""
{%- if cookiecutter.aiohttp == "yes" %}
from .aiohttp_client import AiohttpClient
{%- endif %}
{%- if cookiecutter.redis == "yes" %}
from .redis import RedisClient
{%- endif %}

__all__ = (
    {%- if cookiecutter.aiohttp == "yes" %}
    AiohttpClient,
    {%- endif %}
    {%- if cookiecutter.redis == "yes" %}
    RedisClient,
    {%- endif %}
)
