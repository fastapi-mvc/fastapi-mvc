API
===

This part of the documentation lists the full API reference of all classes and functions.

WSGI
----

.. autoclass:: {{cookiecutter.package_name}}.wsgi.ApplicationLoader
   :members:
   :show-inheritance:

Config
------

.. automodule:: {{cookiecutter.package_name}}.config

.. autoclass:: {{cookiecutter.package_name}}.config.application.Application
   :members:
   :show-inheritance:

.. autoclass:: {{cookiecutter.package_name}}.config.redis.Redis
   :members:
   :show-inheritance:

.. automodule:: {{cookiecutter.package_name}}.config.gunicorn

CLI
---

.. automodule:: {{cookiecutter.package_name}}.cli

.. autofunction:: {{cookiecutter.package_name}}.cli.cli.cli

.. autofunction:: {{cookiecutter.package_name}}.cli.utils.validate_directory

.. autofunction:: {{cookiecutter.package_name}}.cli.serve.serve

App
---

.. automodule:: {{cookiecutter.package_name}}.app

.. autofunction:: {{cookiecutter.package_name}}.app.asgi.on_startup

.. autofunction:: {{cookiecutter.package_name}}.app.asgi.on_shutdown

.. autofunction:: {{cookiecutter.package_name}}.app.asgi.get_application

.. automodule:: {{cookiecutter.package_name}}.app.router

Controllers
~~~~~~~~~~~

.. automodule:: {{cookiecutter.package_name}}.app.controllers

.. autofunction:: {{cookiecutter.package_name}}.app.controllers.ready.readiness_check

Models
~~~~~~

.. automodule:: {{cookiecutter.package_name}}.app.models

Views
~~~~~

.. automodule:: {{cookiecutter.package_name}}.app.views

.. autoclass:: {{cookiecutter.package_name}}.app.views.error.ErrorModel
   :members:
   :show-inheritance:

.. autoclass:: {{cookiecutter.package_name}}.app.views.error.ErrorResponse
   :members:
   :show-inheritance:

Exceptions
~~~~~~~~~~

.. automodule:: {{cookiecutter.package_name}}.app.exceptions

.. autoclass:: {{cookiecutter.package_name}}.app.exceptions.http.HTTPException
   :members:
   :show-inheritance:

.. autofunction:: {{cookiecutter.package_name}}.app.exceptions.http.http_exception_handler

Utils
~~~~~

.. automodule:: {{cookiecutter.package_name}}.app.utils

.. autoclass:: {{cookiecutter.package_name}}.app.utils.aiohttp_client.AiohttpClient
   :members:
   :show-inheritance:

.. autoclass:: {{cookiecutter.package_name}}.app.utils.redis.RedisClient
   :members:
   :show-inheritance:
