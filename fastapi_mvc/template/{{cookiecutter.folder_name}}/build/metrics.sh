#!/usr/bin/env bash

if [ -n "$DEBUG" ]; then
	set -x
fi

set -o errexit
set -o nounset
set -o pipefail

POETRY_HOME="${POETRY_HOME:=${HOME}/.poetry}"
"$POETRY_HOME"/bin/poetry run flake8 --select=E,W,I --max-line-length 80 --import-order-style pep8 --exclude .git,__pycache__,.eggs,*.egg,.pytest_cache,{{cookiecutter.package_name}}/version.py,{{cookiecutter.package_name}}/__init__.py --tee --output-file=pep8_violations.txt --statistics --count {{cookiecutter.package_name}}
"$POETRY_HOME"/bin/poetry run flake8 --select=D --ignore D301 --tee --output-file=pep257_violations.txt --statistics --count {{cookiecutter.package_name}}
"$POETRY_HOME"/bin/poetry run flake8 --select=C901 --tee --output-file=code_complexity.txt --count {{cookiecutter.package_name}}
"$POETRY_HOME"/bin/poetry run flake8 --select=T --tee --output-file=todo_occurence.txt --statistics --count {{cookiecutter.package_name}} tests
"$POETRY_HOME"/bin/poetry run black -l 80 --check {{cookiecutter.package_name}}
