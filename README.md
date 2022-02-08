<div align="center">
<h1>fastapi-mvc</h1>

![fastapi-mvc](https://github.com/rszamszur/fastapi-mvc-template/blob/master/assets/readme.gif?raw=true)
[![CI](https://github.com/rszamszur/fastapi-mvc/actions/workflows/main.yml/badge.svg?branch=master)](https://github.com/rszamszur/fastapi-mvc/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/rszamszur/fastapi-mvc/branch/master/graph/badge.svg?token=7ESV30TYZS)](https://codecov.io/gh/rszamszur/fastapi-mvc)
[![K8s integration](https://github.com/rszamszur/fastapi-mvc/actions/workflows/integration.yml/badge.svg)](https://github.com/rszamszur/fastapi-mvc/actions/workflows/integration.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![PyPI](https://img.shields.io/pypi/v/fastapi-mvc)
![PyPI - Downloads](https://img.shields.io/pypi/dm/fastapi-mvc)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fastapi-mvc)
![GitHub](https://img.shields.io/github/license/rszamszur/fastapi-mvc?color=blue)

</div>

---

**Documentation**: [https://fastapi-mvc.netlify.app](https://fastapi-mvc.netlify.app)

**Source Code**: [https://github.com/rszamszur/fastapi-mvc](https://github.com/rszamszur/fastapi-mvc)

**Example generated project**: https://github.com/rszamszur/fastapi-mvc-example

---

## Features
<details>
  <summary>Generated project core implemented using MVC architectural pattern</summary>
  
  Generated project is structured in MVC architectural pattern to help developers who don't know FastAPI yet but are familiar with MVC to get up to speed quickly.
</details>

<details>
  <summary>WSGI + ASGI for high performance and better configuration</summary>

#### TLDR;

Running WSGI as a master worker with ASGI workers gives better results than running pure ASGI (for FastAPI for now):
* better performance (requests per second)
* better support for different protocols
* broader configuration
* better support with using reverse proxy
---
First of all, whether it's ASGI, WSGI, or combined, think of this as something that serves the application. For instance, Ruby on Rails uses Puma. The result of any of those servers is a TCP/IP or UNIX socket which is later on utilized by reverse proxy ex: Nginx (a TCP/IP socket you can access directly over the network, but still in production, usually it'll be behind a reverse proxy).

Now to WSGI + ASGI part. FastAPI is implemented with asyncio (https://docs.python.org/3/library/asyncio.html), so having a pure WSGI server doesn't make sense since you'd lose all the benefits of asynchronous concurrency. That's where ASGI comes in. However, Python journey with asyncio is still pretty young. Most projects have yet to reach maturity level (you should expect early bugs and a limited feature set). FastAPI, as ASGI server uses uvicorn, which is still prior 1.x.x release (17 in total so far, current 0.16.0) and lacks support for some protocols (ex: no HTTP/2).
Moreover, some reverse proxy might not know how to work with asynchronous servers, and some problems or early bugs on this layer might happen as well.

I'm not saying uvicorn is bad. Quite contrary, if you'd run 4 pure uvicorn workes, you'd still get great results. But if you'd run the same amount of workers with gunicorn (WSGI) as a master worker, it turns out you can even pump those numbers up.

Gunicorn with 4 Uvicorn Workers (source: https://stackoverflow.com/a/62977786/10566747):
```
Requests per second: 7891.28 [#/sec] (mean)
Time per request: 126.722 [ms] (mean)
Time per request: 0.127 [ms] (mean, across all concurrent requests)
```

Pure Uvicorn with 4 workers:
```
Requests per second: 4359.68 [#/sec] (mean)
Time per request: 229.375 [ms] (mean)
Time per request: 0.229 [ms] (mean, across all concurrent requests)
```

~80% better

I guess gunicorn does a better job in worker management. However, it's a more mature project, so it's probably a matter of time when uvicorn (or other ASGI for that matter) will catch up to this benchmark.

Last but not least, gunicorn gives a ton of settings to configure (https://docs.gunicorn.org/en/stable/settings.html), which can come in handy.
</details>

<details>
  <summary>Generated project comes with tests at 99% coverage</summary>
  
  Unit test coverage is at 99% regardless of chosen configuration. There is also a placeholder for integration tests with an example dummy test.
</details>

<details>
  <summary>Proper Dockerfile created with best practices for the cloud and Kubernetes</summary>
  
Container image features:
* Based on distroless image
* Run as PID 1 (with child processes)
* Utilizes multi-stage build for smallest size possible, also this results in having only necessary libraries/dependencies/tools in outcome container image.
* DigestSHA - immutable identifier instead of tags, for better reproducibility and security.
* Signal handling, for Kubernetes to be able to gracefully shut down pods.
* Created with common layers.
* By default runs as non-root user

Based on Google [Best practices for building containers](https://cloud.google.com/architecture/best-practices-for-building-containers), [Top 20 Dockerfile best practices](https://sysdig.com/blog/dockerfile-best-practices), and own experience.
</details>

<details>
  <summary>Extensive GitHub actions for CI</summary>
  
![ci_example](https://github.com/rszamszur/fastapi-mvc-template/blob/master/assets/ci.png?raw=true)
</details>

<details>
  <summary>Helm chart for Kubernetes</summary>
  
For easily deploying application in Kubernetes cluster.
</details>

<details>
  <summary>Reproducible virtualized development environment</summary>

Easily boot virtual machine with Vagrant. Code and test straight away. 

*Note: Project directory is rsync'ed between Host and Guest.*

*Note2: provided Vagrant vm doesn't have port forwarding configured which means, that application won't be accessible on Host OS.*
</details>

<details>
  <summary>Redis and aiohttp utilities</summary>
  
For your discretion, I've provided some basic utilities:
* RedisClient `.app.utils.redis`
* AiohttpClient `.app.utils.aiohttp_client`

They're initialized in `asgi.py` on FastAPI startup event handler, and are available for whole application scope without passing object instances between controllers.
</details>

<details>
  <summary>Kubernetes deployment with HA Redis cluster</summary>
  
Application stack in Kubernetes:
![k8s_arch](https://github.com/rszamszur/fastapi-mvc-template/blob/master/assets/k8s_arch.png?raw=true)
</details>

<details>
  <summary>Readable and documented code</summary>
  
The metrics stage in CI workflow ensures important PEP rules are enforced. For additional readability and formatting checks - black is used. Every piece of generated code is documented with docstrings. Last but not least there is also extended README with how to.
</details>

<details>
  <summary>Configurable from env</summary>
  
Generated application provides flexibility of configuration. All significant settings are defined by the environment variables, each with the default value.
</details>

<details>
  <summary>Generated project uses <a href="https://github.com/python-poetry/poetry" target="_blank">Poetry</a> dependency management</summary>

Poetry comes with all the tools you might need to manage your project in a deterministic way. Moreover, it's based on new unified Python project settings file - <a href="https://www.python.org/dev/peps/pep-0518/" target="_blank">PEP 518</a> that replaces `setup.py`.
</details>

## Quick start

```shell
pip install fastapi-mvc
fastapi-mvc new /tmp/demo-project
cd /tmp/demo-project
fastapi-mvc run
```

## Prerequisites

* Python 3.7 or later installed [How to install python](https://docs.python-guide.org/starting/installation/)
* Poetry [How to install poetry](https://python-poetry.org/docs/#installation) or pip [How to install pip](https://pip.pypa.io/en/stable/installation/) installed
* make (optional)

## Installation

```shell
pip install fastapi-mvc
```

Or directly from source:
```shell
git clone git@github.com:rszamszur/fastapi-mvc.git
cd fastapi-mvc
make install
```

## Getting started

Creating a new FastAPI project is as easy as:
```shell
fastapi-mvc new my-project
```

To run development uvicorn server:
```shell
cd my-project
fastapi-mvc run
```

To run production WSGI + ASGI server:
```shell
cd my-project
poetry run my-project serve
# or if project virtualenv PATH is set
my-project serve
```

To confirm it's working:
```shell
curl localhost:8000/api/ready
{"status":"ok"}
```

## CLI

This package exposes simple CLI for easier interaction:

```shell
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
```
```shell
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
```
```shell
$ fastapi-mvc run --help
Usage: fastapi-mvc run [OPTIONS]

  Run development uvicorn server.

  The 'fastapi-mvc run' commands runs development uvicorn server for a
  fastapi-mvc project at the current working directory.

Options:
  --host TEXT                  Host to bind.  [default: 127.0.0.1]
  -p, --port INTEGER           Port to bind.  [default: 8000]
  -w, --workers INTEGER RANGE  The number of worker processes for handling
                               requests.  [default: 1]

  --no-reload                  Disable auto-reload.
  --help                       Show this message and exit.
```

## Contributing

[CONTRIBUTING](https://github.com/rszamszur/fastapi-mvc/blob/master/CONTRIBUTING.md)

## License

[MIT](https://github.com/rszamszur/fastapi-mvc/blob/master/LICENSE)
