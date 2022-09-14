#!/usr/bin/env bash

if [ -n "$DEBUG" ]; then
	set -x
fi

set -o errexit
set -o nounset
set -o pipefail

POETRY_HOME="${POETRY_HOME:=${HOME}/.local/share/pypoetry}"
POETRY_BINARY="${POETRY_BINARY:=${POETRY_HOME}/venv/bin/poetry}"
echo "[metrics] Run {{cookiecutter.project_name}} PEP 8 checks."
"$POETRY_BINARY" run flake8 --select=E,W,I --max-line-length 80 --import-order-style pep8 --statistics --count {{cookiecutter.package_name}}
echo "[metrics] Run {{cookiecutter.project_name}} PEP 257 checks."
"$POETRY_BINARY" run flake8 --select=D --ignore D301 --statistics --count {{cookiecutter.package_name}}
echo "[metrics] Run {{cookiecutter.project_name}} pyflakes checks."
"$POETRY_BINARY" run flake8 --select=F --statistics --count {{cookiecutter.package_name}}
echo "[metrics] Run {{cookiecutter.project_name}} code complexity checks."
"$POETRY_BINARY" run flake8 --select=C901 --statistics --count {{cookiecutter.package_name}}
echo "[metrics] Run {{cookiecutter.project_name}} open TODO checks."
"$POETRY_BINARY" run flake8 --select=T --statistics --count {{cookiecutter.package_name}} tests
echo "[metrics] Run {{cookiecutter.project_name}} black checks."
"$POETRY_BINARY" run black -l 80 --check {{cookiecutter.package_name}}
