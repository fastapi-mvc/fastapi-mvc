API
===

This part of the documentation lists the full API reference of all classes and functions.

Borg
----

.. autoclass:: fastapi_mvc.Borg
   :members:
   :special-members: __init__
   :show-inheritance:

Generators
----------

.. automodule:: fastapi_mvc.generators

.. autoclass:: fastapi_mvc.generators.Generator
   :members:
   :show-inheritance:

.. autoclass:: fastapi_mvc.generators.ProjectGenerator
   :members:
   :show-inheritance:

.. autoclass:: fastapi_mvc.generators.ControllerGenerator
   :members:
   :show-inheritance:

.. autoclass:: fastapi_mvc.generators.GeneratorGenerator
   :members:
   :show-inheritance:

Commands
--------

.. automodule:: fastapi_mvc.commands

.. autoclass:: fastapi_mvc.commands.Command
   :members:
   :show-inheritance:

.. autoclass:: fastapi_mvc.commands.Invoker
   :members:
   :show-inheritance:

.. autoclass:: fastapi_mvc.commands.RunGenerator
   :members:
   :show-inheritance:

.. autoclass:: fastapi_mvc.commands.RunShell
   :members:
   :show-inheritance:

CLI
---

.. automodule:: fastapi_mvc.cli

.. autofunction:: fastapi_mvc.cli.cli.cli

.. autofunction:: fastapi_mvc.cli.run.run

.. autofunction:: fastapi_mvc.cli.new.get_new_cmd

.. autofunction:: fastapi_mvc.cli.new.invoke_generator

.. autofunction:: fastapi_mvc.cli.generate.get_generate_cmd

.. autofunction:: fastapi_mvc.cli.generate.invoke_generator

.. autoclass:: fastapi_mvc.cli.click_custom.GeneratorsMultiCommand
   :members:
   :show-inheritance:

.. autoclass:: fastapi_mvc.cli.click_custom.GeneratorCommand
   :members:
   :show-inheritance:

Utils
-----

.. automodule:: fastapi_mvc.utils

.. autoclass:: fastapi_mvc.utils.ShellUtils
   :members:
   :show-inheritance:

.. autofunction:: fastapi_mvc.utils.excepthook.global_except_hook
