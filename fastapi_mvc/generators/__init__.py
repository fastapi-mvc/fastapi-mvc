"""Fastapi-mvc generators.

Fastapi-mvc comes with a number of scripts called generators that are designed
to make your development life easier by creating everything that’s necessary to
start working on a particular task.

Each generator is build of the following:
    * A copier template.
    * Click options and arguments for creating generator CLI subcommand.
    * Method for creating thing it generates.

Resources:
    1. `Click Arguments`_
    2. `Click Options`_
    3. `Copier Docs`_

.. _Click Arguments:
    https://click.palletsprojects.com/en/8.1.x/arguments/

.. _Click Options:
    https://click.palletsprojects.com/en/8.1.x/options/

.. _Copier Docs:
    https://copier.readthedocs.io/en/v6.2.0

"""
from fastapi_mvc.generators.loader import load_generators
from fastapi_mvc.generators.generator import generator
from fastapi_mvc.generators.controller import controller


__all__ = ("load_generators", "controller", "generator")
