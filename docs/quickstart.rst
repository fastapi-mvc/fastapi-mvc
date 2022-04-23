Quickstart
==========

Prerequisites
-------------

* Python 3.7 or later `(How to install python) <https://docs.python-guide.org/starting/installation/>`__:
* make

Environment with `Nix <https://nixos.org/>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To start a shell with development environment run:

.. code-block:: bash

    nix-shell shell.nix

Installation
------------

Installation is as simple as:

.. code-block:: bash

    pip install fastapi-mvc

Or directly from source:

.. code-block:: bash

    git clone git@github.com:rszamszur/fastapi-mvc.git
    cd fastapi-mvc
    make install

CLI
---

This package exposes simple CLI for easier interaction:

.. code-block:: bash

    $ fastapi-mvc --help
    Usage: fastapi-mvc [OPTIONS] COMMAND [ARGS]...

      Create and develop production grade FastAPI projects.

      Documentation: https://fastapi-mvc.netlify.app

      Source Code: https://github.com/rszamszur/fastapi-mvc

    Options:
      -v, --verbose  Enable verbose logging.
      --help         Show this message and exit.

    Commands:
      new  Create a new FastAPI application.
      run  Run development uvicorn server.

    $ fastapi-mvc new --help
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

    $ fastapi-mvc run --help
    Usage: fastapi-mvc run [OPTIONS]

      Run development uvicorn server.

      The 'fastapi-mvc run' commands runs development uvicorn server for a
      fastapi-mvc project at the current working directory.

    Options:
      --host TEXT      Host to bind.  [default: 127.0.0.1]
      -p, --port TEXT  Port to bind.  [default: 8000]
      --help           Show this message and exit.
