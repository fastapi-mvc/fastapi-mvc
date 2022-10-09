:tocdepth: 2
Generators
==========

.. note::
    **WORK IN PROGRESS** I'll add the rest `documentation updates <https://github.com/fastapi-mvc/fastapi-mvc/issues/175>`__ asap.
    However, there is a bare minimum to get you started, especially if you are familiar with `Click <https://click.palletsprojects.com/en/8.1.x/>`__

When you create an application using the ``fastapi-mvc new`` command, you are in fact using a generator.
After that, you can get a list of all available generators by just invoking ``fastapi-mvc generate``:

.. code-block:: bash

    fastapi-mvc new my-app
    cd my-app
    fastapi-mvc generate --help

You will get a list of all generators that come with ``fastapi-mvc``.
If you need a detailed description of the controller generator, for example, you can simply do:

.. code-block:: bash

    fastapi-mvc generate controller --help


Creating your first generator
-----------------------------

Generators are built on top of `copier <https://github.com/copier-org/copier>`__. It provides powerful options for manipulating and creating files based on given input and template.
Moreover, it is agnostic to the programming language one is templating. The best way to understand concepts behind generators is by creating one from scratch (but worry not, there is a builtin generator for generating generators, so you won't have to do this every time).
For instance, let's create a ``foobar`` generator that creates a ``hello_world.py`` file inside ``my_app/config`` with name given as CLI argument.

Generator
~~~~~~~~~

The first step is to create a bare minimum generator class at ``lib/generators/foobar/foobar.py`` with the following content:

.. code-block:: python

    import os

    import click
    from fastapi_mvc import Generator


    cmd_short_help = "Run custom generator foobar."
    cmd_help = """\
    Creates a dummy hello_world.py example.
    """
    epilog = """\
    Example:
        `fastapi-mvc generate foobar WORLD!`

        creates an example file:
            helo_world.py

    """


    @click.command(
        cls=Generator,
        # Or use repository address
        template=os.path.dirname(__file__),
        category="Custom",
        help=cmd_help,
        short_help=cmd_short_help,
    )
    @click.argument(
        "NAME",
        required=True,
        nargs=1,
    )
    @click.pass_context
    def foobar(ctx, name):
        # You can access Generator class object instance for this command via click.Context
        # https://click.palletsprojects.com/en/8.1.x/api/?highlight=context#click.Context.command
        ctx.command.ensure_project_data()

        data = {
            "project_name": ctx.command.project_data["project_name"],
            "name": name.lower().replace("-", "_"),
        }

        ctx.command.run_copy(data=data)


Our new generator is quite simple, it uses ``Generator`` class to instantiate command line interface for this generator. If you have used `Click <https://click.palletsprojects.com/en/8.1.x/>`__ before, this should be familiar to you.
When a generator is invoked, the decorated method is executed with ``kwagrs`` provided from generator CLI command - more on that a bit later.

.. note::
    **WORK IN PROGRESS** I'll add the rest `documentation updates <https://github.com/fastapi-mvc/fastapi-mvc/issues/175>`__ asap.

Considerations
~~~~~~~~~~~~~~

This tutorial explains the basic concept and implementations behind fastapi-mvc generators.
The same use case can be templated in various ways. The full possibilities of copier and jinja are beyond the scope of this tutorial.

For more information please see `copier documentation <https://copier.readthedocs.io/en/v6.2.0/>`__, `jinja documentation <https://jinja.palletsprojects.com/en/3.1.x/>`__.
Builtin generators can be found in `fastapi_mvc.generators submodule <https://github.com/fastapi-mvc/fastapi-mvc/tree/master/fastapi_mvc/generators>`__
In case of any questions or problems, feel free to create an `issue <https://github.com/fastapi-mvc/fastapi-mvc/issues/new/choose>`__.

Creating generators with generators
-----------------------------------

Generators themselves have a generator:

.. code-block:: bash

    $ fastapi-mvc generate generator --help
    Usage: fastapi-mvc generate generator [OPTIONS] NAME

      Creates a new generator at lib/generators. Pass the generator name
      under_scored.

    Options:
      -N, --skip-nix                  Skip nix expression files.
      --license [MIT|BSD2|BSD3|ISC|Apache2.0|LGPLv3+|LGPLv3|LGPLv2+|LGPLv2|no]
                                      Choose license.  [default: MIT]
      --repo-url TEXT                 New project repository url.
      --help                          Show this message and exit.

    Example:
        `fastapi-mvc generate generator awesome`

        creates a standard awesome generator:
            lib/generators/awesome/.envrc
            lib/generators/awesome/.gitignore
            lib/generators/awesome/CHANGELOG.md
            lib/generators/awesome/LICENSE
            lib/generators/awesome/README.md
            lib/generators/awesome/__init__.py
            lib/generators/awesome/poetry.lock
            lib/generators/awesome/pyproject.toml
            lib/generators/awesome/template
            lib/generators/awesome/template/{{package_name}}
            lib/generators/awesome/template/{{package_name}}/hello_world.py
            lib/generators/awesome/update.sh
            lib/generators/awesome/default.nix
            lib/generators/awesome/shell.nix
            lib/generators/awesome/.fastapi-mvc.yml
            lib/generators/awesome/awesome.py

Generator base class API reference
----------------------------------

.. autoclass:: fastapi_mvc.Generator
   :members:
   :show-inheritance:
