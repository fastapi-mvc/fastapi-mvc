# Contributing

**First off, thanks for taking the time to contribute!**

## Issues

**Before submitting**

* **Check that your issue does not already exist in the [issue tracker](https://github.com/fastapi-mvc/fastapi-mvc/issues)**

### Questions

If you have any question about fastapi-mvc, or you are seeking for help you are encouraged to [open question](https://github.com/fastapi-mvc/fastapi-mvc/issues/new?assignees=&labels=question&template=question.md&title=) or [a new discussion](https://github.com/fastapi-mvc/fastapi-mvc/discussions/new).

### Suggesting enhancements

Feel free to [open enhancement](https://github.com/fastapi-mvc/fastapi-mvc/issues/new?assignees=&labels=enhancement%2C+triage&template=feature-request.md&title=) so we can discuss it. Bringing new ideas and pointing out elements needing clarification allows to make this project better!

### Reporting Bugs

If you encountered an unexpected behavior using [fastapi-mvc](https://github.com/fastapi-mvc/fastapi-mvc), please open bug report and provide the necessary information by [filling in the template](https://github.com/fastapi-mvc/fastapi-mvc/issues/new?assignees=&labels=bug%2C+triage&template=bug-report.md&title=).

## Documentation

The project could always use more documentation, whether as part of the official project docs, or even on the web in blog posts, articles, and such.

## Discuss

Feel free to discuss with community through [discussion channel](https://github.com/fastapi-mvc/fastapi-mvc/discussions).

## Contributing to code

### Codebase

This project is made of two things:

* Package: fastapi-mvc - implementation, tests, etc.
* Builtin copier templates: 
  * [fastapi-mvc/copier-project](https://github.com/fastapi-mvc/copier-project) for scaffolding new fastapi-mvc project.
  * [fastapi-mvc/copier-controller](https://github.com/fastapi-mvc/copier-controller) for scaffolding new controller upon fastapi-mvc project.
  * [fastapi-mvc/copier-generator](https://github.com/fastapi-mvc/copier-generator) for scaffolding new generator for fastapi-mvc.
  * [fastapi-mvc/copier-script](https://github.com/fastapi-mvc/copier-script) for scaffolding new shell script.

The project template (copier-project) has their own tests and checks. However, since template isn't a valid Python code until its generated, all checks are done on the default (full) generated project in [fastapi-mvc/copier-project CI workflow](https://github.com/fastapi-mvc/copier-project/actions/workflows/main.yml).

### Style guide

Git Commit Messages:

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Reference issues and pull requests liberally after the first line

Metrics stage ensure following rules are followed:

* [PEP 8](https://www.python.org/dev/peps/pep-0008/)
* [PEP 257](https://www.python.org/dev/peps/pep-0257/) for docstrings
* [black](https://github.com/psf/black) for unified formatting

### Development environment

This project provides two ways of setting up the project for local development. Feel free to choose one that suits you the most.

<table>
<tr>
<th> Poetry </th>
<th> Nix (recommended) </th>
</tr>
<tr>
<td>

Prerequisites:

* Python 3.8 or later [How to install python](https://docs.python-guide.org/starting/installation/)
* make
* git 2.27 or later
* (optional) curl
* (optional) Poetry [How to install poetry](https://python-poetry.org/docs/#installation)

</td>
<td>

Prerequisites:

* Nix 2.8.x or later installed [How to install Nix](https://nixos.org/download.html)

</td>
</tr>
<tr>
<td colspan="2">

You will first need to fork [fastapi-mvc](https://github.com/fastapi-mvc/fastapi-mvc) and clone repository:

```shell
git clone git@github.com:your_username/fastapi-mvc.git
cd fastapi-mvc
```

</td>
</tr>
<tr>
<td>

Now, you will need to install the required dependencies for fastapi-mvc with `Poetry` via `make install` target:

```shell
make install
```

By default `make install` target will search first for `python3` then `python` executable in your `PATH`.
If needed this can be overridden by `PYTHON` environment variable.

```shell
export PYTHON=/path/to/my/python
make install
```

If `Poetry` is not found in its default installation directory (`${HOME}/.local/share/pypoetry`) this target will install it for you.
However, one can always point to existing/customize `Poetry` installation with [environment variables](https://python-poetry.org/docs/configuration/#using-environment-variables):

```shell
export POETRY_HOME=/custom/poetry/path
export POETRY_CACHE_DIR=/custom/poetry/path/cache
export POETRY_VIRTUALENVS_IN_PROJECT=true
make install
```

</td>
<td>

First [enable Nix flakes](https://nixos.wiki/wiki/Flakes#Enable_flakes) if needed.

(Optional) [Setup fastapi-mvc Nix binary cache](https://app.cachix.org/cache/fastapi-mvc#pull) to speed up the build process:

```shell
nix-env -iA cachix -f https://cachix.org/api/v1/install
cachix use fastapi-mvc
```

Build fastapi-mvc development environment with Nix:

```shell
nix build .#poetryEnv --print-build-logs
```

**NOTE!** On first run this may take a while.

To spawn shell with complete development environment form Nix: 

```shell
nix develop
```

</td>
</tr>
<tr>
<td colspan="2">

Create a branch for local development:

```shell
git checkout -b name-of-your-bugfix-or-feature
```

Now you can make your changes locally. When you're done making changes, check that your changes pass all tests:

</td>
</tr>
<tr>
<td>

```shell
make metrics
make test
```

</td>
<td>

```shell
nix run .#metrics
nix run .#test
```

</td>
</tr>
<tr>
<td colspan="2">

Commit your changes and push your branch to GitHub:

```shell
git add .
git commit -m "Meaningfull commit message"
git push origin name-of-your-bugfix-or-feature
```

</td>
</tr>
</table>

### Pull requests

Before you submit a pull request, check that it meets these guidelines:

* Updated the `CHANGELOG.md` file with your changes.
* Added tests for changed code where applicable.
* Documentation reflects the changes where applicable.
* [Open a new pull request](https://github.com/fastapi-mvc/fastapi-mvc/compare)

If you have any questions to any of the points above, just **submit and ask**!
This checklist is here to help you, not to deter you from contributing!
