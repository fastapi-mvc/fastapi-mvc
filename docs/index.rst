Welcome to fastapi-mvc
======================

.. image:: _static/readme.gif
    :align: center
    :target: https://fastapi-mvc.netlify.app/

--------------

.. image:: https://github.com/fastapi-mvc/fastapi-mvc/actions/workflows/main.yml/badge.svg?branch=master
   :target: https://github.com/fastapi-mvc/fastapi-mvc/actions/workflows/main.yml

.. image:: https://github.com/fastapi-mvc/fastapi-mvc/actions/workflows/nix.yml/badge.svg?branch=master
   :target: https://github.com/fastapi-mvc/fastapi-mvc/actions/workflows/nix.yml

.. image:: https://github.com/fastapi-mvc/fastapi-mvc/actions/workflows/integration.yml/badge.svg?branch=master
   :target: https://github.com/fastapi-mvc/fastapi-mvc/actions/workflows/integration.yml

.. image:: https://codecov.io/gh/fastapi-mvc/fastapi-mvc/branch/master/graph/badge.svg?token=7ESV30TYZS
    :target: https://codecov.io/gh/fastapi-mvc/fastapi-mvc

.. image:: https://img.shields.io/pypi/v/fastapi-mvc
    :alt: PyPI

.. image:: https://img.shields.io/pypi/dm/fastapi-mvc
    :alt: PyPI - Downloads

.. image:: https://img.shields.io/pypi/pyversions/fastapi-mvc
    :alt: PyPI - Python Version

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

.. image:: https://img.shields.io/github/stars/fastapi-mvc/fastapi-mvc?style=social
   :target: https://github.com/fastapi-mvc/fastapi-mvc/stargazers/

**Project scaffold:** `https://github.com/fastapi-mvc/copier-project <https://github.com/fastapi-mvc/copier-project>`__

**Example generated project:** `https://github.com/fastapi-mvc/example <https://github.com/fastapi-mvc/example>`__

--------------

Fastapi-mvc is a developer productivity tool for `FastAPI <https://fastapi.tiangolo.com/>`__ web framework.
It is designed to make programming `FastAPI <https://fastapi.tiangolo.com/>`__ applications easier by making assumptions about what every developer needs to get started.
It allows you to write less code while accomplishing more. Core features:

* Generated project based on MVC architectural pattern
* WSGI + ASGI production server
* Generated project comes with docstrings and 100% unit tests coverage
* Kubernetes deployment with Redis HA cluster
* Makefile, GitHub actions and utilities
* Helm chart for Kubernetes deployment
* Dockerfile with K8s and cloud in mind
* Generate pieces of code or even your own generators
* Uses `Poetry <https://github.com/python-poetry/poetry>`__ dependency management
* Includes set of Nix expressions
* Virtualized reproducible development environment using Vagrant

Fastapi-mvc comes with a number of scripts called generators that are designed to make your development life easier by creating everything that's necessary to start working on a particular task.
One of these is the new application generator, which will provide you with the foundation of a fresh `FastAPI <https://fastapi.tiangolo.com/>`__ application so that you don't have to write it yourself.

Creating a new project is as easy as:

.. code-block:: bash

    $ fastapi-mvc new /tmp/galactic-empire

This will create a fastapi-mvc project called galactic-empire in a ``/tmp/galactic-empire`` directory and install its dependencies using ``make install``.

Once project is generated and installed lets run development uvicorn server (ASGI):

.. code-block:: bash

    $ cd /tmp/galactic-empire
    $ fastapi-mvc run

To confirm it's actually working:

.. code-block:: bash

    $ curl 127.0.0.1:8000/api/ready
    {"status":"ok"}

Now let's add new API endpoints. For that we need to generate new controller:

.. code-block:: bash

    $ fastapi-mvc generate controller death_star status load:post fire:delete

And then test generated controller endpoints:

.. code-block:: bash

    $ curl 127.0.0.1:8000/api/death_star/status
    {"hello":"world"}
    $ curl -X POST 127.0.0.1:8000/api/death_star/load
    {"hello":"world"}
    $ curl -X DELETE 127.0.0.1:8000/api/death_star/fire
    {"hello":"world"}

You will also see it in server logs:

.. code-block:: bash

    INFO:     127.0.0.1:47284 - "GET /api/ready HTTP/1.1" 200 OK
    INFO:     127.0.0.1:55648 - "GET /api/death_star/status HTTP/1.1" 200 OK
    INFO:     127.0.0.1:55650 - "POST /api/death_star/load HTTP/1.1" 200 OK
    INFO:     127.0.0.1:55652 - "DELETE /api/death_star/fire HTTP/1.1" 200 OK

You can get the project directly from PyPI:

.. code-block:: bash

    pip install fastapi-mvc

Documentation
-------------

This part of the documentation guides you through all of the features and usage.

.. toctree::
   :maxdepth: 2

   about
   quickstart
   cli
   generators

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

   contributing
   license
   changelog
