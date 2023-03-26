# Changelog

This file documents changes to [fastapi-mvc](https://github.com/fastapi-mvc/fastapi-mvc). The release numbering uses [semantic versioning](http://semver.org).

## Unreleased

### Generators

* Bump copier-controller from 0.2.1 to 0.2.2. [952bf68](https://github.com/fastapi-mvc/fastapi-mvc/commit/952bf68d6361de0c94ed81dc39ed1a5e7fcbb494)
* Bump copier-script from 0.1.1 to 0.1.2. [af51059](https://github.com/fastapi-mvc/fastapi-mvc/commit/af51059b4c1dd4e4a270c791aede1a66ac719eb7)

### Internal

* Refactor `flake.nix` using [flake-parts](https://github.com/hercules-ci/flake-parts). PR [#257](https://github.com/fastapi-mvc/fastapi-mvc/pull/257)
* Implement workflow for updating `flake.lock` inputs. PR [#257](https://github.com/fastapi-mvc/fastapi-mvc/pull/257)
* Update dependencies:
  * Bump myst-parser from 0.18.1 to 0.19.1. PR [#251](https://github.com/fastapi-mvc/fastapi-mvc/pull/251)
  * Bump pytest from 7.2.1 to 7.2.2. PR [#252](https://github.com/fastapi-mvc/fastapi-mvc/pull/252)
  * Bump sphinx from 5.3.0 to 6.1.3. PR [#254](https://github.com/fastapi-mvc/fastapi-mvc/pull/254)
  * Bump mypy from 1.0.1 to 1.1.1. PR [#255](https://github.com/fastapi-mvc/fastapi-mvc/pull/255)
  * Bump myst-parser from 0.19.1 to 1.0.0. PR [#256](https://github.com/fastapi-mvc/fastapi-mvc/pull/256)
* Update GitHub Actions:
  * Bump cachix/install-nix-action from 19 to 20. PR [#250](https://github.com/fastapi-mvc/fastapi-mvc/pull/250)

## 0.27.0 (01.03.2023)

### Breaking Changes

* Refactor API for generator command line interface implementation [#246](https://github.com/fastapi-mvc/fastapi-mvc/issues/246). PR [#245](https://github.com/fastapi-mvc/fastapi-mvc/pull/245)

### Generators

* Bump copier-project from 0.4.0 to 0.5.0. PR [#249](https://github.com/fastapi-mvc/fastapi-mvc/pull/249)

### Internal

* Implement type checking [#120](https://github.com/fastapi-mvc/fastapi-mvc/issues/120). PR [#245](https://github.com/fastapi-mvc/fastapi-mvc/pull/245)
* Update dependencies:
  * Bump markdown-it-py from 2.1.0 to 2.2.0. PR [#244](https://github.com/fastapi-mvc/fastapi-mvc/pull/244)

## 0.26.0 (12.02.2023)

### Generators

* Bump copier-generator from 0.1.0 to 0.2.0. PR [#241](https://github.com/fastapi-mvc/fastapi-mvc/pull/241)
* Bump copier-controller from 0.2.0 to 0.2.1. [16acea1](https://github.com/fastapi-mvc/fastapi-mvc/commit/16acea1b8281bd7e295c51c6052088dc4b1d1bf2)
* Bump copier-script from 0.1.0 to 0.1.1. [96a46d8](https://github.com/fastapi-mvc/fastapi-mvc/commit/96a46d85728ec1202dea23764e23c97b4a69bcd6)

## 0.25.0 (07.02.2023)

### Generators

* Bump copier-project from 0.3.0 to 0.4.0. PR [#240](https://github.com/fastapi-mvc/fastapi-mvc/pull/240)

### Internal

* Update Poetry to 1.3.x [#236](https://github.com/fastapi-mvc/fastapi-mvc/issues/236). PR [#237](https://github.com/fastapi-mvc/fastapi-mvc/pull/237)
* Update dependencies:
  * Bump flake8-docstrings from 1.6.0 to 1.7.0. PR [#235](https://github.com/fastapi-mvc/fastapi-mvc/pull/235)
  * Bump black from 22.12.0 to 23.1.0. PR [#239](https://github.com/fastapi-mvc/fastapi-mvc/pull/239)
* Update GitHub Actions:
  * Bump docker/build-push-action from 3 to 4. PR [#234](https://github.com/fastapi-mvc/fastapi-mvc/pull/234)
  * Bump cachix/install-nix-action from 18 to 19. PR [#238](https://github.com/fastapi-mvc/fastapi-mvc/pull/238)

## 0.24.0 (08.01.2023)

### Features

* Implement `fastapi-mvc update` command [#229](https://github.com/fastapi-mvc/fastapi-mvc/issues/229). PR [#230](https://github.com/fastapi-mvc/fastapi-mvc/pull/230)

### Internal

* Add `SECURITY.md`. [6f00a13](https://github.com/fastapi-mvc/fastapi-mvc/commit/6f00a139f6ed0d1e39e063f72562aa4bc65374c9)
* Refactor `.coveragerc` into `pyproject.toml`. PR [#232](https://github.com/fastapi-mvc/fastapi-mvc/pull/232)
* Remove override for a non-existent input in `flake.nix`. [49dc9c0](https://github.com/fastapi-mvc/fastapi-mvc/commit/49dc9c0e58d3c791f40c35e353d9cc57a534ddab)

### Docs

* Update `about.rst` page. PR [#230](https://github.com/fastapi-mvc/fastapi-mvc/pull/230)
* Update `quickstart.rst` page. PR [#230](https://github.com/fastapi-mvc/fastapi-mvc/pull/230)
* Add `cli.rst` page. PR [#231](https://github.com/fastapi-mvc/fastapi-mvc/pull/231)

## 0.23.0 (01.01.2023)

### Generators

* Bump copier-project from 0.2.0 to 0.3.0. [e99e66c](https://github.com/fastapi-mvc/fastapi-mvc/commit/e99e66c04ecef05b949071aeb2ad0dbfeb70f617)
* Bump copier-controller from 0.1.0 to 0.2.0. [0e710c1](https://github.com/fastapi-mvc/fastapi-mvc/commit/0e710c14bea8a41543f4b9c3f0e44ff45e690064)

### Internal

* Refactor and improve current test cases suite [#225](https://github.com/fastapi-mvc/fastapi-mvc/issues/225). PR [#227](https://github.com/fastapi-mvc/fastapi-mvc/pull/227)
* Update dependencies:
  * Bump pallets-sphinx-themes from 2.0.2 to 2.0.3. PR [#226](https://github.com/fastapi-mvc/fastapi-mvc/pull/226)

## 0.22.0 (15.12.2022)

### Generators

* Bump copier-project from 0.1.0 to 0.2.0. PR [#224](https://github.com/fastapi-mvc/fastapi-mvc/pull/224)

### Internal

* Update GitHub Actions:
  * Bump nwtgck/actions-netlify from 1.2.4 to 2.0.0. PR [#222](https://github.com/fastapi-mvc/fastapi-mvc/pull/222)
  * Bump fkirc/skip-duplicate-actions from 5.2.0 to 5.3.0. PR [#223](https://github.com/fastapi-mvc/fastapi-mvc/pull/223)

## 0.21.0 (13.12.2022)

### Features

* Refactor Nix expressions to flakes [#216](https://github.com/fastapi-mvc/fastapi-mvc/issues/216). PR [#218](https://github.com/fastapi-mvc/fastapi-mvc/pull/218)
* Add Python 3.11 support [#198](https://github.com/fastapi-mvc/fastapi-mvc/issues/198). PR [#220](https://github.com/fastapi-mvc/fastapi-mvc/pull/220)

### Internal

* Update dependencies:
  * Bump pytest from 7.1.3 to 7.2.0. PR [#203](https://github.com/fastapi-mvc/fastapi-mvc/pull/203)
  * Bump sphinx from 5.2.3 to 5.3.0. PR [#205](https://github.com/fastapi-mvc/fastapi-mvc/pull/205)
  * Bump flake8-import-order from 0.18.1 to 0.18.2. PR [#215](https://github.com/fastapi-mvc/fastapi-mvc/pull/215)
  * Bump black from 22.8.0 to 22.12.0. PR [#221](https://github.com/fastapi-mvc/fastapi-mvc/pull/221)
  * Bump certifi from 2022.9.24 to 2022.12.7. PR [#219](https://github.com/fastapi-mvc/fastapi-mvc/pull/219)

## 0.20.0 (11.11.2022)

### Features

* Allow generators lookup paths configuration via an environment variable [#211](https://github.com/fastapi-mvc/fastapi-mvc/issues/211). PR [#212](https://github.com/fastapi-mvc/fastapi-mvc/pull/212)

### Documentation

* Update documentation after refactor to copier [#175](https://github.com/fastapi-mvc/fastapi-mvc/issues/175). PR [#213](https://github.com/fastapi-mvc/fastapi-mvc/pull/213)

## 0.19.0 (09.11.2022)

### Features

* Implement new generator - shell script [#197](https://github.com/fastapi-mvc/fastapi-mvc/issues/197). PR [#208](https://github.com/fastapi-mvc/fastapi-mvc/pull/208)
* Implement CLI commands aliases [#80](https://github.com/fastapi-mvc/fastapi-mvc/issues/80). PR [#209](https://github.com/fastapi-mvc/fastapi-mvc/pull/209)

### Internal

* Update GitHub Actions:
  * Bump nwtgck/actions-netlify from 1.2.3 to 1.2.4. PR [#200](https://github.com/fastapi-mvc/fastapi-mvc/pull/200)
  * Bump cachix/cachix-action from 10 to 12. PR [#201](https://github.com/fastapi-mvc/fastapi-mvc/pull/201)
  * Bump cachix/install-nix-action from 17 to 18. PR [#202](https://github.com/fastapi-mvc/fastapi-mvc/pull/202)

## 0.18.2 (23.10.2022)

### Internal

* Ensure git is installed in `make install` target. PR [#190](https://github.com/fastapi-mvc/fastapi-mvc/pull/190)
* Start testing on macOS [#186](https://github.com/fastapi-mvc/fastapi-mvc/issues/186). PR [#191](https://github.com/fastapi-mvc/fastapi-mvc/pull/191)
* Refactor nix container image build to separate workflow [#193](https://github.com/fastapi-mvc/fastapi-mvc/issues/193). PR [#194](https://github.com/fastapi-mvc/fastapi-mvc/pull/194)
* Add container image build workflow [#192](https://github.com/fastapi-mvc/fastapi-mvc/issues/192). PR [#194](https://github.com/fastapi-mvc/fastapi-mvc/pull/194)
* Ensure system dependencies prior executing shell in `new` command [#184](https://github.com/fastapi-mvc/fastapi-mvc/issues/184). PR [#195](https://github.com/fastapi-mvc/fastapi-mvc/pull/195)

## 0.18.1 (17.10.2022)

### Generators

* Bump copier-project version from 0.1.0 to 0.1.1. [6afb1fd](https://github.com/fastapi-mvc/fastapi-mvc/commit/6afb1fd0d8d888c10887647dfe789060b2bcc5c4)

### Fixed

* Invalid default project name if destination is `.` [#187](https://github.com/fastapi-mvc/fastapi-mvc/issues/187). PR [#188](https://github.com/fastapi-mvc/fastapi-mvc/pull/188)

### Internal

* Implement ensure_permission method [#185](https://github.com/fastapi-mvc/fastapi-mvc/issues/185). PR [#188](https://github.com/fastapi-mvc/fastapi-mvc/pull/188)

## 0.18.0 (10.10.2022)

### Breaking Changes

* Improve generators UX [#171](https://github.com/fastapi-mvc/fastapi-mvc/issues/171). PR [#176](https://github.com/fastapi-mvc/fastapi-mvc/pull/176)
* Refactor generator generator cookiecutter template to copier [#172](https://github.com/fastapi-mvc/fastapi-mvc/issues/172). PR [#176](https://github.com/fastapi-mvc/fastapi-mvc/pull/176)
* Refactor controller generator cookiecutter template to copier [#173](https://github.com/fastapi-mvc/fastapi-mvc/issues/173). PR [#176](https://github.com/fastapi-mvc/fastapi-mvc/pull/176)
* Refactor project generator cookiecutter template to copier [#174](https://github.com/fastapi-mvc/fastapi-mvc/issues/174). PR [#176](https://github.com/fastapi-mvc/fastapi-mvc/pull/176)

## 0.17.0 (05.10.2022)

### Breaking Changes

* Drop Python 3.7 support. PR [#166](https://github.com/fastapi-mvc/fastapi-mvc/pull/166)

### Internal

* Bump project template version from 0.2.0 to 0.3.0 [8da80e2](https://github.com/fastapi-mvc/fastapi-mvc/commit/8da80e26faaa3519cb20f8be61a41ddbfa9fde7a).
* Drop mock dev-dependency [#128](https://github.com/fastapi-mvc/fastapi-mvc/issues/128). PR [#169](https://github.com/fastapi-mvc/fastapi-mvc/pull/169)
* Add poetry2nix overlay. PR [#168](https://github.com/fastapi-mvc/fastapi-mvc/pull/168)
* Update dependencies. PR [#167](https://github.com/fastapi-mvc/fastapi-mvc/pull/167)
  * Bump pytest from 6.2.5 to 7.1.3.
  * Bump pytest-cov from 2.12.0 to 4.0.0.
  * Bump flake8 from 3.9.2 to 5.0.4.
  * Bump black from 22.3.0 to 22.8.0.
  * Bump Sphinx from 4.5.0 to 5.2.3.
  * Bump myst-parser from 0.17.2 to 0.18.1.

## 0.16.1 (04.10.2022)

### Internal

* Pin default `fastapi-mvc/cookiecutter` version to a tag rather than `master` branch [#159](https://github.com/fastapi-mvc/fastapi-mvc/issues/159).
* Override canceling matrix job if only one of them fail [#64](https://github.com/fastapi-mvc/fastapi-mvc/issues/64). PR [#160](https://github.com/fastapi-mvc/fastapi-mvc/pull/160)
* Update documentation [#158](https://github.com/fastapi-mvc/fastapi-mvc/issues/158). PR [#165](https://github.com/fastapi-mvc/fastapi-mvc/pull/165)

## 0.16.0 (18.09.2022)

### NOTE!

During this release, not only was the project transferred under fastapi-mvc organization. But also project template (`fastapi_mvc/generators/project/template/**`) was moved to a separate repository. 
This means a lot of refactoring, cleanup, and changes in configuration, CI, URLs, etc. Even though CI checks are pretty thorough, there is a chance I could miss something that will cause a bug somewhere. 
If so, feel free to raise an issue, and I'll handle it as soon as possible.

### Features

* Add Nix CI workflow [#141](https://github.com/fastapi-mvc/fastapi-mvc/issues/141). PR [#145](https://github.com/fastapi-mvc/fastapi-mvc/pull/145)
* Move project template to a separate repository [#146](https://github.com/fastapi-mvc/fastapi-mvc/issues/146). PR [#157](https://github.com/fastapi-mvc/fastapi-mvc/pull/149)

### Internal

* Migrate to Poetry 1.2.x release [#21](https://github.com/fastapi-mvc/fastapi-mvc/issues/21). PR [#142](https://github.com/fastapi-mvc/fastapi-mvc/pull/142)
* Improve GH actions automation [#143](https://github.com/fastapi-mvc/fastapi-mvc/issues/143). PR [#142](https://github.com/fastapi-mvc/fastapi-mvc/pull/142)
* Improve generated project cache in CI workflow [#107](https://github.com/fastapi-mvc/fastapi-mvc/issues/107). PR [#142](https://github.com/fastapi-mvc/fastapi-mvc/pull/142)
* Refactor Makefile to utilize different set of targets for Nix and Poetry [#144](https://github.com/fastapi-mvc/fastapi-mvc/issues/144). PR [#145](https://github.com/fastapi-mvc/fastapi-mvc/pull/145)
* Transfer project to fastapi-mvc organisation [#147](https://github.com/fastapi-mvc/fastapi-mvc/issues/147). PR [#148](https://github.com/fastapi-mvc/fastapi-mvc/pull/148)

## 0.15.0 (09.09.2022)

### Breaking Changes

* Improve custom generator class discovery in `load_generators` method [#137](https://github.com/fastapi-mvc/fastapi-mvc/issues/137). PR [#138](https://github.com/fastapi-mvc/fastapi-mvc/pull/138)
  - This changes the module attribute from which the custom generator class is being discovered. For older custom generators, just replace `__all__ = ...` with `generator_class = ...` in custom generator `__init__.py`.

### Fixed

* Method `get_git_user_info()` raises `FileNotFoundError` exception if `git` command does not exists [#85](https://github.com/fastapi-mvc/fastapi-mvc/issues/85). PR [#140](https://github.com/fastapi-mvc/fastapi-mvc/pull/140)

### Internal

* Add `flake8` pyflakes checks to `make metrics` target [#135](https://github.com/fastapi-mvc/fastapi-mvc/issues/135). PR [#136](https://github.com/fastapi-mvc/fastapi-mvc/pull/136)
* Update project template dependencies:
  * Bump fastapi from 0.75.0 to 0.82.0.
  * Bump uvicorn from 0.17.0 to 0.18.3.
  * Bump aioredis from 2.0.0 to 2.0.1.
  * Bump aiohttp from 3.8.0 to 3.8.1.

## 0.14.1 (11.08.2022)

### Features

* Allow `pkgs.python` to be configurable in `shell.nix`. PR [#132](https://github.com/fastapi-mvc/fastapi-mvc/pull/132)

### Fixed

* Fix `POETRY_HOME` environment variable in shell.nix nix expression [#131](https://github.com/fastapi-mvc/fastapi-mvc/issues/131). PR [#132](https://github.com/fastapi-mvc/fastapi-mvc/pull/132)

### Internal

* Refactor string formatting with f-Strings [#133](https://github.com/fastapi-mvc/fastapi-mvc/issues/133). PR [#134](https://github.com/fastapi-mvc/fastapi-mvc/pull/134)
* Update macos runner in integration workflows [#125](https://github.com/fastapi-mvc/fastapi-mvc/issues/125). PR [#126](https://github.com/fastapi-mvc/fastapi-mvc/pull/126)
* Add minor improvements. PR [#127](https://github.com/fastapi-mvc/fastapi-mvc/pull/127)

## 0.14.0 (31.07.2022)

### Features

* Add `-N, --skip-nix` flag for `fastapi-mvc new` command [#123](https://github.com/fastapi-mvc/fastapi-mvc/issues/123). PR [#124](https://github.com/fastapi-mvc/fastapi-mvc/pull/124)
* Add nix expression for `fastapi-mvc` package [#114](https://github.com/fastapi-mvc/fastapi-mvc/issues/114). PR [#116](https://github.com/fastapi-mvc/fastapi-mvc/pull/116)
* Add nix expression for package generated from `fastapi-mvc` project template. [#115](https://github.com/fastapi-mvc/fastapi-mvc/issues/115). PR [#116](https://github.com/fastapi-mvc/fastapi-mvc/pull/116)
* Add container image nix expression for `fastapi-mvc` and project template [#56](https://github.com/fastapi-mvc/fastapi-mvc/issues/56). PR [#116](https://github.com/fastapi-mvc/fastapi-mvc/pull/116)

### Internal

* Improve Vagrantfile in project template [#121](https://github.com/fastapi-mvc/fastapi-mvc/issues/121). PR [#122](https://github.com/fastapi-mvc/fastapi-mvc/pull/122)

## 0.13.1 (13.06.2022)

### Security

* [CVE-2022-24065](http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-24065) OS Command Injection in cookiecutter. Update vulnerable dependency:
  * Bump cookiecutter from 1.7.3 to 2.1.1.

## 0.13.0 (09.06.2022)

### Features

* Add support for binding gunicorn server to a UNIX socket [#25](https://github.com/fastapi-mvc/fastapi-mvc/issues/25). PR [#105](https://github.com/fastapi-mvc/fastapi-mvc/pull/105)

### Fixed

* Missing cookiecutter kwarg in generator template [#102](https://github.com/fastapi-mvc/fastapi-mvc/issues/102). PR [#103](https://github.com/fastapi-mvc/fastapi-mvc/pull/103)

### Internal

* Add generators feature documentation [#75](https://github.com/fastapi-mvc/fastapi-mvc/issues/75). PR [#101](https://github.com/fastapi-mvc/fastapi-mvc/pull/101)
* Add integration tests for generators [#76](https://github.com/fastapi-mvc/fastapi-mvc/issues/76). PR [#104](https://github.com/fastapi-mvc/fastapi-mvc/pull/104)

## 0.12.0 (10.05.2022)

### Features

* Add Sphinx autodoc documentation for project template [#89](https://github.com/fastapi-mvc/fastapi-mvc/issues/89). PR [#99](https://github.com/fastapi-mvc/fastapi-mvc/pull/99)

### Internal

* Extend and improve k8s integration workflow [#93](https://github.com/fastapi-mvc/fastapi-mvc/issues/93). PR [#94](https://github.com/fastapi-mvc/fastapi-mvc/pull/94)
* Improve generators implementation [#96](https://github.com/fastapi-mvc/fastapi-mvc/issues/96). PR [#97](https://github.com/fastapi-mvc/fastapi-mvc/pull/97)
* Refactor fastapi-mvc project template into generators submodule [#77](https://github.com/fastapi-mvc/fastapi-mvc/issues/77). PR [#98](https://github.com/fastapi-mvc/fastapi-mvc/pull/98)
* Refactor and improve project template structure [#90](https://github.com/fastapi-mvc/fastapi-mvc/issues/90). PR [#99](https://github.com/fastapi-mvc/fastapi-mvc/pull/99)
* Increase project template unit tests coverage to 100%. PR [#99](https://github.com/fastapi-mvc/fastapi-mvc/pull/99)
* Update package dependencies:
  * Bump click from 7.1.2 to 8.1.3.
  * Bump black from 21.12b0 to 22.3.0.
* Update project template dependencies:
  * Bump click from 7.1.2 to 8.1.3.
  * Bump black from 21.12b0 to 22.3.0.

## 0.11.1 (27.04.2022)

### Fixed

* Controller generator creating duplicates entries in config/router.py [#78](https://github.com/fastapi-mvc/fastapi-mvc/issues/78). PR [#92](https://github.com/fastapi-mvc/fastapi-mvc/pull/92)

### Internal

* Remove redundant `# -*- coding: utf-8 -*-` in file headers [#66](https://github.com/fastapi-mvc/fastapi-mvc/issues/66). PR [#91](https://github.com/fastapi-mvc/fastapi-mvc/pull/91)

## 0.11.0 (24.04.2022)

### Features

* Implement controller generator [#47](https://github.com/fastapi-mvc/fastapi-mvc/issues/47). PR [#70](https://github.com/fastapi-mvc/fastapi-mvc/pull/70)
* Implement generator generator [#68](https://github.com/fastapi-mvc/fastapi-mvc/issues/68). PR [#70](https://github.com/fastapi-mvc/fastapi-mvc/pull/70)
* Implement logic for loading user generators into fastapi-mvc CLI at RunTime [#69](https://github.com/fastapi-mvc/fastapi-mvc/issues/69). PR [#70](https://github.com/fastapi-mvc/fastapi-mvc/pull/70)

### Internal

* Implement global except hook, refactor current exceptions handling [#73](https://github.com/fastapi-mvc/fastapi-mvc/issues/73). PR [#70](https://github.com/fastapi-mvc/fastapi-mvc/pull/70)
* Refactor `Invoker` class with using queue [#71](https://github.com/fastapi-mvc/fastapi-mvc/issues/71). PR [#70](https://github.com/fastapi-mvc/fastapi-mvc/pull/70)
* Refactor `fastapi_mvc.commands` to be more generic [#72](https://github.com/fastapi-mvc/fastapi-mvc/issues/72). PR [#70](https://github.com/fastapi-mvc/fastapi-mvc/pull/70)
* Refactor existing documentation with Sphinx [#74](https://github.com/fastapi-mvc/fastapi-mvc/issues/74). PR [#83](https://github.com/fastapi-mvc/fastapi-mvc/pull/83)
* Migrate to `install-poetry.py` script prior Poetry 1.2.x release migration [#87](https://github.com/fastapi-mvc/fastapi-mvc/issues/87). PR [#88](https://github.com/fastapi-mvc/fastapi-mvc/pull/88)

### Fixed

* CLI `fastapi-mvc run` command doesn't distinguish whether project is installed or crashed due to error [#82](https://github.com/fastapi-mvc/fastapi-mvc/issues/82). PR [#86](https://github.com/fastapi-mvc/fastapi-mvc/pull/86)
* CLI `fastapi-mvc run` command should use absolute path to poetry binary [#84](https://github.com/fastapi-mvc/fastapi-mvc/issues/84). PR [#86](https://github.com/fastapi-mvc/fastapi-mvc/pull/86)

## 0.10.0 (07.04.2022)

### Fixed

* New project cannot install with Python version > 3.10 [#60](https://github.com/fastapi-mvc/fastapi-mvc/issues/60). PR [#61](https://github.com/fastapi-mvc/fastapi-mvc/pull/61) by [@Merinorus](https://github.com/Merinorus)
* Metrics job for Python 3.10 [#63](https://github.com/fastapi-mvc/fastapi-mvc/issues/63). PR [#65](https://github.com/fastapi-mvc/fastapi-mvc/pull/65) by [@Merinorus](https://github.com/Merinorus)

### Features

* Add nix shell config for local development environment [#57](https://github.com/fastapi-mvc/fastapi-mvc/issues/57). PR [#58](https://github.com/fastapi-mvc/fastapi-mvc/pull/58)
* Allow overriding poetry version for make install target via env variable: $POETRY_VERSION [#59](https://github.com/fastapi-mvc/fastapi-mvc/issues/59). PR [#58](https://github.com/fastapi-mvc/fastapi-mvc/pull/58)

### Internal

* Update template dependencies:
  * Bump fastapi from 0.70.0 to 0.75.0.
  * Bump uvicorn from 0.15.0 to 0.17.0.
* Add minor `ShellUtils` unit test case improvement.
* Add python 3.10 in CI tests [#62](https://github.com/fastapi-mvc/fastapi-mvc/issues/62). PR [#61](https://github.com/fastapi-mvc/fastapi-mvc/pull/61) by [@Merinorus](https://github.com/Merinorus)

## 0.9.0 (14.02.2022)

### Fixed

* CLI`fastapi-mvc run` command implementation [#48](https://github.com/fastapi-mvc/fastapi-mvc/issues/48). PR [#52](https://github.com/fastapi-mvc/fastapi-mvc/pull/52)
* GitHub main workflow package coverage sources. PR [#52](https://github.com/fastapi-mvc/fastapi-mvc/pull/52)

### Internal

* Implement all `fastapi-mvc.ini` parser properties [#50](https://github.com/fastapi-mvc/fastapi-mvc/issues/50). PR [#52](https://github.com/fastapi-mvc/fastapi-mvc/pull/52)
* Refactor execution logic from CLI into command design pattern [#51](https://github.com/fastapi-mvc/fastapi-mvc/issues/51). PR [#52](https://github.com/fastapi-mvc/fastapi-mvc/pull/52)

## 0.8.0 (08.02.2022)

### Features

* Implement CLI `fastapi-mvc run` command for running uvicorn development server [#14](https://github.com/fastapi-mvc/fastapi-mvc/issues/14), [#31](https://github.com/fastapi-mvc/fastapi-mvc/issues/31). PR [#35](https://github.com/fastapi-mvc/fastapi-mvc/pull/35)

### Fixed

* New project doesn't install correctly if created from activated virtualenv [#37](https://github.com/fastapi-mvc/fastapi-mvc/issues/37). PR [#40](https://github.com/fastapi-mvc/fastapi-mvc/pull/40)
* CLI `fastapi-mvc new` `--license` option value is not passed to cookiecutter [#39](https://github.com/fastapi-mvc/fastapi-mvc/issues/39). PR [#42](https://github.com/fastapi-mvc/fastapi-mvc/pull/42)

### Internal

* Refactor logic from CLI commands to separate classes [#38](https://github.com/fastapi-mvc/fastapi-mvc/issues/38). PR [#40](https://github.com/fastapi-mvc/fastapi-mvc/pull/40)
* Add documentation [#9](https://github.com/fastapi-mvc/fastapi-mvc/issues/9). PR [#33](https://github.com/fastapi-mvc/fastapi-mvc/pull/33)
* Add make template-checks target for running metrics and tests on template.
* Add make pre-commit target for running package and template checks.
* Add make test target for running package unit and integration tests.
* Improve make scripts logging information.

## 0.7.0 (31.01.2022)

### Features

* Implement new template CLI serve command options [#24](https://github.com/fastapi-mvc/fastapi-mvc/issues/24). PR [#27](https://github.com/fastapi-mvc/fastapi-mvc/pull/27)

### Fixed

* Incomplete command in template `build/unit-test.sh` make script [#28](https://github.com/fastapi-mvc/fastapi-mvc/issues/28). PR [#27](https://github.com/fastapi-mvc/fastapi-mvc/pull/27)
* Debian snapshot repository is expired causing container image build failure [#29](https://github.com/fastapi-mvc/fastapi-mvc/issues/29). PR [#27](https://github.com/fastapi-mvc/fastapi-mvc/pull/27)

### Internal

* Lint tests. PR #30

## 0.6.0 (27.01.2022)

### Features

* Implement all major HTTP methods in aiohttp utility [#17](https://github.com/fastapi-mvc/fastapi-mvc/issues/17). PR [#22](https://github.com/fastapi-mvc/fastapi-mvc/pull/22)
* Make container image reproducible both for package and template [#15](https://github.com/fastapi-mvc/fastapi-mvc/issues/15). PR [#23](https://github.com/fastapi-mvc/fastapi-mvc/pull/23) by [@r2r-dev](https://github.com/r2r-dev)

### Fixed

* Template style guide: W293 error. PR #20

### Internal

* Improve make target scripts both for package and template [#18](https://github.com/fastapi-mvc/fastapi-mvc/issues/18). PR [#20](https://github.com/fastapi-mvc/fastapi-mvc/pull/20)
* Do not run fastapi as a root user inside container [#16](https://github.com/fastapi-mvc/fastapi-mvc/issues/16). PR [#23](https://github.com/fastapi-mvc/fastapi-mvc/pull/23) by [@r2r-dev](https://github.com/r2r-dev)

## 0.5.0 (11.01.2022)

### Features

* Refactor project from the pure template into the package which generates fastapi-mvc projects from cookiecutter template [#6](https://github.com/fastapi-mvc/fastapi-mvc/issues/6). PR [#10](https://github.com/fastapi-mvc/fastapi-mvc/pull/10)

### Fixed

* Add missing `FASTAPI_USE_REDIS` env var in Helm chart config map and deployment.

### Internal

* Rename project to fastapi-mvc.
* Add `FASTAPI_DEBUG` env var in Helm chart config map and deployment.
* Add K8s integration test workflow.
* Rename Test workflow to CI.
* Extend make targets for package and template.
* Add minor improvements to package and template GitHub CI workflows.
* Add GitHub workflows for publishing to PyPi [#8](https://github.com/fastapi-mvc/fastapi-mvc/issues/8). PR [#11](https://github.com/fastapi-mvc/fastapi-mvc/pull/11)

## 0.4.0 (10.12.2021)

### Features

* Implement model for error response rendering.
* Implement custom HTTPException, and its handler to have freedom to define returned response body.
* Extend application configuration from environment variables.
* Add and utilize `gunicorn.conf.py` file for better WSGI configuration.

### Internal

* Update project dependencies:
  * Bump fastapi from 0.66.0 to 0.70.0.
  * Bump aioredis from 2.0.0a1 to 2.0.0.
  * Bump aiohttp from 3.7.4.post0 to 3.8.1.
  * Bump uvicorn from 0.14.0 to 0.15.0.
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
