Welcome to fastapi-mvc
======================

.. image:: _static/readme.gif
    :align: center
    :scale: 50%
    :target: https://fastapi-mvc.netlify.app/

--------------

.. image:: https://github.com/rszamszur/fastapi-mvc/actions/workflows/main.yml/badge.svg?branch=master
   :target: https://github.com/rszamszur/fastapi-mvc/actions/workflows/main.yml

.. image:: https://github.com/rszamszur/fastapi-mvc/actions/workflows/integration.yml/badge.svg?branch=master
   :target: https://github.com/rszamszur/fastapi-mvc/actions/workflows/integration.yml

.. image:: https://codecov.io/gh/rszamszur/fastapi-mvc/branch/master/graph/badge.svg?token=7ESV30TYZS
    :target: https://codecov.io/gh/rszamszur/fastapi-mvc

.. image:: https://img.shields.io/pypi/v/fastapi-mvc
    :alt: PyPI

.. image:: https://img.shields.io/pypi/dm/fastapi-mvc
    :alt: PyPI - Downloads

.. image:: https://img.shields.io/pypi/pyversions/fastapi-mvc
    :alt: PyPI - Python Version

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

**Example generated project:** `https://github.com/rszamszur/fastapi-mvc-example <https://github.com/rszamszur/fastapi-mvc-example>`__

--------------

Create and develop production grade `FastAPI <https://fastapi.tiangolo.com/>`__ projects, core features:

* Based on MVC architectural pattern
* WSGI + ASGI production server
* Generated project comes with docstrings and 99% unit tests coverage
* Kubernetes deployment with Redis HA cluster
* Makefile, GitHub actions and utilities
* Helm chart for Kubernetes deployment
* Dockerfile with K8s and cloud in mind
* Generate pieces of code or even your own generators
* Uses `Poetry <https://github.com/python-poetry/poetry>`__ dependency management
* Reproducible development environment using Vagrant or Nix

Fastapi-mvc comes with a number of scripts called generators that are designed to make your development life easier by creating everything that's necessary to start working on a particular task.
One of these is the new application generator, which will provide you with the foundation of a fresh `FastAPI <https://fastapi.tiangolo.com/>`__ application so that you don't have to write it yourself.

Creating a new project is as easy as:

.. code-block:: bash

    $ fastapi-mvc new /tmp/demo-project

This will create a `FastAPI <https://fastapi.tiangolo.com/>`__ application called demo-project in a ``/tmp/demo-project`` directory and install its dependencies using ``make install``.

Once project is generated and installed lets run development uvicorn server (ASGI):

.. code-block:: bash

    $ cd /tmp/demo-project
    $ fastapi-mvc run
    [INFO] Executing shell command: ['poetry', 'run', 'uvicorn', '--host', '127.0.0.1', '--port', '8000', '--reload', 'demo_project.app.asgi:application'].
    INFO:     Will watch for changes in these directories: ['/tmp/demo-project']
    INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
    INFO:     Started reloader process [4713] using watchgod
    INFO:     Started server process [4716]
    INFO:     Waiting for application startup.
    INFO:     Application startup complete.

To confirm it's actually working:

.. code-block:: bash

    $ curl 127.0.0.1:8000/api/ready
    {"status":"ok"}

Great, now lets add new API endpoints. For that we need to generate new controller:

.. code-block:: bash

    $ fastapi-mvc generate controller stock_market ticker buy:post sell:delete

And then test generated controller endpoints:

.. code-block:: bash

    $ curl localhost:8000/api/stock_market/ticker
    {"hello":"world"}
    $ curl -X POST localhost:8000/api/stock_market/buy
    {"hello":"world"}
    $ curl -X DELETE localhost:8000/api/stock_market/sell
    {"hello":"world"}

You will also see it in server logs:

.. code-block:: bash

    INFO:     127.0.0.1:47284 - "GET /api/ready HTTP/1.1" 200 OK
    INFO:     127.0.0.1:47286 - "GET /api/stock_market/ticker HTTP/1.1" 200 OK
    INFO:     127.0.0.1:47294 - "POST /api/stock_market/buy HTTP/1.1" 200 OK
    INFO:     127.0.0.1:47296 - "DELETE /api/stock_market/sell HTTP/1.1" 200 OK

You can get the project directly from PyPI:

.. code-block:: bash

    pip install fastapi-mvc

Documentation
-------------

This part of the documentation guides you through all of the features and usage.

.. toctree::
   :maxdepth: 2

   features
   quickstart
   create
   development
   configuration
   deployment

API Reference
-------------

If you are looking for information on a specific function, class, or
method, this part of the documentation is for you.

.. toctree::
   :maxdepth: 2

   api

Miscellaneous Pages
-------------------

.. toctree::
   :maxdepth: 2

   CONTRIBUTING.md
   license
   CHANGELOG.md
