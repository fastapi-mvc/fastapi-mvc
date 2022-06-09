# {{cookiecutter.project_name}}

{%- if cookiecutter.github_actions == "yes" %}
[![CI]({{cookiecutter.repo_url}}/actions/workflows/main.yml/badge.svg?branch=master)]({{cookiecutter.repo_url}}/actions/workflows/main.yml)
{%- endif %}
{%- if cookiecutter.github_actions == "yes" and cookiecutter.helm == "yes" %}
[![K8s integration]({{cookiecutter.repo_url}}/actions/workflows/integration.yml/badge.svg)]({{cookiecutter.repo_url}}/actions/workflows/integration.yml)
{%- endif %}
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![GitHub](https://img.shields.io/badge/fastapi-v.0.75.0-blue)
![GitHub](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9-blue)
![GitHub](https://img.shields.io/badge/license-{{cookiecutter.license}}-blue)

## This project was generated with [fastapi-mvc](https://github.com/rszamszur/fastapi-mvc)

---

## Prerequisites

If You want to go easy way and use provided virtualized environment You'll need to have installed:
* rsync 
* Vagrant [How to install vagrant](https://www.vagrantup.com/downloads)
* (Optional) Enabled virtualization in BIOS

Otherwise, for local complete project environment with k8s infrastructure bootstrapping You'll need:

For application:
* Python 3.7 or later installed [How to install python](https://docs.python-guide.org/starting/installation/)
* Poetry [How to install poetry](https://python-poetry.org/docs/#installation)

For infrastructure:
* make, gcc, golang
* minikube version 1.22.0 [How_to_install_minikube](https://minikube.sigs.k8s.io/docs/start/)
* helm version 3.0.0 or higher [How_to_install_helm](https://helm.sh/docs/intro/install/)
* kubectl version 1.16 up to 1.20.8 [How_to_install_kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)
* Container runtime interface. NOTE! dev-env script uses docker for minikube, for other CRI you'll need to modify this line in dev-env.sh `MINIKUBE_IN_STYLE=0 minikube start --driver=docker 2>/dev/null`

### Environment with [Nix](https://nixos.org/)

To start a shell with development environment run:
```shell
nix-shell shell.nix
```

## Quickstart
First run `vagrant up` in project root directory and enter virtualized environment using `vagrant ssh`
Then run following commands to bootstrap local development cluster exposing `fastapi-mvc` application.
```sh
$ cd /syncd
$ make dev-env
```
*Note: this process may take a while on first run.*

Once development cluster is up and running you should see summary listing application address:
```
Kubernetes cluster ready

fastapi-mvc available under: http://{{cookiecutter.folder_name}}.192.168.49.2.nip.io/

You can delete dev-env by issuing: minikube delete
```
*Note: above address may be different for your installation.*

*Note: provided virtualized env doesn't have port forwarding configured which means, that bootstrapped application stack in k8s won't be accessible on Host OS.*

Deployed application stack in Kubernetes:
{%- if cookiecutter.redis == "yes" %}
```shell
vagrant@ubuntu-focal:/syncd$ make dev-env
...
...
...
Kubernetes cluster ready
FastAPI available under: http://{{cookiecutter.folder_name}}.192.168.49.2.nip.io/
You can delete dev-env by issuing: make clean
vagrant@ubuntu-focal:/syncd$ kubectl get all -n {{cookiecutter.folder_name}}
NAME                                                     READY   STATUS    RESTARTS   AGE
pod/{{cookiecutter.folder_name}}-7f4dd8dc7f-p2kr7                1/1     Running   0          55s
pod/rfr-redisfailover-persistent-keep-0                  1/1     Running   0          3m39s
pod/rfr-redisfailover-persistent-keep-1                  1/1     Running   0          3m39s
pod/rfr-redisfailover-persistent-keep-2                  1/1     Running   0          3m39s
pod/rfs-redisfailover-persistent-keep-5d46b5bcf8-2r7th   1/1     Running   0          3m39s
pod/rfs-redisfailover-persistent-keep-5d46b5bcf8-6kqv5   1/1     Running   0          3m39s
pod/rfs-redisfailover-persistent-keep-5d46b5bcf8-sgtvv   1/1     Running   0          3m39s

NAME                                        TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)     AGE
service/{{cookiecutter.folder_name}}                ClusterIP   10.110.42.252   <none>        8000/TCP    56s
service/rfs-redisfailover-persistent-keep   ClusterIP   10.110.4.24     <none>        26379/TCP   3m39s

NAME                                                READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/{{cookiecutter.folder_name}}                1/1     1            1           55s
deployment.apps/rfs-redisfailover-persistent-keep   3/3     3            3           3m39s

NAME                                                           DESIRED   CURRENT   READY   AGE
replicaset.apps/{{cookiecutter.folder_name}}-7f4dd8dc7f                1         1         1       55s
replicaset.apps/rfs-redisfailover-persistent-keep-5d46b5bcf8   3         3         3       3m39s

NAME                                                 READY   AGE
statefulset.apps/rfr-redisfailover-persistent-keep   3/3     3m39s

NAME                                                                  AGE
redisfailover.databases.spotahome.com/redisfailover-persistent-keep   3m39s
vagrant@ubuntu-focal:/syncd$ curl http://{{cookiecutter.folder_name}}.192.168.49.2.nip.io/api/ready
{"status":"ok"}
```

{%- else %}
```shell
vagrant@ubuntu-focal:/syncd$ make dev-env
...
...
...
Kubernetes cluster ready
FastAPI available under: http://{{cookiecutter.folder_name}}.192.168.49.2.nip.io/
You can delete dev-env by issuing: make clean
vagrant@ubuntu-focal:/syncd$ kubectl get all -n {{cookiecutter.folder_name}}
NAME                        READY   STATUS    RESTARTS   AGE
pod/{{cookiecutter.folder_name}}-649966bb7f-r694l   1/1     Running   0          114s

NAME           TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)    AGE
service/{{cookiecutter.folder_name}}   ClusterIP   10.97.16.46   <none>        8000/TCP   114s

NAME                   READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/{{cookiecutter.folder_name}}   1/1     1            1           114s

NAME                              DESIRED   CURRENT   READY   AGE
replicaset.apps/{{cookiecutter.folder_name}}-649966bb7f   1         1         1       114s
vagrant@ubuntu-focal:/syncd$ curl http://{{cookiecutter.folder_name}}.192.168.49.2.nip.io/api/ready
{"status":"ok"}
```

{%- endif %}

## Installation

With make:
```shell
make install
```

You can customize poetry installation with [environment variables](https://python-poetry.org/docs/configuration/#using-environment-variables) 
```shell
export POETRY_HOME=/custom/poetry/path
export POETRY_CACHE_DIR=/custom/poetry/path/cache
export POETRY_VIRTUALENVS_IN_PROJECT=true
make install
```

Or using poetry directly:
```shell
poetry install
```

To bootstrap local minikube Kubernetes cluster exposing `{{cookiecutter.folder_name}}` application:
```shell
make dev-env
```

## CLI

This package exposes simple CLI for easier interaction:

```shell
$ {{cookiecutter.script_name}} --help
Usage: {{cookiecutter.script_name}} [OPTIONS] COMMAND [ARGS]...

  {{cookiecutter.project_name.capitalize()}} CLI root.

Options:
  -v, --verbose  Enable verbose logging.
  --help         Show this message and exit.

Commands:
  serve  {{cookiecutter.project_name}} CLI serve command.
$ {{cookiecutter.script_name}} serve --help
Usage: {{cookiecutter.script_name}} serve [OPTIONS]

  Run production gunicorn (WSGI) server with uvicorn (ASGI) workers.

Options:
  --bind TEXT                  Host to bind.
  -w, --workers INTEGER RANGE  The number of worker processes for handling
                               requests.
  -D, --daemon                 Daemonize the Gunicorn process.
  -e, --env TEXT               Set environment variables in the execution
                               environment.
  --pid PATH                   Specifies the PID file.
  --help                       Show this message and exit.
```

*NOTE: Maximum number of workers may be different in your case, it's limited to `multiprocessing.cpu_count()`*

To serve application simply run:

```shell
$ {{cookiecutter.script_name}} serve
```

To confirm it's working:

```shell
$ curl localhost:8000/api/ready
{"status":"ok"}
```

## Dockerfile

This repository provides Dockerfile for virtualized environment.

*NOTE: Replace podman with docker if it's yours containerization engine.*
```shell
$ make image
$ podman run -dit --name {{cookiecutter.docker_image_name}} -p 8000:8000 {{cookiecutter.docker_image_name}}:$(cat TAG)
f41e5fa7ffd512aea8f1aad1c12157bf1e66f961aeb707f51993e9ac343f7a4b
$ podman ps
CONTAINER ID  IMAGE                                 COMMAND               CREATED        STATUS            PORTS                   NAMES
f41e5fa7ffd5  localhost/{{cookiecutter.docker_image_name}}:0.1.0  /usr/bin/fastapi ...  2 seconds ago  Up 3 seconds ago  0.0.0.0:8000->8000/tcp  {{cookiecutter.docker_image_name}}
$ curl localhost:8000/api/ready
{"status":"ok"}
```

## Application configuration

This application provides flexibility of configuration. 
All significant settings are defined by the environment variables, each with the default value. 
Moreover, package CLI allows overriding core ones: host, port, workers. 
You can modify all other available configuration settings in the gunicorn.conf.py file.

Priority of overriding configuration:
1. cli
2. environment variables
3. gunicorn.py

All application configuration is available in `{{cookiecutter.package_name}}.config` submodule.

### Environment variables

#### Application configuration

| Key                  | Default                                                         | Description                                                                                         |
|----------------------|-----------------------------------------------------------------|-----------------------------------------------------------------------------------------------------|
| FASTAPI_BIND         | `"127.0.0.1:8000"`                                              | The socket to bind. A string of the form: 'HOST', 'HOST:PORT', 'unix:PATH'. An IP is a valid HOST.  |
| FASTAPI_WORKERS      | `"2"`                                                           | Number of gunicorn workers (uvicorn.workers.UvicornWorker)     |
| FASTAPI_DEBUG        | `"True"`                                                        | FastAPI logging level. You should disable this for production. |
| FASTAPI_PROJECT_NAME | `"{{cookiecutter.project_name}}"`                               | FastAPI project name.                                          |
| FASTAPI_VERSION      | `"0.4.0"`                                                       | Application version.                                           |
| FASTAPI_DOCS_URL     | `"/"`                                                           | Path where swagger ui will be served at.                       |
| FASTAPI_USE_REDIS    | `"False"`                                                       | Whether or not to use Redis.                                   |
| FASTAPI_GUNICORN_LOG_LEVEL | `"info"`                                                        | The granularity of gunicorn log output |
| FASTAPI_GUNICORN_LOG_FORMAT | `'%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'` | Gunicorn log format |
{%- if cookiecutter.redis == "yes" %}

#### Redis configuration

| Key                        | Default       | Description                               |
|----------------------------|---------------|-------------------------------------------|
| FASTAPI_REDIS_HOTS         | `"127.0.0.1"` | Redis host.                               |
| FASTAPI_REDIS_PORT         | `"6379"`      | Redis port.                               |
| FASTAPI_REDIS_USERNAME     | `""`          | Redis username.                           |
| FASTAPI_REDIS_PASSWORD     | `""`          | Redis password.                           |
| FASTAPI_REDIS_USE_SENTINEL | `"False"`     | If provided Redis config is for Sentinel. |
{%- endif %}

### gunicorn.conf.py

1. Source: `{{cookiecutter.package_name}}.config/gunicorn.conf.py`
2. [Gunicorn configuration file documentation](https://docs.gunicorn.org/en/latest/settings.html)

### Routes definition

Endpoints are defined in `{{cookiecutter.package_name}}.app.router`. Just simply import your controller and include it to FastAPI router:

```python
from fastapi import APIRouter
from {{cookiecutter.package_name}}.app.controllers.api.v1 import ready

root_api_router = APIRouter(
    prefix="/api"
)

root_api_router.include_router(ready.router, tags=["ready"])
```

## Development

You can implement your own web routes logic straight away in `{{cookiecutter.package_name}}.app.controllers.api.v1` submodule. For more information please see [FastAPI documentation](https://fastapi.tiangolo.com/tutorial/).
{%- if cookiecutter.redis == "yes" or cookiecutter.aiohttp == "yes" %}

### Utilities

For your discretion, I've provided some basic utilities:
{%- if cookiecutter.redis == "yes" %}
* RedisClient `{{cookiecutter.package_name}}.app.utils.redis`
{%- endif %}
{%- if cookiecutter.aiohttp == "yes" %}
* AiohttpClient `{{cookiecutter.package_name}}.app.utils.aiohttp_client`
{%- endif %}

They're initialized in `asgi.py` on FastAPI startup event handler:

```python
async def on_startup():
    """Fastapi startup event handler.

    Creates RedisClient and AiohttpClient session.

    """
    log.debug("Execute FastAPI startup event handler.")
    # Initialize utilities for whole FastAPI application without passing object
    # instances within the logic. Feel free to disable it if you don't need it.
    {%- if cookiecutter.redis == "yes" and cookiecutter.aiohttp == "yes" %}
    if settings.USE_REDIS:
        await RedisClient.open_redis_client()

    AiohttpClient.get_aiohttp_client()
    {%- elif cookiecutter.redis == "yes" %}
    if settings.USE_REDIS:
        await RedisClient.open_redis_client()
    {%- elif cookiecutter.aiohttp == "yes" %}
    AiohttpClient.get_aiohttp_client()
    {%- else %}
    pass
    {%- endif %}


async def on_shutdown():
    """Fastapi shutdown event handler.

    Destroys RedisClient and AiohttpClient session.

    """
    log.debug("Execute FastAPI shutdown event handler.")
    # Gracefully close utilities.
    {%- if cookiecutter.redis == "yes" and cookiecutter.aiohttp == "yes" %}
    if settings.USE_REDIS:
        await RedisClient.close_redis_client()

    await AiohttpClient.close_aiohttp_client()
    {%- elif cookiecutter.redis == "yes" %}
    if settings.USE_REDIS:
        await RedisClient.close_redis_client()
    {%- elif cookiecutter.aiohttp == "yes" %}
    await AiohttpClient.close_aiohttp_client()
    {%- else %}
    pass
    {%- endif %}
```

and are available for whole application scope without passing object instances. In order to utilize it just execute classmethods directly.

Example:
{%- if cookiecutter.redis == "yes" %}
```python
from {{cookiecutter.package_name}}.app.utils import RedisClient

response = RedisClient.get("Key")
```
{%- endif %}
{%- if cookiecutter.aiohttp == "yes" %}
```python
from {{cookiecutter.package_name}}.app.utils import AiohttpClient

response = AiohttpClient.get("http://foo.bar")
```
{%- endif %}
{%- endif %}

### Exceptions

#### HTTPException and handler

Source: `{{cookiecutter.package_name}}.app.exceptions.http.py`

This exception combined with `http_exception_handler` method allows you to use it the same manner as you'd use `FastAPI.HTTPException` with one difference. 
You have freedom to define returned response body, whereas in `FastAPI.HTTPException` content is returned under "detail" JSON key.
In this application custom handler is added in `asgi.py` while initializing FastAPI application. 
This is needed in order to handle it globally.

### Web Routes
All routes documentation is available on:
* `/` with Swagger
* `/redoc` or ReDoc.

## License

This project is licensed under the terms of the {{cookiecutter.license}} license.
