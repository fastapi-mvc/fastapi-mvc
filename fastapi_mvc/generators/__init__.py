"""Fastapi-mvc generators.

Fastapi-mvc comes with a number of scripts called generators that are designed
to make your development life easier by creating everything that’s necessary to
start working on a particular task.

Each generator is build of the following:
    * A cookiecutter template.
    * Click options and arguments for creating generator CLI subcommand.
    * Methods for creating and deleting the thing it generates.

Resources:
    1. `Click Arguments`_
    2. `Click Options`_
    3. `Cookiecutter Docs`_

.. _Click Arguments:
    https://click.palletsprojects.com/en/8.1.x/arguments/

.. _Click Options:
    https://click.palletsprojects.com/en/8.1.x/options/

.. _Cookiecutter Docs:
    https://cookiecutter.readthedocs.io/en/1.7.2/

"""
from fastapi_mvc.generators.base import Generator
from fastapi_mvc.generators.project import ProjectGenerator
from fastapi_mvc.generators.controller import ControllerGenerator
from fastapi_mvc.generators.generator import GeneratorGenerator
