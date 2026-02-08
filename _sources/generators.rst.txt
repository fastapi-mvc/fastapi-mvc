:tocdepth: 2

Generators
==========

When you create an application using the ``fastapi-mvc new`` command, you are in fact using a generator.
After that, you can get a list of all available generators by just invoking ``fastapi-mvc generate``:

.. code-block:: bash

    fastapi-mvc new my-app
    cd my-app
    fastapi-mvc generate --help
    # Or using alias short-cut
    fm g --help

You will get a list of all generators that come with ``fastapi-mvc``.
If you need a detailed description of the controller generator, for example, you can simply do:

.. code-block:: bash

    fastapi-mvc generate controller --help
    # Or using alias short-cut
    fm g ctl --help

Creating your first generator
-----------------------------

Generators are built on top of `copier <https://github.com/copier-org/copier>`__. It provides powerful options for manipulating and creating files based on given input and template.
Moreover, it is agnostic to the programming language one is templating. The best way to understand concepts behind generators is by creating one from scratch (but worry not, there is a builtin generator for generating generators, so you won't have to do this every time).
For instance, let's create a ``foobar`` generator with name given as CLI argument, that creates a ``hello_world.py`` file inside ``my_app`` directory.

Generator CLI
~~~~~~~~~~~~~

The first step is to create a bare minimum generator command line interface at ``./lib/generators/foobar/foobar.py`` with the following content:

.. code-block:: python

    import os

    import click
    import copier
    from fastapi_mvc.cli import GeneratorCommand
    from fastapi_mvc.utils import require_fastapi_mvc_project
    from fastapi_mvc.constants import ANSWERS_FILE


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
        cls=GeneratorCommand,
        help=cmd_help,
        short_help=cmd_short_help,
        epilog=epilog,
        # Define alias short-cut for more efficient invocation
        alias="foo",
        # Define category under which generator should be printed in ``fastapi-mvc generate`` CLI command help page.
        category="Custom",
    )
    @click.argument(
        "NAME",
        required=True,
        nargs=1,
    )
    def foobar(name: str) -> None:
        """Define foobar generator command-line interface.

        Args:
            name (str): Given name to greet.

        """
        project_data = require_fastapi_mvc_project()

        data = {
            "project_name": project_data["project_name"],
            "name": name.lower().replace("-", "_"),
        }

        copier.run_copy(
            src_path=os.path.dirname(__file__),  # Or use repository address
            data=data,
            answers_file=ANSWERS_FILE,
        )


Our new generator is quite simple, it uses ``GeneratorCommand`` class to instantiate command line interface for this concrete generator. If you have used `Click <https://click.palletsprojects.com/en/8.1.x/>`__ before, this should be familiar to you.
When a generator is invoked, the decorated method is executed with arguments and options provided from CLI command. In this case it is ``name`` CLI argument. Using ``GeneratorCommand`` class is not required. It only provides you with ``alias``, ``category`` and some help formatting utils.
You can use ``click.Command`` should you choose.

Copier template
~~~~~~~~~~~~~~~

In order to actually generate something, we still need to define a copier template. The first step is to create core template structure:

.. code-block:: bash

    foobar/
    ├── template
    │   └── {{package_name}}
    │       └── hello_world.py.jinja
    └── copier.yml

You must have:

* A ``copier.yml`` file, that defines copier template configuration.
* A subdirectory that contains template files (configurable and not mandatory).

Beyond that, you can have whatever files/directories you want.

.. note::
    Directory ``{{package_name}}`` is only needed if you want to generate files inside the project Python package.

The ``copier.yml`` defines template configuration, in our case it will be the following content:

.. code-block:: yaml

    # TEMPLATE SETTINGS
    _subdirectory: template
    _templates_suffix: .jinja
    _min_copier_version: "6.2.0"
    _envops:
      block_end_string: "%}"
      block_start_string: "{%"
      comment_end_string: "#}"
      comment_start_string: "{#"
      keep_trailing_newline: true
      variable_end_string: "}}"
      variable_start_string: "{{"

    # TEMPLATE QUESTIONS
    project_name:
      type: str
      help: >-
        What's your project name?

        Do not use dots or spaces in the name; just "A-Za-z0-9-_" please.

    name:
      type: str
      help: What is the name to greet for the generator hello world example?

    # TEMPLATE NONE-CONFIGURABLE DEFAULTS
    package_name:
      type: str
      default: "{{ project_name|lower|replace(' ','_')|replace('-','_') }}"
      when: false

.. note::
    You might wonder why ``project_name`` and ``package_name`` are included in the template configuration when the generator only uses ``name`` (equivalent to name CLI argument) question?
    Since ``foobar`` generator will create a file inside the project Python module, it needs to know its directory name first.
    As a way to normalize value for the template, ``package_name`` - the non-configurable default is based on ``project_name`` value.
    Hence ``project_name`` question in ``copier.yml`` and the value in the ``data`` dictionary passed to the ``run_copy`` method.
    Moreover, for your convenience, this value is automatically read from ``.fastapi-mvc.yml`` file via ``require_fastapi_mvc_project()`` utility method.
    But nothing stands in your way of providing package_name directly or in any valid way you’d see fit.

Template questions looks familiar? It is contains exactly the same keys as copier data dictionary:

.. code-block:: python

        data = {
            "project_name": ctx.command.project_data["project_name"],
            "name": name.lower().replace("-", "_"),
        }

Lastly, we need to implement ``hello_world.py.jinja`` template file.

.. code-block:: jinja

    """A dummy template file example"
    print("Hello {{name}}!")

Before we can actually invoke foobar generator we need to make it visible for fastapi-mvc.

Generators lookup
~~~~~~~~~~~~~~~~~

To be imported a valid fastapi-mvc generator must have:

* A ``*.py`` file, that defines generator CLI and execution logic.
* A ``__init__.py`` file, that defines Python submodule and attribute for generator lookup.

Since Python modules can have many files, classes, and methods we need to tell fastapi-mvc where to search for ``foobar`` generator. To do so write the following content to ``__init__.py``:

.. code-block:: python

    """Custom generator for fastapi-mvc."""
    from .foobar import foobar

    # NOTE! Do not edit this! Method for programmatically loading user generators
    # depends on having only one fastapi_mvc.Generator in module `generator` attribute.
    generator = foobar

Now our ``foobar`` generator structure will look like so:

.. code-block:: bash

    foobar/
    ├── template
    │   └── {{package_name}}
    │       └── hello_world.py.jinja
    ├── __init__.py
    ├── foobar.py
    └── copier.yml

By default ``fastapi-mvc`` will try import generators from ``lib/generators`` located in the project root directory. However, one can provide additional paths to look for via ``FMVC_PATH`` environment variable:

.. code-block:: bash

    export FMVC_PATH="/my/generators:/home/user/fastapi-mvc-generators"
    fastapi-mvc generate --help

.. note::
    The given path must point to the parent directory, not a generator root! For instance, if our ``foobar`` directory is located at ``/tmp/generators/foobar`` one needs to point to ``/tmp/generators`` otherwise import will fail with an exception.

Invoking generator
~~~~~~~~~~~~~~~~~~

To invoke our new generator we just need to call it:

.. code-block:: bash

    $ fastapi-mvc generate foobar johndoe

    Copying from template version None
     identical  .
     identical  my_app
        create  my_app/hello_world.py

    $ cat my_app/hello_world.py
    """A dummy template file example"
    print("Hello johndoe!")

Before we go on, let’s see our brand new generator description:

.. code-block:: bash

    $ fastapi-mvc generate foobar --help
    Usage: fastapi-mvc generate foobar [OPTIONS] NAME

      Creates a dummy hello_world.py example.

    Options:
      --help  Show this message and exit.

    Example:
        `fastapi-mvc generate foobar WORLD!`

        creates an example file:
            helo_world.py

Considerations
~~~~~~~~~~~~~~

This tutorial explains the basic concept and implementations behind fastapi-mvc generators.
The same use case can be templated in various ways. The full possibilities of copier and jinja are beyond the scope of this tutorial.

For more information please see `copier documentation <https://copier.readthedocs.io/en/v6.2.0/>`__, `jinja documentation <https://jinja.palletsprojects.com/en/3.1.x/>`__.
Builtin generators can be found in `fastapi_mvc.generators submodule <https://github.com/fastapi-mvc/fastapi-mvc/tree/master/fastapi_mvc/generators>`__
In case of any questions or problems, feel free to create an `issue <https://github.com/fastapi-mvc/fastapi-mvc/issues/new/choose>`__ or open a new `discussion <https://github.com/fastapi-mvc/fastapi-mvc/discussions>`__.

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
            lib/generators/awesome/.github
            lib/generators/awesome/.github/dependabot.yml
            lib/generators/awesome/.github/workflows/update-flake.yml
            lib/generators/awesome/.envrc
            lib/generators/awesome/.gitignore
            lib/generators/awesome/CHANGELOG.md
            lib/generators/awesome/LICENSE
            lib/generators/awesome/README.md
            lib/generators/awesome/__init__.py
            lib/generators/awesome/template
            lib/generators/awesome/template/{{package_name}}
            lib/generators/awesome/template/{{package_name}}/hello_world.py
            lib/generators/awesome/update.sh
            lib/generators/awesome/flake.nix
            lib/generators/awesome/flake.lock
            lib/generators/awesome/.generator.yml
            lib/generators/awesome/awesome.py

Adding CLI options and arguments
--------------------------------

If you have used `Click <https://click.palletsprojects.com/en/8.1.x/>`__ before, this should be a piece of cake for you.

Really, the only difference between any ``Click`` command and fastapi-mvc generator is a custom class, and its few extra ``kwargs`` passed to ``@click.command`` decorator.
The differences are highlighted:

.. code-block:: python
    :emphasize-lines: 2, 6 - 7

    @click.command(
        cls=GeneratorCommand,
        help=cmd_help,
        short_help=cmd_short_help,
        epilog=epilog,
        alias="foo",
        category="Custom",
    )

The rest of the implementation is just a pure Python Click.

What about project data?
------------------------

Some generators might need to know the state from which a concrete project was rendered to generate something on top of it.
For instance, it might depend on the information if the project has enabled Nix and will render its contents accordingly or just simply needs to know the name of the Python package directory name.
This is where project data comes in. Via ``require_fastapi_mvc_project()`` method, one can load ``.fastapi-mvc.yml`` file and validate the project.

But wait? What data is actually stored in ``.fastapi-mvc.yml`` file? Well this depends on the `copier project template <https://github.com/fastapi-mvc/copier-project>`__ used for rendering the project.
In a nutshell it is a copier answers file that includes the current answers and copier metadata. It is used both by copier (updating, copying over, etc.) and fastapi-mvc.

Example contents:

.. code-block:: yaml

    # Changes here will be overwritten by Copier
    _commit: efb938e
    _src_path: https://github.com/fastapi-mvc/copier-project.git
    aiohttp: true
    author: Radosław Szamszur
    chart_name: test-app
    container_image_name: test-app
    copyright_date: '2022'
    email: github@rsd.sh
    fastapi_mvc_version: 0.17.0
    github_actions: true
    helm: true
    license: MIT
    nix: true
    package_name: test_app
    project_description: This project was generated with fastapi-mvc.
    project_name: test-app
    redis: true
    repo_url: https://your.repo.url.here
    script_name: test-app
    version: 0.1.0

Define alias short-cut
----------------------

It is all about efficiency. Why type the long ``fastapi-mvc generate foobar ...`` command? Ain't nobody got time for that. All you need to do is define an alias for your generator:

.. code-block:: python

    @click.command(
        cls=GeneratorCommand,
        ...,
        alias="foo",
    )

And, now invoke it with speed: ``fm g foo ...``

.. note::
    ``fm`` is an alias for ``fastapi-mvc`` entrypoint, and ``g`` is an alias for ``generate`` command.
