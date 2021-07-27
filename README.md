# FastAPI-MVC-template

![Build](https://github.com/rszamszur/fastapi-mvc-template/actions/workflows/build.yml/badge.svg)
![Test](https://github.com/rszamszur/fastapi-mvc-template/actions/workflows/test.yml/badge.svg)
[![codecov](https://codecov.io/gh/rszamszur/fastapi-mvc-template/branch/master/graph/badge.svg?token=7ESV30TYZS)](https://codecov.io/gh/rszamszur/fastapi-mvc-template)

FastAPI project core implemented using MVC architectural pattern with base utilities, tests, and pipeline to speed up creating new projects based on FastAPI.

As of today [FastAPI](https://fastapi.tiangolo.com/) doesn't have any project generator like other known web frameworks ex: Django, Rails, etc., which makes creating new projects based on it that much more time-consuming.
The idea behind this template is that one can fork this repo, rename package and then start implementing endpoints logic straightaway, rather than creating the whole project from scratch.
Moreover, the project is structured in MVC architectural pattern to help developers who don't know FastAPI yet but are familiar with MVC to get up to speed quickly.

Last but not least this application utilizes WSGI + ASGI combination for the best performance possible. Mainly because web servers like Nginx don't know how to async and WSGI is single synchronous callable. You can further read about this [here](https://asgi.readthedocs.io/en/latest/introduction.html).
Additionally, here are some benchmarks done by wonderful people of StackOverflow:
* https://stackoverflow.com/a/62977786/10566747
* https://stackoverflow.com/a/63427961/10566747

### Project structure

```
├── build                           Makefile build scripts
├── fastapi_mvc_template            Python project root
│   ├── app                         FastAPI core implementation
│   │   ├── config                  FastAPI configuration: routes, variables
│   │   ├── controllers             FastAPI controllers
│   │   ├── models                  FastAPI models
│   │   ├── utils                   FastAPI utilities: RedisClient, AiohttpClient
│   │   ├── asgi.py                 FastAPI ASGI node
│   ├── cli                         Application command line interface implementation
│   ├── version.py                  Application version
│   └── wsgi.py                     Application master node: WSGI
├── tests
│   ├── integration                 Integration test implementation
│   └── unit                        Unit tests implementation
├── .travis.yml                     Pipeline definition
├── CHANGELOG.md
├── Dockerfile
├── LICENSE
├── Makefile
├── README.md
├── requirements.txt
├── setup.py
├── TAG             
└── tox.ini                         Tox task automation definitions
```

## Installation

Prerequisites:
* Python 3.7 or later installed [How to install python](https://docs.python-guide.org/starting/installation/)
* Python package index installed. [How to install pip](https://pip.pypa.io/en/stable/installing/)
* Virtualenv
* make

### Using make

```shell
git clone git@github.com:rszamszur/fastapi-mvc-template.git
cd fastapi-mvc-template
make venv
```

### From source

```shell
git clone git@github.com:rszamszur/fastapi-mvc-template.git
cd fastapi-mvc-template
pip install .
# Or if you want to have build and test dependencies as well
pip install -r requirements.txt
```

## Usage

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
$ curl localhost:8080/api/ready
{"status":"ok"}
```

### Using Dockerfile

This package provides Dockerfile for virtualized environment.

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

## Development

You can implement your own web routes logic straight away in `.app.controllers.api.v1` submodule. For more information please see [FastAPI documentation](https://fastapi.tiangolo.com/tutorial/).

### Utilities

For your discretion, I've provided some basic utilities:
* RedisClient `.app.utilities.redis`
* AiohttpClient `.app.utilities.aiohttp_client`

They're initialized in `asgi.py` on FastAPI startup event handler:

```python
async def on_startup():
    """Fastapi startup event handler.

    Creates AiohttpClient session.

    """
    log.debug("Execute FastAPI startup event handler.")
    # Initialize utilities for whole FastAPI application without passing object
    # instances within the logic. Feel free to disable it if you don't need it.
    RedisClient.open_redis_client()
    AiohttpClient.get_aiohttp_client()


async def on_shutdown():
    """Fastapi shutdown event handler.

    Destroys AiohttpClient session.

    """
    log.debug("Execute FastAPI shutdown event handler.")
    # Gracefully close utilities.
    await RedisClient.close_redis_client()
    await AiohttpClient.close_aiohttp_client()
```

and are available for whole application scope without passing object instances. In order to utilize it just execute classmethods directly.

Example:
```python
from fastapi_mvc_template.app.utils.redis import RedisClient

response = RedisClient.get("Key")
```
```python
from fastapi_mvc_template.app.utils.aiohttp_client import AiohttpClient

response = AiohttpClient.get("http://foo.bar")
```

If you don't need it just simply remove the utility, init on start up and tests.

### Application configuration
All application configuration is available under `.app.config` submodule:

Global config:
```python
from fastapi_mvc_template.version import __version__


# FastAPI logging level
DEBUG = True
# FastAPI project name
PROJECT_NAME = "fastapi_mvc_template"
VERSION = __version__
# All your additional application configuration should go either here or in
# separate file in this submodule.
```

Redis config for RedisClient utility (can be overridden by env variables):

```python
import os


REDIS_HOST = os.getenv('FASTAPI_REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('FASTAPI_REDIS_PORT', 6379))
REDIS_USERNAME = os.getenv('FASTAPI_REDIS_USERNAME', None)
REDIS_PASSWORD = os.getenv('FASTAPI_REDIS_PASSWORD', None)
# If provided above Redis config is for Sentinel.
REDIS_USE_SENTINEL = bool(os.getenv('FASTAPI_REDIS_USE_SENTINEL', False))
```

Lastly web routes definition. You just simply import you controller and include it to FastAPI router:

```python
from fastapi import APIRouter
from fastapi_mvc_template.app.controllers.api.v1 import ready

router = APIRouter(
    prefix="/api"
)

router.include_router(ready.router, tags=["ready"])
```

### Web Routes
All routes documentation is available on:
* `/` with Swagger
* `/redoc` or ReDoc.

## Contributing

Questions, comments or improvements? Please create an issue on Github. I do my best to include every contribution proposed in any way that I can.

## License

[MIT](https://github.com/rszamszur/fastapi-mvc-template/blob/master/LICENSE)
