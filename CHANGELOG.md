# Changelog

This file documents changes to [fastapi-mvc-template](https://github.com/rszamszur/fastapi-mvc-template). The release numbering uses [semantic versioning](http://semver.org).

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
