Quickstart
==========

Installation
------------

Prerequisites
~~~~~~~~~~~~~

Before you install fastapi-mvc, you should check to make sure that your system has the proper prerequisites installed. These include:

* Python 3.7 or later `(How to install python) <https://docs.python-guide.org/starting/installation/>`__
* pip
* curl
* make

Environment with `Nix <https://nixos.org/>`__
*********************************************

You can always spawn shell with all requirements using Nix:

.. code-block:: bash

    nix-shell shell.nix

From PyPi:
~~~~~~~~~~

To install fastapi-mvc from PyPi use ``pip install`` command:

.. code-block:: bash

    pip install fastapi-mvc

To verify that you have everything installed correctly, you should be able to run the following in a new terminal:

.. code-block:: bash

    fastapi-mvc --help

From source with Poetry:
~~~~~~~~~~~~~~~~~~~~~~~~

To install fastapi-mvc from source first clone the repository and use ``make install`` target:

.. code-block:: bash

    git clone git@github.com:rszamszur/fastapi-mvc.git
    cd fastapi-mvc
    make install

You can always customize poetry installation with `environment variables <https://python-poetry.org/docs/configuration/#using-environment-variables>`__:

.. code-block:: bash

    export POETRY_HOME=/custom/poetry/path
    export POETRY_CACHE_DIR=/custom/poetry/path/cache
    export POETRY_VIRTUALENVS_IN_PROJECT=true
    make install

Creating a new project
----------------------

Fastapi-mvc comes with a number of scripts called generators that are designed to make your development life easier by creating everything that's necessary to start working on a particular task.
One of these is the new application generator, which will provide you with the foundation of a fresh `FastAPI <https://fastapi.tiangolo.com/>`__ application so that you don't have to write it yourself.

To use this generator, open a terminal and run:

.. code-block:: bash

    $ fastapi-mvc new /tmp/galactic-empire
    [INFO] Running generator: new
    [INFO] Creating a new fastapi-mvc project: /tmp/galactic-empire
    [INFO] Executing shell command: ['make', 'install']
    [install] Begin installing project.
    Creating virtualenv galactic-empire in /tmp/galactic-empire/.venv
    Updating dependencies
    Resolving dependencies... (15.5s)

    Writing lock file

    Package operations: 57 installs, 0 updates, 0 removals

      • Installing frozenlist (1.3.0)
      • Installing idna (2.10)
      • Installing multidict (6.0.2)
      • Installing pyparsing (3.0.8)
      • Installing sniffio (1.2.0)
      • Installing aiosignal (1.2.0)
      • Installing anyio (3.5.0)
      • Installing async-timeout (4.0.2)
      • Installing attrs (21.4.0)
      • Installing charset-normalizer (2.0.12)
      • Installing iniconfig (1.1.1)
      • Installing mccabe (0.6.1)
      • Installing packaging (21.3)
      • Installing pluggy (1.0.0)
      • Installing py (1.11.0)
      • Installing pycodestyle (2.8.0)
      • Installing pyflakes (2.4.0)
      • Installing snowballstemmer (2.2.0)
      • Installing toml (0.10.2)
      • Installing typing-extensions (4.2.0)
      • Installing yarl (1.7.2)
      • Installing aiohttp (3.8.1)
      • Installing asgiref (3.5.0)
      • Installing certifi (2021.10.8)
      • Installing chardet (4.0.0)
      • Installing click (7.1.2)
      • Installing coverage (6.3.2)
      • Installing flake8 (4.0.1)
      • Installing h11 (0.13.0)
      • Installing httptools (0.4.0)
      • Installing mypy-extensions (0.4.3)
      • Installing pathspec (0.9.0)
      • Installing platformdirs (2.5.2)
      • Installing pydantic (1.9.0)
      • Installing pydocstyle (6.1.1)
      • Installing pytest (6.2.5)
      • Installing python-dotenv (0.20.0)
      • Installing pyyaml (6.0)
      • Installing starlette (0.17.1)
      • Installing tomli (1.2.3)
      • Installing urllib3 (1.26.9)
      • Installing uvloop (0.16.0)
      • Installing watchgod (0.8.2)
      • Installing websockets (10.3)
      • Installing aioredis (2.0.1)
      • Installing aioresponses (0.7.3)
      • Installing black (21.12b0)
      • Installing fastapi (0.75.2)
      • Installing flake8-docstrings (1.6.0)
      • Installing flake8-import-order (0.18.1)
      • Installing flake8-todo (0.7)
      • Installing gunicorn (20.1.0)
      • Installing mock (4.0.3)
      • Installing pytest-asyncio (0.15.1)
      • Installing pytest-cov (2.12.1)
      • Installing requests (2.25.1)
      • Installing uvicorn (0.17.6)

    Installing the current project: galactic-empire (0.1.0)
    Project successfully installed.
    To activate virtualenv run: $ poetry shell
    Now you should access CLI script: $ galactic-empire --help
    Alternatively you can access CLI script via poetry run: $ poetry run galactic-empire --help
    To deactivate virtualenv simply type: $ deactivate
    To activate shell completion:
     - for bash: $ echo 'eval "$(_GALACTIC_EMPIRE_COMPLETE=source_bash galactic-empire)' >> ~/.bashrc
     - for zsh: $ echo 'eval "$(_GALACTIC_EMPIRE_COMPLETE=source_zsh galactic-empire)' >> ~/.zshrc
     - for fish: $ echo 'eval "$(_GALACTIC_EMPIRE_COMPLETE=source_fish galactic-empire)' >> ~/.config/fish/completions/galactic-empire.fish

This will create a fastapi-mvc project called galactic-empire in a ``/tmp/galactic-empire`` directory and install its dependencies using ``make install``.

After you create the application, switch to its folder:

.. code-block:: bash

    $ cd /tmp/galactic-empire

The galactic-empire directory will have a number of generated files and folders that make up the structure of a fastapi-mvc application.
Here's a basic rundown on the function of each of the files and folders that fastapi-mvc creates by default:

.. code-block:: bash

    ├── .github
    │   └── workflows                GitHub Actions definition
    ├── build                        Makefile scripts
    ├── charts                       Helm chart for application
    │   └── galactic-empire
    ├── galactic_empire              Python project root
    │   ├── app                      FastAPI core implementation
    │   │   ├── controllers          Application controllers
    │   │   ├── exceptions           Application custom exceptions
    │   │   ├── models               Application models
    │   │   ├── utils                Application utilities
    │   │   ├── router.py            Application root APIRouter
    │   │   └── asgi.py              Application ASGI node implementation
    │   ├── cli                      Application CLI implementation
    │   ├── config                   Configuration submodule
    │   │   ├── application.py       Application configuration
    │   │   ├── gunicorn.conf.py     Gunicorn configuration
    │   │   └── redis.py             Redis configuration
    │   ├── version.py               Application version
    │   └── wsgi.py                  Application WSGI master node implementation
    ├── manifests                    Manifests for spotathome/redis-operator
    ├── tests
    │   ├── integration              Integration test implementation
    │   ├── unit                     Unit tests implementation
    ├── CHANGELOG.md
    ├── Dockerfile                   Dockerfile definition
    ├── .dockerignore
    ├── .coveragerc
    ├── .gitignore
    ├── fastapi-mvc.ini              Fastapi-mvc application configuration.
    ├── shell.nix                    Nix shell configuration file.
    ├── LICENSE
    ├── Makefile                     Makefile definition
    ├── poetry.lock                  Poetry dependency management lock file
    ├── pyproject.toml               PEP 518 - The build system dependencies
    ├── README.md
    ├── TAG                          Application version for build systems
    └── Vagrantfile                  Virtualized environment definiton

Hello, World!
-------------

To begin with, let's get some text up on screen quickly. To do this, you need to get your uvicorn development server running.

Starting up the Web Server
~~~~~~~~~~~~~~~~~~~~~~~~~~

You actually have a functional FastAPI application already. To see it, you need to start a web server on your development machine.
You can do this by running the following command in the galactic-empire directory:

.. code-block:: bash

    $ fastapi-mvc run
    [INFO] Executing shell command: ['/home/demo/.poetry/bin/poetry', 'install', '--no-interaction']
    Installing dependencies from lock file

    No dependencies to install or update

    Installing the current project: galactic-empire (0.1.0)
    [INFO] Executing shell command: ['/home/demo/.poetry/bin/poetry', 'run', 'uvicorn', '--host', '127.0.0.1', '--port', '8000', '--reload', 'galactic_empire.app.asgi:application']
    INFO:     Will watch for changes in these directories: ['/tmp/galactic-empire']
    INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
    INFO:     Started reloader process [4694] using watchgod
    INFO:     Started server process [4697]
    INFO:     Waiting for application startup.
    INFO:     Application startup complete.

This will start up `uvicron <https://github.com/encode/uvicorn>`__ development server (ASGI) distributed with fastapi-mvc by default.
To see your application in action, open a browser window and navigate to http://127.0.0.1:8000. You should see the FastAPI interactive API documentation page:

.. image:: _static/docs_page.png
    :align: center

When you want to stop the web server, hit Ctrl+C in the terminal window where it's running.
When using uvicorn development server, you don't need to restart the it; changes you make in files will be automatically picked up by the uvicorn.

The FastAPI documentation page is the smoke test for a new fastapi-mvc application: it makes sure that you have your software configured correctly enough to serve a page.

You can also check application health by running GET request to ``/api/ready`` endpoint:

.. code-block:: bash

    $ curl 127.0.0.1:8000/api/ready
    {"status":"ok"}

Creating new endpoint
---------------------

To create new endpoint, you need to create at minimum a route and controller with a method.
Lets say we want to create ``death_star`` controller with following endpoints:

* status (GET)
* load (POST)
* fire (DELETE)

For that we will run the controller generator:

.. code-block:: bash

    $ fastapi-mvc generate controller death_star status load:post fire:delete

This will do several things for you:

* Create controller: galactic_empire/app/controllers/death_star.py
* Create unit test: tests/unit/app/controllers/test_death_star.py
* Add router entry in: galactic_empire/config/router.py

The most important of these is the controller file, ``galactic_empire/app/controllers/death_star.py``.
Let's take a look at it:

.. code-block:: python

    """Death star controller implementation."""
    import logging

    from fastapi import APIRouter


    router = APIRouter(
        prefix="/death_star"
    )
    log = logging.getLogger(__name__)


    @router.get(
        "/status",
        status_code=200,
        # Decorator options:
        # https://fastapi.tiangolo.com/tutorial/path-operation-configuration/
    )
    async def status():
        # Implement endpoint logic here.
        return {"hello": "world"}


    @router.post(
        "/load",
        status_code=200,
        # Decorator options:
        # https://fastapi.tiangolo.com/tutorial/path-operation-configuration/
    )
    async def load():
        # Implement endpoint logic here.
        return {"hello": "world"}


    @router.delete(
        "/fire",
        status_code=200,
        # Decorator options:
        # https://fastapi.tiangolo.com/tutorial/path-operation-configuration/
    )
    async def fire():
        # Implement endpoint logic here.
        return {"hello": "world"}

Endpoints are just methods with ``FastAPI path decorator`` aggregated in one file that makes a controller.
For more information please refer to FastAPI documentation, some useful links:

* `create-a-path-operation <https://fastapi.tiangolo.com/tutorial/first-steps/#step-3-create-a-path-operation>`__
* `path params <https://fastapi.tiangolo.com/tutorial/path-params/>`__
* `path-operation-configuration <https://fastapi.tiangolo.com/tutorial/path-operation-configuration/>`__

Now let's look at router configuration:

.. code-block:: python
    :emphasize-lines: 6, 12

    """Application routes configuration.

    In this file all application endpoints are being defined.
    """
    from fastapi import APIRouter
    from galactic_empire.app.controllers import death_star
    from galactic_empire.app.controllers.api.v1 import ready

    router = APIRouter(prefix="/api")

    router.include_router(ready.router, tags=["ready"])
    router.include_router(death_star.router)

As you can see controller generator automatically added FastAPI router entries for you.
You can always disable this behaviour by running with the ``--skip-routes`` option.

Lastly let's try if our new endpoints actually work:

.. code-block:: bash

    $ curl 127.0.0.1:8000/api/death_star/status
    {"hello":"world"}
    $ curl -X POST 127.0.0.1:8000/api/death_star/load
    {"hello":"world"}
    $ curl -X DELETE 127.0.0.1:8000/api/death_star/fire
    {"hello":"world"}

As you can see fastapi-mvc is just a tool designed to make your FastAPI development life easier, by creating everything that's necessary to start working on a particular task.
However, generated project by fastapi-mvc is fully independent and does not require it in order to work. You can learn more about it in the next chapter.
