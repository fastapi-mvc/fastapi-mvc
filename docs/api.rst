:tocdepth: 2

API
===

This part of the documentation lists the full API reference of all classes and functions.

CLI
---

.. automodule:: fastapi_mvc.cli

.. autoclass:: fastapi_mvc.cli.ClickAliasedCommand
   :members:
   :show-inheritance:

.. autoclass:: fastapi_mvc.cli.ClickAliasedGroup
   :members:
   :show-inheritance:

.. autoclass:: fastapi_mvc.cli.GeneratorCommand
   :members:
   :show-inheritance:

.. autoclass:: fastapi_mvc.cli.GeneratorsMultiCommand
   :members:
   :show-inheritance:

.. autofunction:: fastapi_mvc.cli.cli.cli

.. autofunction:: fastapi_mvc.cli.run.run

.. autofunction:: fastapi_mvc.cli.new.new

.. autofunction:: fastapi_mvc.cli.generate.get_generate_cmd

.. autofunction:: fastapi_mvc.cli.update.update


Generators
----------

.. automodule:: fastapi_mvc.generators

.. autofunction:: fastapi_mvc.generators.ControllerGenerator

.. autofunction:: fastapi_mvc.generators.GeneratorGenerator

.. autofunction:: fastapi_mvc.generators.ScriptGenerator

.. autofunction:: fastapi_mvc.generators.load_generators


Utils
-----

.. automodule:: fastapi_mvc.utils

.. autofunction:: fastapi_mvc.utils.get_poetry_path

.. autofunction:: fastapi_mvc.utils.run_shell

.. autofunction:: fastapi_mvc.utils.get_git_user_info

.. autofunction:: fastapi_mvc.utils.load_answers_file

.. autofunction:: fastapi_mvc.utils.ensure_permissions

.. autofunction:: fastapi_mvc.utils.require_fastapi_mvc_project

.. autofunction:: fastapi_mvc.utils.excepthook.global_except_hook
