Generators
==========

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

Generators are built on top of `cookiecutter <https://github.com/cookiecutter/cookiecutter>`__. It provides powerful options for manipulating and creating files based on given input and template.
Moreover, it is agnostic to the programming language one is templating. The best way to understand concepts behind generators is by creating one from scratch (but worry not, there is a builtin generator for generating generators, so you won't have to do this every time).
For instance, let's create a ``foobar`` generator that creates a file inside ``my_app/config`` with name given as CLI argument.

Generator class
~~~~~~~~~~~~~~~

The first step is to create a bare minimum generator class at ``lib/generators/foobar/foobar.py`` with the following content:

.. code-block:: python

    import os

    from cookiecutter.main import cookiecutter
    from fastapi_mvc.generators import Generator


    class FoobarGenerator(Generator):

        __slots__ = ("_parser",)

        name = "foobar"
        template = os.path.abspath(
            os.path.join(
                os.path.abspath(__file__),
                "../template",
            )
        )

        def __init__(self, parser):
            Generator.__init__(self)
            self._parser = parser

        def new(self, name, skip):
            context = {
                "package_name": self._parser.package_name,
                "folder_name": self._parser.folder_name,
                "foobar_name": name,
            }

            self._log.debug("Cookiecutter context: {0}".format(context))

            cookiecutter(
                self.template,
                extra_context=context,
                output_dir=os.path.abspath(
                    os.path.join(
                        self._parser.project_root,
                        "../",
                    )
                ),
                no_input=True,
                overwrite_if_exists=True,
                skip_if_file_exists=skip,
            )

Our new generator is quite simple, it inherits from ``Generator`` base class, and has one method definition along with some class variables.
When a generator is invoked, the ``new`` method is executed with ``kwagrs`` provided from generator CLI command - more on that a bit later. Now let's break down the various implementations of ``FoobarGenerator`` class:

Class variables
***************

They define generator CLI and cookiecutter template:

* name (required) - A distinguishable generator name, that will be used as subcommand for ``fastapi-mvc generate`` CLI command.
* template (required) - Path to generator cookiecutter template root directory or remote repository URL.
* usage - Path to generator usage file. This will be printed at the end of generator CLI command help page.
* category - Name under which generator should be printed in ``fastapi-mvc generate`` CLI command help page.
* cli_arguments - Click arguments to register with this generator CLI command.
* cli_options - Click options to register with this generator CLI command.
* cli_help - The help string to use for this generator CLI command.
* cli_short_help - The short help to use for this generator CLI command. This is shown on the command listing of ``fastapi-mvc generate`` command.
* cli_deprecated - Issues a message indicating that the generator CLI command is deprecated.

Class variables that are not defined will be inherited from ``Generator`` base class. The defaults are:

.. code-block:: python

    name: str = NotImplemented
    template: str = NotImplemented
    usage: str = None
    category: str = "Other"
    cli_arguments = [
        Argument(
            param_decls=["NAME"],
            required=True,
            nargs=1,
        ),
    ]
    cli_options = [
        Option(
            param_decls=["-S", "--skip"],
            help="Skip files that already exist.",
            is_flag=True,
        ),
    ]
    cli_help = None
    cli_short_help = None
    cli_deprecated = False

Why ``__slots__``?
******************

In this case, slots apart from standard behavior, also ensure that class variables available in object instances as object attributes are read-only.
They define generator CLI and cookiecutter template and thus, by principle, should be immutable at RunTime.
However, if the need arises, you can still edit them should you choose. To do so either remove ``__slots__`` or access via ``__class__`` magic method.
Removing __slots__ will make class variables default values for object attributes. Editing one from the object instance will not change the value
of the class variable or the value in another object. Is, the other way round when accessing via ``__class__`` magic method ex. ``self.__class__.name``.
Not only it will change a class variable value, but also an object attribute value for all objects created from this class. Provided, class
is one entry in memory. For instance, if you would deep clone it, the above would only apply to the class in which the change was made. Not
that this is super important, because I do not see a use case where there would be ever two generator class object instances. But I want you to
understand the difference.

Constructor
***********

Each generator ``__init__`` will receive a parser object instance. It contains necessary project context data like project folder and package name. For all available parser attributes please see the :ref:`parser API reference <api:Parsers>`.

New method
**********

As said previously the ``new`` method is executed with ``kwagrs`` provided from generator CLI command. Actual method implementation and cookiecutter API call is up to you to define. But let's look closely at the example:

.. code-block:: python

        def new(self, name, skip):
            context = {
                "package_name": self._parser.package_name,
                "folder_name": self._parser.folder_name,
                "foobar_name": name,
            }

            self._log.debug("Cookiecutter context: {0}".format(context))

            cookiecutter(
                self.template,
                extra_context=context,
                output_dir=os.path.abspath(
                    os.path.join(
                        self._parser.project_root,
                        "../",
                    )
                ),
                no_input=True,
                overwrite_if_exists=True,
                skip_if_file_exists=skip,
            )

.. note::
    To get the kwarg name, the chosen name is converted to lower case, up to two dashes are removed as the prefix, and other dashes are converted to underscores:

    * ``-f``, ``--foo-bar``, the name is ``foo_bar``
    * ``-x``, the name is ``x``
    * ``-f``, ``--filename``, ``dest``, the name is ``dest``
    * ``--CamelCase``, the name is ``camelcase``
    * ``-f``, ``-fb``, the name is ``f``
    * ``--f``, ``--foo-bar``, the name is ``f``
    * ``---f``, the name is ``_f``

    In this particular example, kwarg for generator ``--skip`` CLI option is ``skip`` and kwarg for ``NAME`` CLI argument is ``name``.

Since ``FoobarGenerator`` class does not define its own class variables for CLI options and arguments, the defaults are being used:

* name - CLI argument - name.
* skip - If True skip the files in the corresponding directories if they already exist.

Lastly, we need to call ``cookiecutter`` with the appropriate template and context.

Cookiecutter template
~~~~~~~~~~~~~~~~~~~~~

In order to actually generate something, we still need to define a cookiecutter template. The first step is to create core template structure:

.. code-block:: bash

    template/
    ├── {{cookiecutter.folder_name}}
    │   └── {{cookiecutter.package_name}}
    ├── cookiecutter.json
    └── USAGE

You must have:

* A ``cookiecutter.json`` file.
* A ``{{cookiecutter.folder_name}}`` directory, where ``folder_name`` is defined in your ``cookiecutter.json``.

Beyond that, you can have whatever files/directories you want.

.. note::
    Directory ``{{cookiecutter.package_name}}`` is only needed if you want to generate files inside the project package as well.

The ``cookiecutter.json`` contains all the template parameters, in our case, it is the following content:

.. code-block:: json

    {
      "folder_name": "{{ cookiecutter.folder_name }}",
      "package_name": "{{ cookiecutter.package_name }}",
      "foobar_name": "{{ cookiecutter.foobar_name }}"
    }

Looks familiar? It is contains exactly the same keys as cookiecutter context dictionary in ``new()`` method:

.. code-block:: python

    context = {
        "package_name": self._parser.package_name,
        "folder_name": self._parser.folder_name,
        "foobar_name": name,
    }

Lastly we need to template file which will be generated in ``my_app/config``.
Create a file at ``lib/generators/foobar/template/{{cookiecutter.folder_name}}/{{cookiecutter.package_name}}/config/{{cookiecutter.foobar_name}}.py`` with the following content:

.. code-block::

    from pydantic import BaseSettings

    class {{cookiecutter.foobar_name}}(BaseSettings):

        foo: str = "bar"

Before we can actually invoke foobar generator we need to make ``FoobarGenerator`` class visible for ``fastapi-mvc``.

Generators lookup
~~~~~~~~~~~~~~~~~

When you run ``fastapi-mvc generate foobar [OPTIONS] [ARGS]`` fastapi-mvc requires these files under project root directory:

.. code-block:: bash

    ├── lib
    │   └── generators
    │       └── foobar
    │           ├── foobar.py
    │           └── __init__.py

Since Python modules can have many files, classes, and methods we need to tell fastapi-mvc where to search for ``FoobarGenerator`` class. To do so write the following content to ``__init__.py``:

.. code-block:: python

    from .foobar import FoobarGenerator

    # NOTE! Method for programmatically loading user generators depends on having only one class in module `generator_class` attribute.
    generator_class = FoobarGenerator

.. note::
    At the time being fastapi-mvc will try import generators only from ``lib/generators`` located in the project root directory.
    In the future releases I'm planing to add a global path, or parametrize search paths by env variable. You are always welcome to create an `issue <https://github.com/fastapi-mvc/fastapi-mvc/issues/new/choose>`__.

Invoking generator
~~~~~~~~~~~~~~~~~~

To invoke our new generator, we just need to do:

.. code-block:: bash

    $ fastapi-mvc generate foobar myconfig
    [INFO] Running generator: foobar

    $ cat my_app/config/myconfig.py
    from pydantic import BaseSettings

    class myconfig(BaseSettings):

        foo: str = "bar"

Before we go on,, let's see our brand new generator description:

.. code-block:: bash

    $ fastapi-mvc generate foobar --help
    Usage: fastapi-mvc generate foobar [OPTIONS] NAME

    Options:
      -S, --skip  Skip files that already exist.
      --help      Show this message and exit.

Fastapi-mvc will only include usage description from CLI options and arguments. To fully customize help we can solve this problem in two ways.
The first one is setting ``cli_help`` and ``cli_short_help`` class variables. The second way to add a description is by creating a file named USAGE.
But more on that in the next steps.

Considerations
~~~~~~~~~~~~~~

This tutorial explains the basic concept and implementations behind fastapi-mvc generators.
The same use case can be templated in various ways. The full possibilities of cookiecutter are beyond the scope of this tutorial.

For more information please see `cookiecutter documentation <https://cookiecutter.readthedocs.io/en/1.7.3/>`__.
Builtin generators can be found in `fastapi_mvc.generators submodule <https://github.com/fastapi-mvc/fastapi-mvc/tree/master/fastapi_mvc/generators>`__
In case of any questions or problems, feel free to create an `issue <https://github.com/fastapi-mvc/fastapi-mvc/issues/new/choose>`__.

Creating generators with generators
-----------------------------------

Generators themselves have a generator:

.. code-block:: bash

    $ fastapi-mvc generate generator --help
    Usage: fastapi-mvc generate generator [OPTIONS] NAME

    Options:
      -S, --skip  Skip files that already exist.
      --help      Show this message and exit.

    Description:
        Creates a new generator at lib/generators. Pass the generator name
        under_scored.

    Example:
        `fastapi-mvc generate generator my_controller`

    creates a project local my_controller generator:
        lib/generators/my_controller/
        lib/generators/my_controller/__init__.py
        lib/generators/my_controller/generator.py
        lib/generators/my_controller/template/USAGE
        lib/generators/my_controller/template/

    $ fastapi-mvc generate generator foobar
    [INFO] Running generator: generator

This is the generator just created:

.. code-block:: python

    """FastAPI MVC foobar generator implementation."""
    import os

    from cookiecutter.main import cookiecutter
    from fastapi_mvc.generators import Generator


    class FoobarGenerator(Generator):
        """Foobar generator implementation.

        Args:
            parser (IniParser): IniParser object instance of a fastapi-mvc project.

        Attributes:
            name (str): **(class variable)** A distinguishable generator name, that
                will be used as subcommand for ``fastapi-mvc generate`` CLI command.
            template (str): **(class variable)**  Path to generator cookiecutter
                template root directory.
            usage (typing.Optional[str]): **(class variable)** Path to generator
                usage file, that will be printed at the end of its CLI command help
                page.
            category (str): **(class variable)** Name under which generator should
                be printed in ``fastapi-mvc generate`` CLI command help page.
            _log (logging.Logger): Logger class object instance.
            _parser (IniParser): IniParser object instance for current fastapi-mvc
                project.

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

        __slots__ = ("_parser",)

        name = "foobar"
        template = os.path.abspath(
            os.path.join(
                os.path.abspath(__file__),
                "../template",
            )
        )
        category = "MyGenerators"
        usage = os.path.join(template, "USAGE")

        def __init__(self, parser):
            """Initialize FoobarGenerator class object instance."""
            Generator.__init__(self)
            self._parser = parser

        def new(self, name, skip):
            """Generate a new foobar.

            Hint:
                Kwargs passed to this method are from generator CLI options and
                arguments. Since this generator does not override base class
                cli_options and cli_arguments class variables, defaults are used.

            Args:
                name (str): Given CLI argument - name.
                skip (bool): If True skip the files in the corresponding directories
                    if they already exist.

            """
            context = {
                "package_name": self._parser.package_name,
                "folder_name": self._parser.folder_name,
                "foobar_name": name,
            }

            self._log.debug("Cookiecutter context: {0}".format(context))

            cookiecutter(
                self.template,
                extra_context=context,
                output_dir=os.path.abspath(
                    os.path.join(
                        self._parser.project_root,
                        "../",
                    )
                ),
                no_input=True,
                overwrite_if_exists=True,
                skip_if_file_exists=skip,
            )

        def destroy(self, **kwargs):
            """Not yet implemented.

            Args:
                **kwargs(dict): Abstract methods kwargs.

            """
            raise NotImplementedError

.. warning::
    Destroy method is a feature not yet implemented. However, it will be used to un-generate/undo.
    For now, you can leave it as is, since base class requires this method to be defined.

Let's see our brand new generator description:

.. code-block:: bash

    $ fastapi-mvc generate --help
    Usage: fastapi-mvc generate [OPTIONS] GENERATOR [ARGS]...

      The 'fastapi-mvc generate' commands runs a generator of your choice for a
      fastapi-mvc project at the current working directory.

    Options:
      --help  Show this message and exit.

    Please choose a generator below.

    Builtins:
      controller
      generator

    MyGenerators:
      foobar

    $ fastapi-mvc generate foobar --help
    Usage: fastapi-mvc generate foobar [OPTIONS] NAME

    Options:
      -S, --skip  Skip files that already exist.
      --help      Show this message and exit.

    Description:
        Explain the generator

    Example:
        fastapi-mvc generate test thing

        This will create:
            what/will/it/create

Adding CLI options and arguments
--------------------------------

Fastapi-mvc generators can be easily modified to accept custom command line arguments and options. This functionality comes from `click <https://click.palletsprojects.com/en/8.1.x>`__.
To make things easier ``cli_options`` and ``cli_arguments`` are defined 1:1 as one would using Click library directly. For instance, let’s take recreate the following Click CLI into our generator:

.. code-block:: python

    import click

    @click.command()
    @click.option('--count', default=1, help='Number of greetings.')
    @click.option('--name', prompt='Your name',
                  help='The person to greet.')
    def hello(count, name):
        """Simple program that greets NAME for a total of COUNT times."""
        for x in range(count):
            click.echo(f"Hello {name}!")

    if __name__ == '__main__':
        hello()

All we need to do is, change the decorator with class constructor call, and pack arguments in ``param_decls`` kwarg (this is due to differences in API between option decorator and class constructor):

.. code-block:: python

    from click import Option

    class FoobarGenerator(Generator):

        __slots__ = ("_parser",)

        name = "foobar"
        template = os.path.abspath(
            os.path.join(
                os.path.abspath(__file__),
                "../template",
            )
        )
        cli_arguments = []
        cli_options = [
            Option(
                param_decls=['--count'],
                default=1,
                help='Number of greetings.',
            ),
            Option(
                param_decls=['--name'],
                prompt='Your name',
                help='The person to greet.',
            )
        ]

We also need to update ``new()`` method kwargs:

.. code-block:: python

    def new(count, name):
        for x in range(count):
            print(f"Hello {name}!")

Now let's try it out:

.. code-block::

    $ fastapi-mvc generate foobar --help
    Usage: fastapi-mvc generate foobar [OPTIONS]

    Options:
      --count INTEGER  Number of greetings.
      --name TEXT      The person to greet.
      --help           Show this message and exit.

    $ fastapi-mvc generate foobar --count 3 --name "I'm the Dude"
    [INFO] Running generator: foobar
    Hello I'm the Dude!
    Hello I'm the Dude!
    Hello I'm the Dude!

The same applies to ``click.Arguments``.

.. warning::
    The order of ``click.Arguments`` is important since CLI arguments are positional:

    .. code-block:: python

        cli_arguments = [
            Argument(
                param_decls=["SECOND"],
                required=True,
                nargs=1,
            ),
            Argument(
                param_decls=["FIRST"],
                required=True,
                nargs=1,
            ),
        ]

    Will result in having wrong order:

    .. code-block:: bash

        $ fastapi-mvc generate foobar --help
        Usage: fastapi-mvc generate foobar [OPTIONS] SECOND FIRST
        ...

Lastly you can customize generator command CLI help message via class variables:

.. code-block:: python

    cli_help = """\n
    This is long help.

    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
    """
    cli_short_help = "This is short help"

And by editing ``USAGE`` file:

.. code-block:: bash

    $ cat lib/generators/foobar/template/USAGE
    Description:
        Explain the generator

    Example:
        fastapi-mvc generate test thing

        This will create:
            what/will/it/create

Now let's have a look at the CLI command help:

.. code-block:: bash
    :emphasize-lines: 17, 22 - 27, 34 - 41

    $ fastapi-mvc generate --help
    Usage: fastapi-mvc generate [OPTIONS] GENERATOR [ARGS]...

      The 'fastapi-mvc generate' commands runs a generator of your choice for a
      fastapi-mvc project at the current working directory.

    Options:
      --help  Show this message and exit.

    Please choose a generator below.

    Builtins:
      controller
      generator

    MyGenerators:
      foobar  This is short help

    $ fastapi-mvc generate foobar --help
    Usage: fastapi-mvc generate foobar [OPTIONS] SECOND FIRST

      This is long help.

      Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
      tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
      quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
      consequat.

    Options:
      --count INTEGER  Number of greetings.
      --name TEXT      The person to greet.
      --help           Show this message and exit.

    Description:
        Explain the generator

    Example:
        fastapi-mvc generate test thing

        This will create:
            what/will/it/create

Generator base class API reference
----------------------------------

.. autoclass:: fastapi_mvc.generators.Generator
   :members:
   :show-inheritance:
