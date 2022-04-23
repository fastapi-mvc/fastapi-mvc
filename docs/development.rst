Development
===========

Once a new project is generated, you can jump straight into API endpoints development. Below you'll find some information that should help you get started.

*Note: Some features might not be available depending on chosen options during creation.*

Prerequisites
-------------

If You want to go easy way and use provided virtualized environment You'll need to have installed:

* rsync
* Vagrant `(How to install vagrant) <https://www.vagrantup.com/downloads>`__:
* (Optional) Enabled virtualization in BIOS

Otherwise, for local complete project environment with Kubernetes infrastructure bootstrapping You'll need:

For application:

* Python 3.7 or later `(How to install python) <https://docs.python-guide.org/starting/installation/>`__:
* make

For infrastructure:

* make, gcc, golang
* minikube version 1.22.0 `(How to install_minikube) <https://minikube.sigs.k8s.io/docs/start/>`__:
* helm version 3.0.0 or higher `(How to install helm) <https://helm.sh/docs/intro/install/>`__:
* kubectl version 1.16 up to 1.20.8 `(How to install kubectl) <https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/>`__:
* Container runtime interface. NOTE! dev-env script uses docker for minikube, for other CRI you'll need to modify this line in dev-env.sh `MINIKUBE_IN_STYLE=0 minikube start --driver=docker 2>/dev/null`

Environment with `Nix <https://nixos.org/>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To start a shell with development environment run:

.. code-block:: bash

    nix-shell shell.nix

Quick start
-----------

First run `vagrant up` in project root directory and enter virtualized environment using `vagrant ssh` Then run following commands to bootstrap local development cluster exposing `fastapi-mvc` application.

.. code-block:: bash

    cd /syncd
    make dev-env

*Note: this process may take a while on first run.*

Once development cluster is up and running you should see summary listing application address:

.. code-block:: bash

    Kubernetes cluster ready

    fastapi-mvc available under: http://demo-project.192.168.49.2.nip.io/

    You can delete dev-env by issuing: minikube delete

*Note: above address may be different for your installation.*

*Note: provided virtualized env doesn't have port forwarding configured which means, that bootstrapped application stack in k8s won't be accessible on Host OS.*

Deployed application stack in Kubernetes:

.. code-block:: bash

    vagrant@ubuntu-focal:/syncd$ make dev-env
    ...
    ...
    ...
    Kubernetes cluster ready
    FastAPI available under: http://demo-project.192.168.49.2.nip.io/
    You can delete dev-env by issuing: make clean
    vagrant@ubuntu-focal:/syncd$ kubectl get all -n demo-project
    NAME                                                     READY   STATUS    RESTARTS   AGE
    pod/demo-project-7f4dd8dc7f-p2kr7                1/1     Running   0          55s
    pod/rfr-redisfailover-persistent-keep-0                  1/1     Running   0          3m39s
    pod/rfr-redisfailover-persistent-keep-1                  1/1     Running   0          3m39s
    pod/rfr-redisfailover-persistent-keep-2                  1/1     Running   0          3m39s
    pod/rfs-redisfailover-persistent-keep-5d46b5bcf8-2r7th   1/1     Running   0          3m39s
    pod/rfs-redisfailover-persistent-keep-5d46b5bcf8-6kqv5   1/1     Running   0          3m39s
    pod/rfs-redisfailover-persistent-keep-5d46b5bcf8-sgtvv   1/1     Running   0          3m39s

    NAME                                        TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)     AGE
    service/demo-project                ClusterIP   10.110.42.252   <none>        8000/TCP    56s
    service/rfs-redisfailover-persistent-keep   ClusterIP   10.110.4.24     <none>        26379/TCP   3m39s

    NAME                                                READY   UP-TO-DATE   AVAILABLE   AGE
    deployment.apps/demo-project                1/1     1            1           55s
    deployment.apps/rfs-redisfailover-persistent-keep   3/3     3            3           3m39s

    NAME                                                           DESIRED   CURRENT   READY   AGE
    replicaset.apps/demo-project-7f4dd8dc7f                1         1         1       55s
    replicaset.apps/rfs-redisfailover-persistent-keep-5d46b5bcf8   3         3         3       3m39s

    NAME                                                 READY   AGE
    statefulset.apps/rfr-redisfailover-persistent-keep   3/3     3m39s

    NAME                                                                  AGE
    redisfailover.databases.spotahome.com/redisfailover-persistent-keep   3m39s
    vagrant@ubuntu-focal:/syncd$ curl http://demo-project.192.168.49.2.nip.io/api/ready
    {"status":"ok"}

Installation
------------

With make:

.. code-block:: bash

    make install

You can customize poetry installation with `environment variables <https://python-poetry.org/docs/configuration/#using-environment-variables>`__:

.. code-block:: bash

    export POETRY_HOME=/custom/poetry/path
    export POETRY_CACHE_DIR=/custom/poetry/path/cache
    export POETRY_VIRTUALENVS_IN_PROJECT=true
    make install

Or using poetry directly:

.. code-block:: bash

    poetry install

To bootstrap local minikube Kubernetes cluster exposing `demo-project` application:

.. code-block:: bash

    make dev-env

CLI
---

Generated `demo-project` application exposes simple CLI for easier interaction:

.. code-block:: bash

    $ demo-project --help
    Usage: demo-project [OPTIONS] COMMAND [ARGS]...

      demo-project CLI root.

    Options:
      -v, --verbose  Enable verbose logging.
      --help         Show this message and exit.

    Commands:
      serve  demo-project CLI serve command.

    $ demo-project serve --help
    Usage: demo-project serve [OPTIONS]

      demo-project CLI serve command.

    Options:
      --host TEXT                  Host to bind.  [default: 127.0.0.1]
      -p, --port INTEGER           Port to bind.  [default: 8000]
      -w, --workers INTEGER RANGE  The number of worker processes for handling
                                   requests.  [default: 2]

      -D, --daemon                 Daemonize the Gunicorn process.
      -e, --env TEXT               Set environment variables in the execution
                                   environment.

      -c, --config PATH            Uses a custom gunicorn.conf.py configuration
      --pid PATH                   Specifies the PID file.
      --help                       Show this message and exit.

*NOTE: Maximum number of workers may be different in your case, it's limited to multiprocessing.cpu_count()*

Dockerfile
----------

Generated project comes with Dockerfile for virtualized environment.

*NOTE: Replace podman with docker if it's yours containerization engine.*

.. code-block:: bash

    $ make image
    $ podman run -dit --name demo-project -p 8000:8000 demo-project:$(cat TAG)
    f41e5fa7ffd512aea8f1aad1c12157bf1e66f961aeb707f51993e9ac343f7a4b
    $ podman ps
    CONTAINER ID  IMAGE                                 COMMAND               CREATED        STATUS            PORTS                   NAMES
    f41e5fa7ffd5  localhost/demo-project:0.1.0  /usr/bin/fastapi ...  2 seconds ago  Up 3 seconds ago  0.0.0.0:8000->8000/tcp  demo-project
    $ curl localhost:8000/api/ready
    {"status":"ok"}

Development
-----------

You can implement your own web routes logic straight away in `demo_project.app.controllers.api.v1` submodule. For more information please see `FastAPI documentation <https://fastapi.tiangolo.com/tutorial/>`__:.

Makefile
~~~~~~~~

Provided Makefile is a starting point for application and infrastructure development:

.. code-block:: bash

    Usage:
      make <target>
      help             Display this help
      image            Build demo-project image
      clean-image      Clean demo-project image
      install          Install demo-project with poetry
      metrics          Run demo-project metrics checks
      unit-test        Run demo-project unit tests
      integration-test  Run demo-project integration tests
      dev-env          Start a local Kubernetes cluster using minikube and deploy application
      clean            Remove .cache directory and cached minikube

Utilities
~~~~~~~~~

For your discretion, I've provided some basic utilities:

* RedisClient `demo_project.app.utils.redis`
* AiohttpClient `demo_project.app.utils.aiohttp_client`

They're initialized in `asgi.py` on FastAPI startup event handler:

.. code-block:: python
    :emphasize-lines: 11, 13, 25, 27

    async def on_startup():
        """Fastapi startup event handler.

        Creates RedisClient and AiohttpClient session.

        """
        log.debug("Execute FastAPI startup event handler.")
        # Initialize utilities for whole FastAPI application without passing object
        # instances within the logic. Feel free to disable it if you don't need it.
        if settings.USE_REDIS:
            await RedisClient.open_redis_client()

        AiohttpClient.get_aiohttp_client()


    async def on_shutdown():
        """Fastapi shutdown event handler.

        Destroys RedisClient and AiohttpClient session.

        """
        log.debug("Execute FastAPI shutdown event handler.")
        # Gracefully close utilities.
        if settings.USE_REDIS:
            await RedisClient.close_redis_client()

        await AiohttpClient.close_aiohttp_client()

and are available for whole application scope without passing object instances. In order to utilize it just execute classmethods directly.

Example:

.. code-block:: python

    from demo_project.app.utils import RedisClient

    response = RedisClient.get("Key")

.. code-block:: python

    from demo_project.app.utils import RedisClient

    response = RedisClient.get("Key")

Exceptions
~~~~~~~~~~

**HTTPException and handler**

Source: `demo_project.app.exceptions.http.py`

This exception combined with `http_exception_handler` method allows you to use it the same manner as you'd use `FastAPI.HTTPException` with one difference.
You have freedom to define returned response body, whereas in `FastAPI.HTTPException` content is returned under "detail" JSON key.
In this application custom handler is added in `asgi.py` while initializing FastAPI application. This is needed in order to handle it globally.

Web Routes
~~~~~~~~~~

All routes documentation is available on:

* `/` with Swagger
* `/redoc` or ReDoc.
