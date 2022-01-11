# -*- coding: utf-8 -*-
"""{{cookiecutter.project_description}}"""
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
