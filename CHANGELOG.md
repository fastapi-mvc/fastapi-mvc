# Changelog

This file documents changes to [fastapi-mvc](https://github.com/rszamszur/fastapi-mvc). The release numbering uses [semantic versioning](http://semver.org).

## Unreleased

### Features

- [x] Implement all major HTTP methods in aiohttp utility #17. PR #22

### Fixed

- [x] Template style guide: W293 error. PR #20

### Internal

- [x] Improve make target scripts both for package and template #18. PR #20

## 0.5.0

### Features

- [x] Refactor project from the pure template into the package which generates fastapi-mvc projects from cookiecutter template #6. PR #10

### Fixed

- [x] Add missing FASTAPI_USE_REDIS env var in Helm chart config map and deployment.

### Internal

- [x] Rename project to fastapi-mvc.
- [x] Add FASTAPI_DEBUG env var in Helm chart config map and deployment.
- [x] Add K8s integration test workflow.
- [x] Rename Test workflow to CI.
- [x] Extend make targets for package and template.
- [x] Add minor improvements to package and template GitHub CI workflows.
- [x] Add GitHub workflows for publishing to PyPi #8. PR #11

## 0.4.0

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
- [x] Move fastapi_mvc.app.config submodule to fastapi_mvc.config.
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
- [x] Add Helm charts for fastapi-mvc.
- [x] Add Vagrantfile.

### Internal

- [x] Add manifests for spotathome/redis-operator.
- [x] Fix minor documentation/comments typos.

## 0.1.0

- [X] Initial release
