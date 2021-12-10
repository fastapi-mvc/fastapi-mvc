# FastAPI-MVC-template


[![Test](https://github.com/rszamszur/fastapi-mvc-template/actions/workflows/test.yml/badge.svg?branch=master)](https://github.com/rszamszur/fastapi-mvc-template/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/rszamszur/fastapi-mvc-template/branch/master/graph/badge.svg?token=7ESV30TYZS)](https://codecov.io/gh/rszamszur/fastapi-mvc-template)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![GitHub](https://img.shields.io/badge/fastapi-v.0.70.0-blue)
![GitHub](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9-blue)
![GitHub](https://img.shields.io/github/license/rszamszur/fastapi-mvc-template?color=blue)

---

FastAPI project core implemented using MVC architectural pattern with base utilities, tests, and pipeline to speed up creating new projects based on FastAPI. 
Additionally, this repo includes Kubernetes Helm chart, and a script for bootstrapping local development cluster with High Availability Redis cluster deployed using [spotathome/redis-operator](https://github.com/spotahome/redis-operator).

As of today [FastAPI](https://fastapi.tiangolo.com/) doesn't have any project generator like other known web frameworks ex: Django, Rails, etc., which makes creating new projects based on it that much more time-consuming.
The idea behind this template is that, one can fork this repo, rename package and then start implementing endpoints logic straightaway, rather than creating the whole project from scratch.
Moreover, the project is structured in MVC architectural pattern to help developers who don't know FastAPI yet but are familiar with MVC to get up to speed quickly.

Last but not least this application utilizes WSGI + ASGI combination for the best performance possible. Mainly because web servers like Nginx don't know how to async and WSGI is single synchronous callable. You can further read about this [here](https://asgi.readthedocs.io/en/latest/introduction.html).
Additionally, here are some benchmarks done by wonderful people of StackOverflow:
* https://stackoverflow.com/a/62977786/10566747
* https://stackoverflow.com/a/63427961/10566747

### Kubernetes local development cluster

[Helm chart for application](https://github.com/rszamszur/fastapi-mvc-template/tree/master/charts/fastapi-mvc-template)

Application stack in Kubernetes:
![k8s_arch](https://github.com/rszamszur/fastapi-mvc-template/blob/master/assets/k8s_arch.png?raw=true)

### Project structure

```
├── build                           Makefile build scripts
├── charts                          Helm chart for application
│   └── fastapi-mvc-template
├── fastapi_mvc_template            Python project root
│   ├── app                         FastAPI core implementation
│   │   ├── controllers             FastAPI controllers
│   │   ├── models                  FastAPI models
│   │   ├── utils                   FastAPI utilities: RedisClient, AiohttpClient
│   │   ├── exceptions              FastAPI custom exceptions and exception handlers
│   │   ├── asgi.py                 FastAPI ASGI node
│   ├── config                      FastAPI configuration: routes, variables
│   ├── cli                         Application command line interface implementation
│   ├── version.py                  Application version
│   └── wsgi.py                     Application master node: WSGI
├── tests
│   ├── integration                 Integration test implementation
│   └── unit                        Unit tests implementation
├── manifests                       Manifests for spotathome/redis-operator
├── CHANGELOG.md
├── Dockerfile
├── LICENSE
├── Makefile
├── README.md
├── requirements.txt
├── setup.py
├── TAG             
└── Vagrantfile                     Virtualized environment definiton
```

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

## Quickstart
First run `vagrant up` in project root directory and enter virtualized environment using `vagrant ssh`
Then run following commands to bootstrap local development cluster exposing `fastapi-mvc-template` application.
```sh
$ cd /syncd
$ make dev-env
```
*Note: this process may take a while on first run.*

Once development cluster is up and running you should see summary listing application address:
```
Kubernetes cluster ready

fastapi-mvc-template available under: http://fastapi-mvc-template.192.168.49.2.nip.io/

You can delete dev-env by issuing: minikube delete
```
*Note: above address may be different for your installation.*

*Note: provided virtualized env doesn't have port forwarding configured which means, that bootstrapped application stack in k8s won't be accessible on Host OS.*

Deployed application stack in Kubernetes:
```shell
vagrant@ubuntu-focal:/syncd$ make dev-env
...
...
...
Kubernetes cluster ready
FastAPI available under: http://fastapi-mvc-template.192.168.49.2.nip.io/
You can delete dev-env by issuing: make clean
vagrant@ubuntu-focal:/syncd$ kubectl get all -n fastapi-mvc-template
NAME                                                     READY   STATUS    RESTARTS   AGE
pod/fastapi-mvc-template-7f4dd8dc7f-p2kr7                1/1     Running   0          55s
pod/rfr-redisfailover-persistent-keep-0                  1/1     Running   0          3m39s
pod/rfr-redisfailover-persistent-keep-1                  1/1     Running   0          3m39s
pod/rfr-redisfailover-persistent-keep-2                  1/1     Running   0          3m39s
pod/rfs-redisfailover-persistent-keep-5d46b5bcf8-2r7th   1/1     Running   0          3m39s
pod/rfs-redisfailover-persistent-keep-5d46b5bcf8-6kqv5   1/1     Running   0          3m39s
pod/rfs-redisfailover-persistent-keep-5d46b5bcf8-sgtvv   1/1     Running   0          3m39s

NAME                                        TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)     AGE
service/fastapi-mvc-template                ClusterIP   10.110.42.252   <none>        8000/TCP    56s
service/rfs-redisfailover-persistent-keep   ClusterIP   10.110.4.24     <none>        26379/TCP   3m39s

NAME                                                READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/fastapi-mvc-template                1/1     1            1           55s
deployment.apps/rfs-redisfailover-persistent-keep   3/3     3            3           3m39s

NAME                                                           DESIRED   CURRENT   READY   AGE
replicaset.apps/fastapi-mvc-template-7f4dd8dc7f                1         1         1       55s
replicaset.apps/rfs-redisfailover-persistent-keep-5d46b5bcf8   3         3         3       3m39s

NAME                                                 READY   AGE
statefulset.apps/rfr-redisfailover-persistent-keep   3/3     3m39s

NAME                                                                  AGE
redisfailover.databases.spotahome.com/redisfailover-persistent-keep   3m39s
vagrant@ubuntu-focal:/syncd$ curl http://fastapi-mvc-template.192.168.49.2.nip.io/api/ready
{"status":"ok"}
```

## Installation

Using poetry directly:
```shell
poetry install --extras "aioredis aiohttp"
```

Or using make:
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

To bootstrap local minikube Kubernetes cluster exposing `fastapi-mvc-template` application:
```shell
cd fastapi-mvc-template
$ make dev-env
```

## CLI

This package exposes simple CLI for easier interaction:

```shell
$ fastapi --help
Usage: fastapi [OPTIONS] COMMAND [ARGS]...

  FastAPI MVC template CLI root.

Options:
  -v, --verbose  Enable verbose logging.
  --help         Show this message and exit.

Commands:
  serve  FastAPI MVC template CLI serve command.
$ fastapi serve --help
Usage: fastapi serve [OPTIONS]

  FastAPI MVC template CLI serve command.

Options:
  --host TEXT                  Host to bind.  [default: localhost]
  -p, --port INTEGER           Port to bind.  [default: 8000]
  -w, --workers INTEGER RANGE  The number of worker processes for handling
                               requests.  [default: 2;1<=x<=8]
  --help                       Show this message and exit.
```

*NOTE: Maximum number of workers may be different in your case, it's limited to `multiprocessing.cpu_count()`*

To serve application simply run:

```shell
$ fastapi serve
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
$ podman run -dit --name fastapi-mvc-template -p 8000:8000 fastapi-mvc-template:$(cat TAG)
f41e5fa7ffd512aea8f1aad1c12157bf1e66f961aeb707f51993e9ac343f7a4b
$ podman ps
CONTAINER ID  IMAGE                                 COMMAND               CREATED        STATUS            PORTS                   NAMES
f41e5fa7ffd5  localhost/fastapi-mvc-template:0.1.0  /usr/bin/fastapi ...  2 seconds ago  Up 3 seconds ago  0.0.0.0:8000->8000/tcp  fastapi-mvc-template
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
3. gunicorn.conf.py

All application configuration is available in `fastapi_mvc_template.config` submodule.

### Environment variables

#### Application configuration

| Key                  | Default                  | Description                                                    |
|----------------------|--------------------------|----------------------------------------------------------------|
| FASTAPI_HOST         | `"127.0.0.1"`            | FastAPI host to bind.                                          |
| FASTAPI_PORT         | `"8000"`                 | FastAPI port to bind.                                          |
| FASTAPI_WORKERS      | `"2"`                    | Number of gunicorn workers (uvicorn.workers.UvicornWorker)     |
| FASTAPI_DEBUG        | `"True"`                 | FastAPI logging level. You should disable this for production. |
| FASTAPI_PROJECT_NAME | `"fastapi_mvc_template"` | FastAPI project name.                                          |
| FASTAPI_VERSION      | `"0.4.0"`                | Application version.                                           |
| FASTAPI_DOCS_URL     | `"/"`                    | Path where swagger ui will be served at.                       |
| FASTAPI_USE_REDIS    | `"False"`                | Whether or not to use Redis.                                   |
| FASTAPI_GUNICORN_LOG_LEVEL | `"info"` | The granularity of gunicorn log output |
| FASTAPI_GUNICORN_LOG_FORMAT | `'%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'` | Gunicorn log format |


#### Redis configuration

| Key                        | Default       | Description                               |
|----------------------------|---------------|-------------------------------------------|
| FASTAPI_REDIS_HOTS         | `"127.0.0.1"` | Redis host.                               |
| FASTAPI_REDIS_PORT         | `"6379"`      | Redis port.                               |
| FASTAPI_REDIS_USERNAME     | `""`          | Redis username.                           |
| FASTAPI_REDIS_PASSWORD     | `""`          | Redis password.                           |
| FASTAPI_REDIS_USE_SENTINEL | `"False"`     | If provided Redis config is for Sentinel. |

### gunicorn.conf.py

1. [Source](https://github.com/rszamszur/fastapi-mvc-template/blob/master/fastapi_mvc_template/config/gunicorn.conf.py)
2. [Gunicorn configuration file documentation](https://docs.gunicorn.org/en/latest/settings.html)

### Routes definition

Endpoints are defined in `fastapi_mvc_template.config.router`. Just simply import your controller and include it to FastAPI router:

```python
from fastapi import APIRouter
from fastapi_mvc_template.app.controllers.api.v1 import ready

router = APIRouter(
    prefix="/api"
)

router.include_router(ready.router, tags=["ready"])
```

## Development

You can implement your own web routes logic straight away in `.app.controllers.api.v1` submodule. For more information please see [FastAPI documentation](https://fastapi.tiangolo.com/tutorial/).

### Utilities

For your discretion, I've provided some basic utilities:
* RedisClient `.app.utils.redis`
* AiohttpClient `.app.utils.aiohttp_client`

They're initialized in `asgi.py` on FastAPI startup event handler:

```python
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
```

and are available for whole application scope without passing object instances. In order to utilize it just execute classmethods directly.

Example:
```python
from fastapi_mvc_template.app.utils import RedisClient

response = RedisClient.get("Key")
```
```python
from fastapi_mvc_template.app.utils import AiohttpClient

response = AiohttpClient.get("http://foo.bar")
```

If you don't need it just simply remove the utility, init on start up and tests.

### Exceptions

#### [HTTPException and handler](https://github.com/rszamszur/fastapi-mvc-template/blob/master/fastapi_mvc_template/app/exceptions/http.py)

This exception combined with `http_exception_handler` method allows you to use it the same manner as you'd use `FastAPI.HTTPException` with one difference. 
You have freedom to define returned response body, whereas in `FastAPI.HTTPException` content is returned under "detail" JSON key.
In this application custom handler is added in `asgi.py` while initializing FastAPI application. 
This is needed in order to handle it globally.

[Example usage in ready controller](https://github.com/rszamszur/fastapi-mvc-template/blob/master/fastapi_mvc_template/app/controllers/api/v1/ready.py)

### Web Routes
All routes documentation is available on:
* `/` with Swagger
* `/redoc` or ReDoc.

## Renaming

To your discretion I've provided simple bash script for renaming whole project, although I do not guarantee it will work with all possible names.

It takes two parameters:
1) new project name *NOTE: if your project name contains '-' this script should automatically change '-' to '_' wherever it's needed.*
2) new project url

```shell
#!/usr/bin/env bash

if [ -n "$DEBUG" ]; then
  set -x
fi

set -o errexit
set -o nounset
set -o pipefail

if [[ -z "$1" ]]; then
  echo "Parameter project name is empty."
  exit 1
fi

if [[ -z "$2" ]]; then
  echo "Parameter project url is empty."
  exit 1
fi

grep -rl "https://github.com/rszamszur/fastapi-mvc-template" | xargs sed -i "s/https:\/\/github.com\/rszamszur\/fastapi-mvc-template/${2//\//\\/}/g"
mv charts/fastapi-mvc-template charts/$1

if [[ $1 == *"-"* ]]; then
  mv fastapi_mvc_template ${1//-/_}
  grep -rl --exclude-dir=.git fastapi_mvc_template | xargs sed -i "s/fastapi_mvc_template/${1//-/_}/g"
else
  mv fastapi_mvc_template $1
  grep -rl --exclude-dir=.git fastapi_mvc_template | xargs sed -i "s/fastapi_mvc_template/$1/g"
fi

grep -rl --exclude-dir=.git fastapi-mvc-template | xargs sed -i "s/fastapi-mvc-template/$1/g"
grep -rl --exclude-dir=.git 'FastAPI MVC template' | xargs sed -i "s/FastAPI MVC template/$1/g"
grep -rl --exclude-dir=.git 'Fastapi MVC template' | xargs sed -i "s/FastAPI MVC template/$1/g"
```
*NOTE: Afterwards you may still want to edit some docstrings or descriptions.*

## Contributing

Questions, comments or improvements? Please create an issue on Github. I do my best to include every contribution proposed in any way that I can.

## License

[MIT](https://github.com/rszamszur/fastapi-mvc-template/blob/master/LICENSE)
