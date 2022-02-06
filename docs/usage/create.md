# Creating a new project

Creating a new project is simple as:

```shell
fastapi-mvc new my-project
```

Available options:
```shell
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
```

## Example

![fastapi-mvc](https://github.com/rszamszur/fastapi-mvc-template/blob/master/assets/readme.gif?raw=true)

**Example Generated Project**: [https://github.com/rszamszur/fastapi-mvc-example](https://github.com/rszamszur/fastapi-mvc-example)

### Create it

```shell
fastapi-mvc new /tmp/demo-project
```

### Run it

Run the server with:

```shell
$ cd /tmp/demo-project
$ demo-project serve
[2022-01-08 21:47:06 +0100] [2268861] [INFO] Start gunicorn WSGI with ASGI workers.
[2022-01-08 21:47:06 +0100] [2268861] [INFO] Starting gunicorn 20.1.0
[2022-01-08 21:47:06 +0100] [2268861] [INFO] Listening at: http://127.0.0.1:8000 (2268861)
[2022-01-08 21:47:06 +0100] [2268861] [INFO] Using worker: uvicorn.workers.UvicornWorker
[2022-01-08 21:47:06 +0100] [2268861] [INFO] Server is ready. Spawning workers
[2022-01-08 21:47:06 +0100] [2268867] [INFO] Booting worker with pid: 2268867
[2022-01-08 21:47:06 +0100] [2268867] [INFO] Worker spawned (pid: 2268867)
[2022-01-08 21:47:06 +0100] [2268867] [INFO] Started server process [2268867]
[2022-01-08 21:47:06 +0100] [2268867] [INFO] Waiting for application startup.
[2022-01-08 21:47:06 +0100] [2268867] [INFO] Application startup complete.
[2022-01-08 21:47:06 +0100] [2268873] [INFO] Booting worker with pid: 2268873
[2022-01-08 21:47:06 +0100] [2268873] [INFO] Worker spawned (pid: 2268873)
[2022-01-08 21:47:06 +0100] [2268873] [INFO] Started server process [2268873]
[2022-01-08 21:47:06 +0100] [2268873] [INFO] Waiting for application startup.
[2022-01-08 21:47:06 +0100] [2268873] [INFO] Application startup complete.
```

### Check it

Open you browser at [http://127.0.0.1:8000/api/ready](http://127.0.0.1:8000/api/ready)

You will see the JSON response as:
```JSON
{"status":"ok"}
```

Or test with curl:
```shell
$ curl localhost:8000/api/ready
{"status":"ok"}
```

### Interactive API docs

Now go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

You will see the automatic interactive API documentation.

### Alternative API docs

Now go to [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc).

You will see the alternative automatic documentation.


## Project structure

Created project structure:
```shell
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
```
