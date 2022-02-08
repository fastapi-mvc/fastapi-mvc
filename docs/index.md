# fastapi-mvc


[![CI](https://github.com/rszamszur/fastapi-mvc/actions/workflows/main.yml/badge.svg?branch=master)](https://github.com/rszamszur/fastapi-mvc/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/rszamszur/fastapi-mvc/branch/master/graph/badge.svg?token=7ESV30TYZS)](https://codecov.io/gh/rszamszur/fastapi-mvc)
[![K8s integration](https://github.com/rszamszur/fastapi-mvc/actions/workflows/integration.yml/badge.svg)](https://github.com/rszamszur/fastapi-mvc/actions/workflows/integration.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![PyPI](https://img.shields.io/pypi/v/fastapi-mvc)
![PyPI - Downloads](https://img.shields.io/pypi/dm/fastapi-mvc)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fastapi-mvc)
![GitHub](https://img.shields.io/github/license/rszamszur/fastapi-mvc?color=blue)

---

**Source Code**: [https://github.com/rszamszur/fastapi-mvc](https://github.com/rszamszur/fastapi-mvc)

**Example Generated Project**: [https://github.com/rszamszur/fastapi-mvc-example](https://github.com/rszamszur/fastapi-mvc-example)

---

Documentation for version: **v0.8.0**

Create and develop production grade FastaAPI projects, based on MVC architectural pattern, WSGI + ASGI. 
Includes tests, GitHub actions, utilities, Helm, Dockerfile, Makefile, and more.

## Quick start

Creating a new FastAPI project is as easy as:
```shell
pip install fastapi-mvc
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
# or if Poetry PATH is set
my-project serve
```

To confirm it's working:
```shell
curl localhost:8000/api/ready
{"status":"ok"}
```

## Features

**Generated project core implemented using MVC architectural pattern**
  
: Generated project is structured in MVC architectural pattern to help developers who don't know FastAPI yet but are familiar with MVC to get up to speed quickly.


**WSGI + ASGI for high performance and better configuration**

: **TLDR;**

: Running WSGI as a master worker with ASGI workers gives better results than running pure ASGI:

:  * better performance (requests per second)
  * better support for different protocols
  * broader configuration
  * better support with using reverse proxy

---

<details>
<summary>More details</summary>

First of all, whether it's ASGI, WSGI, or combined, think of this as something that serves the application. For instance, Ruby on Rails uses Puma. The result of any of those servers is a TCP/IP or UNIX socket which is later on utilized by reverse proxy ex: Nginx (a TCP/IP socket you can access directly over the network, but still in production, usually it'll be behind a reverse proxy).
</br>
</br>
Now to WSGI + ASGI part. FastAPI is implemented with <a href="https://docs.python.org/3/library/asyncio.html" target="_blank">asyncio</a>, so having a pure WSGI server doesn't make sense since you'd lose all the benefits of asynchronous concurrency. That's where ASGI comes in. However, Python journey with asyncio is still pretty young. Most projects have yet to reach maturity level (you should expect early bugs and a limited feature set). FastAPI, as ASGI server uses uvicorn, which is still prior 1.x.x release (17 in total so far, current 0.16.0) and lacks support for some protocols (ex: no HTTP/2).
Moreover, some reverse proxy might not know how to work with asynchronous servers, and some problems or early bugs on this layer might happen as well.
</br>
</br>
I'm not saying uvicorn is bad. Quite contrary, if you'd run 4 pure uvicorn workes, you'd still get great results. But if you'd run the same amount of workers with gunicorn (WSGI) as a master worker, it turns out you can even pump those numbers up.
</br>
</br>
Gunicorn with 4 Uvicorn Workers <a href="https://stackoverflow.com/a/62977786/10566747" target="_blank">(source)</a>:
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
</br>
</br>
I guess gunicorn does a better job in worker management. However, it's a more mature project, so it's probably a matter of time when uvicorn (or other ASGI for that matter) will catch up to this benchmark.
</br>
</br>
Last but not least, gunicorn gives a ton of <a href="https://docs.gunicorn.org/en/stable/settings.html" target="_blank">settings to configure</a>, which can come in handy.

</details>

**Generated project comes with tests at 99% coverage**
  
: Unit test coverage is at 99% regardless of chosen configuration. There is also a placeholder for integration tests with an example dummy test.


**Proper Dockerfile created with best practices for the cloud and Kubernetes**
  
: Container image features:

: * Based on distroless image
  * Run as PID 1 (with child processes)
  * Utilizes multi-stage build for smallest size possible, also this results in having only necessary libraries/dependencies/tools in outcome container image.
  * DigestSHA - immutable identifier instead of tags, for better reproducibility and security.
  * Signal handling, for Kubernetes to be able to gracefully shut down pods.
  * Created with common layers.
  * By default runs as non-root user

: Based on Google [Best practices for building containers](https://cloud.google.com/architecture/best-practices-for-building-containers), [Top 20 Dockerfile best practices](https://sysdig.com/blog/dockerfile-best-practices), and own experience.

**Extensive GitHub actions for CI**
  
: ![ci_example](https://github.com/rszamszur/fastapi-mvc-template/blob/master/assets/ci.png?raw=true)

**Helm chart for Kubernetes**
  
: For easily deploying application in Kubernetes cluster.

**Reproducible virtualized development environment**

: Easily boot virtual machine with Vagrant. Code and test straight away. 

: *Note: Project directory is rsync'ed between Host and Guest.*

: *Note2: provided Vagrant vm doesn't have port forwarding configured which means, that application won't be accessible on Host OS.*

**Redis and aiohttp utilities**
  
: For your discretion, I've provided some basic utilities:

: * RedisClient `.app.utils.redis`
  * AiohttpClient `.app.utils.aiohttp_client`

: They're initialized in `asgi.py` on FastAPI startup event handler, and are available for whole application scope without passing object instances between controllers.

**Kubernetes deployment with HA Redis cluster**
  
: Application stack in Kubernetes:
: ![k8s_arch](https://github.com/rszamszur/fastapi-mvc-template/blob/master/assets/k8s_arch.png?raw=true)

**Readable and documented code**
  
: The metrics stage in CI workflow ensures important PEP rules are enforced. For additional readability and formatting checks - black is used. Every piece of generated code is documented with docstrings. Last but not least there is also extended README with how to.

**Configurable from env**
  
: Generated application provides flexibility of configuration. All significant settings are defined by the environment variables, each with the default value.

**Generated project uses [Poetry](https://github.com/python-poetry/poetry) dependency management**

: Poetry comes with all the tools you might need to manage your project in a deterministic way. Moreover, it's based on new unified Python project settings file - [PEP 518](href="https://www.python.org/dev/peps/pep-0518/) that replaces `setup.py`.

## License

[MIT](https://github.com/rszamszur/fastapi-mvc/blob/master/LICENSE)
