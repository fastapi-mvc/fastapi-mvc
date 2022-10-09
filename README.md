<div align="center">

![fastapi-mvc](https://github.com/fastapi-mvc/fastapi-mvc/blob/master/docs/_static/logo.png?raw=true)

![fastapi-mvc](https://github.com/fastapi-mvc/fastapi-mvc/blob/master/docs/_static/readme.gif?raw=true)
[![CI](https://github.com/fastapi-mvc/fastapi-mvc/actions/workflows/main.yml/badge.svg?branch=master)](https://github.com/fastapi-mvc/fastapi-mvc/actions/workflows/main.yml)
[![❄️ Nix CI ❄️](https://github.com/fastapi-mvc/fastapi-mvc/actions/workflows/nix.yml/badge.svg)](https://github.com/fastapi-mvc/fastapi-mvc/actions/workflows/nix.yml)
[![codecov](https://codecov.io/gh/fastapi-mvc/fastapi-mvc/branch/master/graph/badge.svg?token=7ESV30TYZS)](https://codecov.io/gh/fastapi-mvc/fastapi-mvc)
[![K8s integration](https://github.com/fastapi-mvc/fastapi-mvc/actions/workflows/integration.yml/badge.svg)](https://github.com/fastapi-mvc/fastapi-mvc/actions/workflows/integration.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![PyPI](https://img.shields.io/pypi/v/fastapi-mvc)
![PyPI - Downloads](https://img.shields.io/pypi/dm/fastapi-mvc)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fastapi-mvc)
![GitHub](https://img.shields.io/github/license/fastapi-mvc/fastapi-mvc?color=blue)

</div>

---

**Documentation**: [https://fastapi-mvc.netlify.app](https://fastapi-mvc.netlify.app)

**Source Code**: [https://github.com/fastapi-mvc/fastapi-mvc](https://github.com/fastapi-mvc/fastapi-mvc)

**Project scaffold**: [https://github.com/fastapi-mvc/copier-project](https://github.com/fastapi-mvc/copier-project)

**Example generated project**: [https://github.com/fastapi-mvc/example](https://github.com/fastapi-mvc/example)

---

Fastapi-mvc is a developer productivity tool for FastAPI web framework. 
It is designed to make programming FastAPI applications easier by making assumptions about what every developer needs to get started. 
It allows you to write less code while accomplishing more. Core features:

* Generated project based on MVC architectural pattern
* WSGI + ASGI production server
* Generated project comes with Sphinx documentation and 100% unit tests coverage
* Kubernetes deployment with Redis HA cluster
* Makefile, GitHub actions and utilities
* Helm chart for Kubernetes deployment
* Dockerfile with K8s and cloud in mind
* Generate pieces of code or even your own generators
* Uses Poetry dependency management
* Includes set of Nix expressions
* Virtualized reproducible development environment using Vagrant

Fastapi-mvc comes with a number of scripts called generators that are designed to make your development life easier by 
creating everything that’s necessary to start working on a particular task. One of these is the new application generator, 
which will provide you with the foundation of a fresh FastAPI application so that you don’t have to write it yourself.

Creating a new project is as easy as:

```shell
$ fastapi-mvc new /tmp/galactic-empire
```

This will create a fastapi-mvc project called galactic-empire in a `/tmp/galactic-empire` directory and install its dependencies using `make install`.

Once project is generated and installed lets run development uvicorn server (ASGI):

```shell
$ cd /tmp/galactic-empire
$ fastapi-mvc run
```

To confirm it’s actually working:

```shell
$ curl 127.0.0.1:8000/api/ready
{"status":"ok"}
```

Now let's add new API endpoints. For that we need to generate new controller:

```shell
$ fastapi-mvc generate controller death_star status load:post fire:delete
```

And then test generated controller endpoints:

```shell
$ curl 127.0.0.1:8000/api/death_star/status
{"hello":"world"}
$ curl -X POST 127.0.0.1:8000/api/death_star/load
{"hello":"world"}
$ curl -X DELETE 127.0.0.1:8000/api/death_star/fire
{"hello":"world"}
```

You will see it working in server logs as well:

```shell
INFO:     127.0.0.1:47284 - "GET /api/ready HTTP/1.1" 200 OK
INFO:     127.0.0.1:55648 - "GET /api/death_star/status HTTP/1.1" 200 OK
INFO:     127.0.0.1:55650 - "POST /api/death_star/load HTTP/1.1" 200 OK
INFO:     127.0.0.1:55652 - "DELETE /api/death_star/fire HTTP/1.1" 200 OK
```

You can get the project directly from PyPI:

```shell
pip install fastapi-mvc
```

## Projects created with fastapi-mvc

If you have created a project with fastapi-mvc, feel free to open PR and add yourself to the list. Share your story and project. Your success is my success :)

Projects:
* [fastapi-mvc/example](https://github.com/fastapi-mvc/example) - Default generated project by `fastapi-mvc new ...`

## Contributing

[CONTRIBUTING](https://github.com/fastapi-mvc/fastapi-mvc/blob/master/CONTRIBUTING.md)

## License

[MIT](https://github.com/fastapi-mvc/fastapi-mvc/blob/master/LICENSE)
