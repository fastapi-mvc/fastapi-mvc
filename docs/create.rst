Creating a new project
======================

Creating a new project is simple as:

.. code-block:: bash

    fastapi-mvc new demo-project

Available options:

.. code-block:: bash

    Usage: fastapi-mvc new [OPTIONS] APP_PATH

      Create a new FastAPI application.

      The 'fastapi-mvc new' command creates a new FastAPI application with a
      default directory structure and configuration at the path you specify.

    Options:
      -R, --skip-redis                Skip Redis utility files.
      -A, --skip-aiohttp              Skip aiohttp utility files.
      -V, --skip-vagrantfile          Skip Vagrantfile.
      -H, --skip-helm                 Skip Helm chart files.
      -G, --skip-actions              Skip GitHub actions files.
      -C, --skip-codecov              Skip codecov in GitHub actions.
      -I, --skip-install              Dont run make install
      --license [MIT|BSD2|BSD3|ISC|Apache2.0|LGPLv3+|LGPLv3|LGPLv2+|LGPLv2|no]
                                      Choose license.  [default: MIT]
      --repo-url TEXT                 Repository url.
      --help                          Show this message and exit.

Create it
---------

.. code-block:: bash

    $ fastapi-mvc new /tmp/demo-project
    [2022-02-14 21:30:47 +0100] [2189261] [INFO] Creating a new fastapi-mvc project: /tmp/demo-project
    [2022-02-14 21:30:47 +0100] [2189261] [INFO] Installing project
    [install] Begin installing project.
    Creating virtualenv demo-project in /tmp/demo-project/.venv
    Updating dependencies
    Resolving dependencies... (10.2s)

    Writing lock file

    Package operations: 57 installs, 0 updates, 0 removals

      • Installing frozenlist (1.3.0)
      • Installing idna (2.10)
      • Installing multidict (6.0.2)
      • Installing pyparsing (3.0.7)
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
      • Installing pycodestyle (2.7.0)
      • Installing pyflakes (2.3.1)
      • Installing snowballstemmer (2.2.0)
      • Installing toml (0.10.2)
      • Installing typing-extensions (4.1.1)
      • Installing yarl (1.7.2)
      • Installing aiohttp (3.8.1): Installing...
      • Installing asgiref (3.5.0)
      • Installing certifi (2021.10.8)
      • Installing chardet (4.0.0): Installing...
      • Installing click (7.1.2)
      • Installing coverage (6.3.1): Installing...
      • Installing coverage (6.3.1)
      • Installing flake8 (3.9.2)
      • Installing click (7.1.2)
      • Installing coverage (6.3.1)
      • Installing flake8 (3.9.2)
      • Installing chardet (4.0.0)
      • Installing click (7.1.2)
      • Installing coverage (6.3.1)
      • Installing flake8 (3.9.2)
      • Installing h11 (0.13.0)
      • Installing asgiref (3.5.0)
      • Installing certifi (2021.10.8)
      • Installing chardet (4.0.0)
      • Installing click (7.1.2)
      • Installing coverage (6.3.1)
      • Installing flake8 (3.9.2)
      • Installing h11 (0.13.0)
      • Installing aiohttp (3.8.1)
      • Installing asgiref (3.5.0)
      • Installing certifi (2021.10.8)
      • Installing chardet (4.0.0)
      • Installing click (7.1.2)
      • Installing coverage (6.3.1)
      • Installing flake8 (3.9.2)
      • Installing h11 (0.13.0)
      • Installing httptools (0.2.0)
      • Installing mypy-extensions (0.4.3)
      • Installing pathspec (0.9.0)
      • Installing platformdirs (2.5.0)
      • Installing pydantic (1.9.0)
      • Installing pydocstyle (6.1.1)
      • Installing pytest (6.2.5)
      • Installing python-dotenv (0.19.2)
      • Installing pyyaml (6.0)
      • Installing starlette (0.16.0)
      • Installing tomli (1.2.3)
      • Installing urllib3 (1.26.8)
      • Installing uvloop (0.16.0)
      • Installing watchgod (0.7)
      • Installing websockets (10.1)
      • Installing aioredis (2.0.1)
      • Installing aioresponses (0.7.3)
      • Installing black (21.12b0)
      • Installing fastapi (0.70.1)
      • Installing flake8-docstrings (1.6.0)
      • Installing flake8-import-order (0.18.1)
      • Installing flake8-todo (0.7)
      • Installing gunicorn (20.1.0)
      • Installing mock (4.0.3)
      • Installing pytest-asyncio (0.15.1)
      • Installing pytest-cov (2.12.1)
      • Installing requests (2.25.1)
      • Installing uvicorn (0.15.0)

    Installing the current project: demo-project (0.1.0)
    Project successfully installed.
    To activate virtualenv run: $ poetry shell
    Now you should access CLI script: $ demo-project --help
    Alternatively you can access CLI script via poetry run: $ poetry run demo-project --help
    To deactivate virtualenv simply type: $ deactivate
    To activate shell completion:
     - for bash: $ echo 'eval "$(_DEMO_PROJECT_COMPLETE=source_bash demo-project)' >> ~/.bashrc
     - for zsh: $ echo 'eval "$(_DEMO_PROJECT_COMPLETE=source_zsh demo-project)' >> ~/.zshrc
     - for fish: $ echo 'eval "$(_DEMO_PROJECT_COMPLETE=source_fish demo-project)' >> ~/.config/fish/completions/demo-project.fish

Run it
------

To run development uvicorn server:

.. code-block:: bash

    $ cd /tmp/demo-project/
    $ fastapi-mvc run
    [2022-02-14 21:32:14 +0100] [2191860] [INFO] Starting uvicorn development server.
    INFO:     Will watch for changes in these directories: ['/tmp/demo-project']
    INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
    INFO:     Started reloader process [2191879] using watchgod
    INFO:     Started server process [2191887]
    INFO:     Waiting for application startup.
    INFO:     Application startup complete.

To run production WSGI + ASGI server:

.. code-block:: bash

    $ cd /tmp/demo-project/
    $ poetry run demo-project serve
    # or if project virtualenv PATH is set
    $ demo-project serve
    [2022-02-14 21:33:08 +0100] [2193401] [INFO] Start gunicorn WSGI with ASGI workers.
    [2022-02-14 21:33:08 +0100] [2193401] [INFO] Starting gunicorn 20.1.0
    [2022-02-14 21:33:08 +0100] [2193401] [INFO] Listening at: http://127.0.0.1:8000 (2193401)
    [2022-02-14 21:33:08 +0100] [2193401] [INFO] Using worker: uvicorn.workers.UvicornWorker
    [2022-02-14 21:33:08 +0100] [2193401] [INFO] Server is ready. Spawning workers
    [2022-02-14 21:33:08 +0100] [2193410] [INFO] Booting worker with pid: 2193410
    [2022-02-14 21:33:08 +0100] [2193410] [INFO] Worker spawned (pid: 2193410)
    [2022-02-14 21:33:09 +0100] [2193410] [INFO] Started server process [2193410]
    [2022-02-14 21:33:09 +0100] [2193410] [INFO] Waiting for application startup.
    [2022-02-14 21:33:09 +0100] [2193410] [INFO] Application startup complete.
    [2022-02-14 21:33:09 +0100] [2193416] [INFO] Booting worker with pid: 2193416
    [2022-02-14 21:33:09 +0100] [2193416] [INFO] Worker spawned (pid: 2193416)
    [2022-02-14 21:33:09 +0100] [2193416] [INFO] Started server process [2193416]
    [2022-02-14 21:33:09 +0100] [2193416] [INFO] Waiting for application startup.
    [2022-02-14 21:33:09 +0100] [2193416] [INFO] Application startup complete.

Check it
--------

Open you browser at `http://127.0.0.1:8000/api/ready <http://127.0.0.1:8000/api/ready>`__:

You will see the JSON response as:

.. code-block:: bash

    {"status":"ok"}

Or test with curl:

.. code-block:: bash

    $ curl localhost:8000/api/ready
    {"status":"ok"}

Interactive API docs
--------------------

Now go to `http://127.0.0.1:8000/ <http://127.0.0.1:8000/>`__:

You will see the automatic interactive API documentation.

Alternative API docs
--------------------

Now go to `http://127.0.0.1:8000/redoc <http://127.0.0.1:8000/redoc>`__:

You will see the alternative automatic documentation.


Project structure
-----------------

Created project structure:

.. code-block:: bash

    ├── .github
    │   └── workflows                GitHub Actions definition
    ├── build                        Makefile scripts
    ├── charts                       Helm chart for application
    │   └── demo-project
    ├── demo_project                 Python project root
    │   ├── app                      FastAPI core implementation
    │   │   ├── controllers          Application controllers
    │   │   ├── exceptions           Application custom exceptions
    │   │   ├── models               Application models
    │   │   ├── utils                Application utilities
    │   │   └── asgi.py              Application ASGI node implementation
    │   ├── cli                      Application CLI implementation
    │   ├── config                   Configuration submodule
    │   │   ├── application.py       Application configuration
    │   │   ├── gunicorn.conf.py     Gunicorn configuration
    │   │   ├── redis.py             Redis configuration
    │   │   └── router.py            FastAPI router configuration
    │   ├── version.py               Application version
    │   └── wsgi.py                  Application WSGI master node implementation
    ├── manifests                    Manifests for spotathome/redis-operator
    ├── tests
    │   ├── integration              Integration test implementation
    │   ├── unit                     Unit tests implementation
    ├── CHANGELOG.md
    ├── Dockerfile                   Dockerfile definition
    ├── .dockerignore
    ├── .gitignore
    ├── LICENSE
    ├── Makefile                     Makefile definition
    ├── poetry.lock                  Poetry dependency management lock file
    ├── pyproject.toml               PEP 518 - The build system dependencies
    ├── README.md
    ├── TAG                          Application version for build systems
    └── Vagrantfile                  Virtualized environment definiton
