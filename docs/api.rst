API
===

.. module:: fastapi_mvc

Borg
----

.. autoclass:: Borg
   :members:

Parsers
-------

.. currentmodule:: fastapi_mvc.parsers

.. autoclass:: IniParser
   :members:

Generators
----------

.. currentmodule:: fastapi_mvc.generators

.. autoclass:: Generator
   :members:

.. autoclass:: ControllerGenerator
   :members:

.. autoclass:: GeneratorGenerator
   :members:

Commands
--------

.. currentmodule:: fastapi_mvc.commands

.. autoclass:: Command
   :members:

.. autoclass:: Invoker
   :members:

.. autoclass:: RunGenerator
   :members:

.. autoclass:: RunShell
   :members:

CLI
---

.. autofunction:: fastapi_mvc.cli.cli.cli

.. autofunction:: fastapi_mvc.cli.run.run

.. autofunction:: fastapi_mvc.cli.new.new

.. autofunction:: fastapi_mvc.cli.generate.get_generate_cmd

.. autofunction:: fastapi_mvc.cli.generate.invoke_generator

.. autoclass:: fastapi_mvc.cli.click_custom.GeneratorsMultiCommand
   :members:

.. autoclass:: fastapi_mvc.cli.click_custom.GeneratorCommand
   :members:

Utils
-----

.. currentmodule:: fastapi_mvc.utils

.. autoclass:: ShellUtils
   :members:
