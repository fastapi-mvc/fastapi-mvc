:tocdepth: 2
API
===

This part of the documentation lists the full API reference of all classes and functions.

Core
----

.. autoclass:: fastapi_mvc.Command
   :members:
   :show-inheritance:

.. autoclass:: fastapi_mvc.Generator
   :members:
   :show-inheritance:

.. autoclass:: fastapi_mvc.GeneratorsMultiCommand
   :members:
   :show-inheritance:

Generators
----------

.. automodule:: fastapi_mvc.generators

.. autofunction:: fastapi_mvc.generators.controller

.. autofunction:: fastapi_mvc.generators.generator

.. autofunction:: fastapi_mvc.generators.load_generators

CLI
---

.. automodule:: fastapi_mvc.cli

.. autofunction:: fastapi_mvc.cli.cli.cli

.. autofunction:: fastapi_mvc.cli.run.run

.. autofunction:: fastapi_mvc.cli.new.new

.. autofunction:: fastapi_mvc.cli.generate.get_generate_cmd

Utils
-----

.. automodule:: fastapi_mvc.utils

.. autofunction:: fastapi_mvc.utils.run_shell

.. autofunction:: fastapi_mvc.utils.get_git_user_info

.. autofunction:: fastapi_mvc.utils.excepthook.global_except_hook
