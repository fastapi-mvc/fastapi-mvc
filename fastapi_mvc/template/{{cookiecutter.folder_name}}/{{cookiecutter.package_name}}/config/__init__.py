# -*- coding: utf-8 -*-
"""{{cookiecutter.project_description}}"""
from .application import settings
{%- if cookiecutter.redis == "yes" %}
from .redis import redis
{%- endif %}
from .router import router


__all__ = (
    settings,
    {%- if cookiecutter.redis == "yes" %}
    redis,
    {%- endif %}
    router,
)
