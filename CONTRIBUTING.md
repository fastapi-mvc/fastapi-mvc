### :+1::tada: First off, thanks for taking the time to contribute! :tada::+1:

## Issues

**Before submitting**

* **Check that your issue does not already exist in the [issue tracker](https://github.com/rszamszur/fastapi-mvc/issues)**

### Questions

If you have any question about fastapi-mvc, or you are seeking for help you are encouraged to [open question](https://github.com/rszamszur/fastapi-mvc/issues/new?assignees=&labels=question&template=question.md&title=) or [a new discussion](https://github.com/rszamszur/fastapi-mvc/discussions/new).

### Suggesting enhancements

Feel free to [open enhancement](https://github.com/rszamszur/fastapi-mvc/issues/new?assignees=&labels=enhancement%2C+triage&template=feature-request.md&title=) so we can discuss it. Bringing new ideas and pointing out elements needing clarification allows to make this project better!

### Reporting Bugs

If you encountered an unexpected behavior using [fastapi-mvc](https://github.com/rszamszur/fastapi-mvc), please open bug report and provide the necessary information by [filling in the template](https://github.com/rszamszur/fastapi-mvc/issues/new?assignees=&labels=bug%2C+triage&template=bug-report.md&title=).

## Contributing to code

### Codebase

This project is made of two things:

* Template: [cookiecutter template (`fastapi_mvc/template/*`)](https://github.com/rszamszur/fastapi-mvc/tree/master/fastapi_mvc/template) from which projects are generated.
* Package: fastapi-mvc - implementation, tests, etc. Everything except `fastapi_mvc/template` directory.

Both package and template have their own tests and checks. However, since template isn't a valid Python code until its generated, all checks are done on the default (full) generated project.

### Style guide

#### Git Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Reference issues and pull requests liberally after the first line

#### Package - fastapi-mvc

Metrics stage ensure following rules are followed:

* [PEP 8](https://www.python.org/dev/peps/pep-0008/)
* [PEP 257](https://www.python.org/dev/peps/pep-0257/) for docstrings
* [black](https://github.com/psf/black) for unified formatting

#### Template - `fastapi_mvc/template/*`

Template metrics stage ensure following rules are followed:

* [PEP 8](https://www.python.org/dev/peps/pep-0008/)
* [PEP 257](https://www.python.org/dev/peps/pep-0257/) for docstrings
* [black](https://github.com/psf/black) for unified formatting

### Local development

You will first need to fork [fastapi-mvc](https://github.com/rszamszur/fastapi-mvc) and clone repository:
```shell
git clone git@github.com:your_username/fastapi-mvc.git
cd fastapi-mvc
```
Now, you will need to install the required dependencies for fastapi-mvc:
```shell
make install
```
Make sure that the current tests are passing on your machine:
```shell
make test
```
To maintain high code quality and readability this project has strict [style guide](#style-guide) rules enforced by PEP and black.
You must ensure that your code follows it. If not, the CI will fail and your Pull Request will not be merged.

To make sure that you don't accidentally commit code that does pass CI, you can run all checks:
```shell
make pre-commit
```
or separately for package:
```shell
make metrics
make unit-test
make integration-test
```
and for template:
```shell
make template-checks
```

Your code must be accompanied by corresponding tests, if tests are not present your code will not be merged.

### Pull requests

*Note: Since K8s integration workflow can take up to 30 minutes, it only needs to be checked before merging. Feel free to use `[skip-k8s]` flag at the beginning of the commit message to skip it for work in progress.*

* [Open a new pull request](https://github.com/rszamszur/fastapi-mvc/compare)
* Update the `CHANGELOG.md` file with your changes.
* Update documentation if required.
