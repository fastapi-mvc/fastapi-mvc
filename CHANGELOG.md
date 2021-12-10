# Changelog

This file documents changes to [fastapi-mvc-template](https://github.com/rszamszur/fastapi-mvc-template). The release numbering uses [semantic versioning](http://semver.org).

### 0.4.0

### Features

- [x] Implement model for error response rendering.
- [x] Implement custom HTTPException, and its handler to have freedom to define returned response body.
- [x] Extend application configuration from environment variables.
- [x] Add and utilize gunicorn.conf.py file for better WSGI configuration.

### Internal

- [x] Update project dependencies:
  * fastapi (0.66.0 -> 0.70.0)
  * aioredis (2.0.0a1 -> 2.0.0)
  * aiohttp (3.7.4.post0 -> 3.8.1)
  * uvicorn (0.14.0 -> 0.15.0)
- [x] Improve submodules import paths.
- [x] Move fastapi_mvc_template.app.config submodule to fastapi_mvc_template.config.
- [x] Refactor application and redis config with using pydantic.BaseSetting.
- [x] Extend unit tests, and increase coverage to 99%.
- [x] Change RedisClient.ping() method to return false instead of raising an RedisError exception.

## 0.3.0

### Features

- [x] Add python-poetry pyproject.toml and poetry.lock for dependency management and packaging.
- [x] Reduce container image size by ~500 MB with using multi-stage build.

### Internal

- [x] Remove setup.py and requirements.txt.
- [x] Refactor make install to utilize poetry instead of pip.
- [x] Update base container image digest sha.
- [x] Improve GitHub Test workflow.

## 0.2.0

### Features

- [x] Implement make dev-env target for bootstrapping a local Kubernetes cluster with High Availability Redis cluster, and deploy application.
- [x] Add Helm charts for fastapi-mvc-template.
- [x] Add Vagrantfile.

### Internal

- [x] Add manifests for spotathome/redis-operator.
- [x] Fix minor documentation/comments typos.

## 0.1.0

- [X] Initial release
