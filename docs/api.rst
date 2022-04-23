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

.. autofunction:: load_generators

Commands
--------

.. currentmodule:: fastapi_mvc.commands

.. autoclass:: Command
   :members:

.. autoclass:: Invoker
   :members:

.. autoclass:: Generate
   :members:

.. autoclass:: RunShell
   :members:

CLI
---

.. autofunction:: fastapi_mvc.cli.cli.cli

.. autofunction:: fastapi_mvc.cli.run.run

.. autofunction:: fastapi_mvc.cli.new.new

.. autofunction:: fastapi_mvc.cli.generate.generate

.. autoclass:: fastapi_mvc.cli.generate.DynamicMultiCommand
   :members:

.. autoclass:: fastapi_mvc.cli.generate.GeneratorCommand
   :members:

Utils
-----

.. currentmodule:: fastapi_mvc.utils

.. autoclass:: ShellUtils
   :members:
