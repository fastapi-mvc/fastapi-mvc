# Changelog

This file documents changes to [fastapi-mvc](https://github.com/rszamszur/fastapi-mvc). The release numbering uses [semantic versioning](http://semver.org).

## 0.15.0 (09.09.2022)

### Breaking Changes

* Improve custom generator class discovery in `load_generators` method [#137](https://github.com/rszamszur/fastapi-mvc/issues/137). PR [#138](https://github.com/rszamszur/fastapi-mvc/pull/138)
  - This changes the module attribute from which the custom generator class is being discovered. For older custom generators, just replace `__all__ = ...` with `generator_class = ...` in custom generator `__init__.py`.

### Fixed

* Method `get_git_user_info()` raises `FileNotFoundError` exception if `git` command does not exists [#85](https://github.com/rszamszur/fastapi-mvc/issues/85). PR [#140](https://github.com/rszamszur/fastapi-mvc/pull/140)

### Internal

* Add `flake8` pyflakes checks to `make metrics` target [#135](https://github.com/rszamszur/fastapi-mvc/issues/135). PR [#136](https://github.com/rszamszur/fastapi-mvc/pull/136)
* Update project template dependencies:
  * fastapi (0.75.0 -> 0.82.0)
  * uvicorn (0.17.0 -> 0.18.3)
  * aioredis (2.0.0 -> 2.0.1)
  * aiohttp (3.8.0 -> 3.8.1)

## 0.14.1 (11.08.2022)

## Features

* Allow `pkgs.python` to be configurable in `shell.nix`. PR [#132](https://github.com/rszamszur/fastapi-mvc/pull/132)

## Fixed

* Fix `POETRY_HOME` environment variable in shell.nix nix expression [#131](https://github.com/rszamszur/fastapi-mvc/issues/131). PR [#132](https://github.com/rszamszur/fastapi-mvc/pull/132)

### Internal

* Refactor string formatting with f-Strings [#133](https://github.com/rszamszur/fastapi-mvc/issues/133). PR [#134](https://github.com/rszamszur/fastapi-mvc/pull/134)
* Update macos runner in integration workflows [#125](https://github.com/rszamszur/fastapi-mvc/issues/125). PR [#126](https://github.com/rszamszur/fastapi-mvc/pull/126)
* Add minor improvements. PR [#127](https://github.com/rszamszur/fastapi-mvc/pull/127)

## 0.14.0 (31.07.2022)

### Features

* Add `-N, --skip-nix` flag for `fastapi-mvc new` command [#123](https://github.com/rszamszur/fastapi-mvc/issues/123). PR [#124](https://github.com/rszamszur/fastapi-mvc/pull/124)
* Add nix expression for `fastapi-mvc` package [#114](https://github.com/rszamszur/fastapi-mvc/issues/114). PR [#116](https://github.com/rszamszur/fastapi-mvc/pull/116)
* Add nix expression for package generated from `fastapi-mvc` project template. [#115](https://github.com/rszamszur/fastapi-mvc/issues/115). PR [#116](https://github.com/rszamszur/fastapi-mvc/pull/116)
* Add container image nix expression for `fastapi-mvc` and project template [#56](https://github.com/rszamszur/fastapi-mvc/issues/56). PR [#116](https://github.com/rszamszur/fastapi-mvc/pull/116)

### Internal

* Improve Vagrantfile in project template [#121](https://github.com/rszamszur/fastapi-mvc/issues/121). PR [#122](https://github.com/rszamszur/fastapi-mvc/pull/122)

## 0.13.1 (13.06.2022)

### Security

* [CVE-2022-24065](http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-24065) OS Command Injection in cookiecutter. Update vulnerable dependency:
  * cookiecutter (1.7.3 -> 2.1.1)

## 0.13.0 (09.06.2022)

### Features

* Add support for binding gunicorn server to a UNIX socket [#25](https://github.com/rszamszur/fastapi-mvc/issues/25). PR [#105](https://github.com/rszamszur/fastapi-mvc/pull/105)

### Fixed

* Missing cookiecutter kwarg in generator template [#102](https://github.com/rszamszur/fastapi-mvc/issues/102). PR [#103](https://github.com/rszamszur/fastapi-mvc/pull/103)

### Internal

* Add generators feature documentation [#75](https://github.com/rszamszur/fastapi-mvc/issues/75). PR [#101](https://github.com/rszamszur/fastapi-mvc/pull/101)
* Add integration tests for generators [#76](https://github.com/rszamszur/fastapi-mvc/issues/76). PR [#104](https://github.com/rszamszur/fastapi-mvc/pull/104)

## 0.12.0 (10.05.2022)

### Features

* Add Sphinx autodoc documentation for project template [#89](https://github.com/rszamszur/fastapi-mvc/issues/89). PR [#99](https://github.com/rszamszur/fastapi-mvc/pull/99)

### Internal

* Extend and improve k8s integration workflow [#93](https://github.com/rszamszur/fastapi-mvc/issues/93). PR [#94](https://github.com/rszamszur/fastapi-mvc/pull/94)
* Improve generators implementation [#96](https://github.com/rszamszur/fastapi-mvc/issues/96). PR [#97](https://github.com/rszamszur/fastapi-mvc/pull/97)
* Refactor fastapi-mvc project template into generators submodule [#77](https://github.com/rszamszur/fastapi-mvc/issues/77). PR [#98](https://github.com/rszamszur/fastapi-mvc/pull/98)
* Refactor and improve project template structure [#90](https://github.com/rszamszur/fastapi-mvc/issues/90). PR [#99](https://github.com/rszamszur/fastapi-mvc/pull/99)
* Increase project template unit tests coverage to 100%. PR [#99](https://github.com/rszamszur/fastapi-mvc/pull/99)
* Update package dependencies:
  * click (7.1.2 -> 8.1.3)
  * black (21.12b0 -> 22.3.0)
* Update project template dependencies:
  * click (7.1.2 -> 8.1.3)
  * black (21.12b0 -> 22.3.0)

## 0.11.1 (27.04.2022)

### Fixed

* Controller generator creating duplicates entries in config/router.py [#78](https://github.com/rszamszur/fastapi-mvc/issues/78). PR [#92](https://github.com/rszamszur/fastapi-mvc/pull/92)

### Internal

* Remove redundant `# -*- coding: utf-8 -*-` in file headers [#66](https://github.com/rszamszur/fastapi-mvc/issues/66). PR [#91](https://github.com/rszamszur/fastapi-mvc/pull/91)

## 0.11.0 (24.04.2022)

### Features

* Implement controller generator [#47](https://github.com/rszamszur/fastapi-mvc/issues/47). PR [#70](https://github.com/rszamszur/fastapi-mvc/pull/70)
* Implement generator generator [#68](https://github.com/rszamszur/fastapi-mvc/issues/68). PR [#70](https://github.com/rszamszur/fastapi-mvc/pull/70)
* Implement logic for loading user generators into fastapi-mvc CLI at RunTime [#69](https://github.com/rszamszur/fastapi-mvc/issues/69). PR [#70](https://github.com/rszamszur/fastapi-mvc/pull/70)

### Internal

* Implement global except hook, refactor current exceptions handling [#73](https://github.com/rszamszur/fastapi-mvc/issues/73). PR [#70](https://github.com/rszamszur/fastapi-mvc/pull/70)
* Refactor `Invoker` class with using queue [#71](https://github.com/rszamszur/fastapi-mvc/issues/71). PR [#70](https://github.com/rszamszur/fastapi-mvc/pull/70)
* Refactor `fastapi_mvc.commands` to be more generic [#72](https://github.com/rszamszur/fastapi-mvc/issues/72). PR [#70](https://github.com/rszamszur/fastapi-mvc/pull/70)
* Refactor existing documentation with Sphinx [#74](https://github.com/rszamszur/fastapi-mvc/issues/74). PR [#83](https://github.com/rszamszur/fastapi-mvc/pull/83)
* Migrate to `install-poetry.py` script prior Poetry 1.2.x release migration [#87](https://github.com/rszamszur/fastapi-mvc/issues/87). PR [#88](https://github.com/rszamszur/fastapi-mvc/pull/88)

### Fixed

* CLI `fastapi-mvc run` command doesn't distinguish whether project is installed or crashed due to error [#82](https://github.com/rszamszur/fastapi-mvc/issues/82). PR [#86](https://github.com/rszamszur/fastapi-mvc/pull/86)
* CLI `fastapi-mvc run` command should use absolute path to poetry binary [#84](https://github.com/rszamszur/fastapi-mvc/issues/84). PR [#86](https://github.com/rszamszur/fastapi-mvc/pull/86)

## 0.10.0 (07.04.2022)

### Fixed

* New project cannot install with Python version > 3.10 [#60](https://github.com/rszamszur/fastapi-mvc/issues/60). PR [#61](https://github.com/rszamszur/fastapi-mvc/pull/61) by [@Merinorus](https://github.com/Merinorus)
* Metrics job for Python 3.10 [#63](https://github.com/rszamszur/fastapi-mvc/issues/63). PR [#65](https://github.com/rszamszur/fastapi-mvc/pull/65) by [@Merinorus](https://github.com/Merinorus)

### Features

* Add nix shell config for local development environment [#57](https://github.com/rszamszur/fastapi-mvc/issues/57). PR [#58](https://github.com/rszamszur/fastapi-mvc/pull/58)
* Allow overriding poetry version for make install target via env variable: $POETRY_VERSION [#59](https://github.com/rszamszur/fastapi-mvc/issues/59). PR [#58](https://github.com/rszamszur/fastapi-mvc/pull/58)

### Internal

* Update template dependencies:
  * fastapi (0.70.0 -> 0.75.0)
  * uvicorn (0.15.0 -> 0.17.0)
* Add minor `ShellUtils` unit test case improvement.
* Add python 3.10 in CI tests [#62](https://github.com/rszamszur/fastapi-mvc/issues/62). PR [#61](https://github.com/rszamszur/fastapi-mvc/pull/61) by [@Merinorus](https://github.com/Merinorus)

## 0.9.0 (14.02.2022)

### Fixed

* CLI`fastapi-mvc run` command implementation [#48](https://github.com/rszamszur/fastapi-mvc/issues/48). PR [#52](https://github.com/rszamszur/fastapi-mvc/pull/52)
* GitHub main workflow package coverage sources. PR [#52](https://github.com/rszamszur/fastapi-mvc/pull/52)

### Internal

* Implement all `fastapi-mvc.ini` parser properties [#50](https://github.com/rszamszur/fastapi-mvc/issues/50). PR [#52](https://github.com/rszamszur/fastapi-mvc/pull/52)
* Refactor execution logic from CLI into command design pattern [#51](https://github.com/rszamszur/fastapi-mvc/issues/51). PR [#52](https://github.com/rszamszur/fastapi-mvc/pull/52)

## 0.8.0 (08.02.2022)

### Features

* Implement CLI `fastapi-mvc run` command for running uvicorn development server [#14](https://github.com/rszamszur/fastapi-mvc/issues/14), [#31](https://github.com/rszamszur/fastapi-mvc/issues/31). PR [#35](https://github.com/rszamszur/fastapi-mvc/pull/35)

### Fixed

* New project doesn't install correctly if created from activated virtualenv [#37](https://github.com/rszamszur/fastapi-mvc/issues/37). PR [#40](https://github.com/rszamszur/fastapi-mvc/pull/40)
* CLI `fastapi-mvc new` `--license` option value is not passed to cookiecutter [#39](https://github.com/rszamszur/fastapi-mvc/issues/39). PR [#42](https://github.com/rszamszur/fastapi-mvc/pull/42)

### Internal

* Refactor logic from CLI commands to separate classes [#38](https://github.com/rszamszur/fastapi-mvc/issues/38). PR [#40](https://github.com/rszamszur/fastapi-mvc/pull/40)
* Add documentation [#9](https://github.com/rszamszur/fastapi-mvc/issues/9). PR [#33](https://github.com/rszamszur/fastapi-mvc/pull/33)
* Add make template-checks target for running metrics and tests on template.
* Add make pre-commit target for running package and template checks.
* Add make test target for running package unit and integration tests.
* Improve make scripts logging information.

## 0.7.0 (31.01.2022)

### Features

* Implement new template CLI serve command options [#24](https://github.com/rszamszur/fastapi-mvc/issues/24). PR [#27](https://github.com/rszamszur/fastapi-mvc/pull/27)

### Fixed

* Incomplete command in template `build/unit-test.sh` make script [#28](https://github.com/rszamszur/fastapi-mvc/issues/28). PR [#27](https://github.com/rszamszur/fastapi-mvc/pull/27)
* Debian snapshot repository is expired causing container image build failure [#29](https://github.com/rszamszur/fastapi-mvc/issues/29). PR [#27](https://github.com/rszamszur/fastapi-mvc/pull/27)

### Internal

* Lint tests. PR #30

## 0.6.0 (27.01.2022)

### Features

* Implement all major HTTP methods in aiohttp utility [#17](https://github.com/rszamszur/fastapi-mvc/issues/17). PR [#22](https://github.com/rszamszur/fastapi-mvc/pull/22)
* Make container image reproducible both for package and template [#15](https://github.com/rszamszur/fastapi-mvc/issues/15). PR [#23](https://github.com/rszamszur/fastapi-mvc/pull/23) by [@r2r-dev](https://github.com/r2r-dev)

### Fixed

* Template style guide: W293 error. PR #20

### Internal

* Improve make target scripts both for package and template [#18](https://github.com/rszamszur/fastapi-mvc/issues/18). PR [#20](https://github.com/rszamszur/fastapi-mvc/pull/20)
* Do not run fastapi as a root user inside container [#16](https://github.com/rszamszur/fastapi-mvc/issues/16). PR [#23](https://github.com/rszamszur/fastapi-mvc/pull/23) by [@r2r-dev](https://github.com/r2r-dev)

## 0.5.0 (11.01.2022)

### Features

* Refactor project from the pure template into the package which generates fastapi-mvc projects from cookiecutter template [#6](https://github.com/rszamszur/fastapi-mvc/issues/6). PR [#10](https://github.com/rszamszur/fastapi-mvc/pull/10)

### Fixed

* Add missing `FASTAPI_USE_REDIS` env var in Helm chart config map and deployment.

### Internal

* Rename project to fastapi-mvc.
* Add `FASTAPI_DEBUG` env var in Helm chart config map and deployment.
* Add K8s integration test workflow.
* Rename Test workflow to CI.
* Extend make targets for package and template.
* Add minor improvements to package and template GitHub CI workflows.
* Add GitHub workflows for publishing to PyPi [#8](https://github.com/rszamszur/fastapi-mvc/issues/8). PR [#11](https://github.com/rszamszur/fastapi-mvc/pull/11)

## 0.4.0 (10.12.2021)

### Features

* Implement model for error response rendering.
* Implement custom HTTPException, and its handler to have freedom to define returned response body.
* Extend application configuration from environment variables.
* Add and utilize `gunicorn.conf.py` file for better WSGI configuration.

### Internal

* Update project dependencies:
  * fastapi (0.66.0 -> 0.70.0)
  * aioredis (2.0.0a1 -> 2.0.0)
  * aiohttp (3.7.4.post0 -> 3.8.1)
  * uvicorn (0.14.0 -> 0.15.0)
* Improve submodules import paths.
* Move `fastapi_mvc.app.config` submodule to `fastapi_mvc.config`.
* Refactor application and redis config with using `pydantic.BaseSetting`.
* Extend unit tests, and increase coverage to 99%.
* Change `RedisClient.ping()` method to return false instead of raising an RedisError exception.

## 0.3.0 (28.11.2021)

### Features

* Add python-poetry `pyproject.toml` and `poetry.lock` for dependency management and packaging.
* Reduce container image size by ~500 MB with using multi-stage build.

### Internal

* Remove setup.py and requirements.txt.
* Refactor make install to utilize poetry instead of pip.
* Update base container image digest sha.
* Improve GitHub Test workflow.

## 0.2.0 (09.11.2021)

### Features

* Implement make dev-env target for bootstrapping a local Kubernetes cluster with High Availability Redis cluster, and deploy application.
* Add Helm charts for fastapi-mvc.
* Add Vagrantfile.

### Internal

* Add manifests for [spotahome/redis-operator](https://github.com/spotahome/redis-operator).
* Fix minor documentation/comments typos.

## 0.1.0 (27.07.2021)

* Initial release
