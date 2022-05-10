"""Application implementation - utilities.

Resources:
    1. https://aioredis.readthedocs.io/en/latest/

"""
{%- if cookiecutter.aiohttp == "yes" %}
from {{cookiecutter.package_name}}.app.utils.aiohttp_client import AiohttpClient
{%- endif %}
{%- if cookiecutter.redis == "yes" %}
from {{cookiecutter.package_name}}.app.utils.redis import RedisClient
{%- endif %}
