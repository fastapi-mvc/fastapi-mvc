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

.. autoclass:: fastapi_mvc.generators.controller
   :members:
   :show-inheritance:

.. autoclass:: fastapi_mvc.generators.generator
   :members:
   :show-inheritance:

.. autofunction:: fastapi_mvc.generator.load_generators

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

.. autoclass:: fastapi_mvc.utils.ShellUtils
   :members:
   :show-inheritance:

.. autofunction:: fastapi_mvc.utils.excepthook.global_except_hook
