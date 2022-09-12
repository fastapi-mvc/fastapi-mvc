#!/usr/bin/env bash

if [ -n "$DEBUG" ]; then
	set -x
fi

set -o errexit
set -o nounset
set -o pipefail


POETRY_HOME="${POETRY_HOME:=${HOME}/.local/share/pypoetry}"
POETRY_BINARY="${POETRY_BINARY:=${POETRY_HOME}/venv/bin/poetry}"
echo "[metrics] Run fastapi-mvc PEP 8 checks."
"$POETRY_BINARY" run flake8 --select=E,W,I --max-line-length 80 --import-order-style pep8 --extend-exclude=fastapi_mvc/generators/**/template --statistics --count fastapi_mvc
echo "[metrics] Run fastapi-mvc PEP 257 checks."
"$POETRY_BINARY" run flake8 --select=D --ignore D301 --extend-exclude=fastapi_mvc/generators/**/template --statistics --count fastapi_mvc
echo "[metrics] Run fastapi-mvc pyflakes checks."
"$POETRY_BINARY" run flake8 --select=F --extend-exclude=fastapi_mvc/generators/**/template --statistics --count fastapi_mvc
echo "[metrics] Run fastapi-mvc code complexity checks."
"$POETRY_BINARY" run flake8 --select=C901 --extend-exclude=fastapi_mvc/generators/**/template --statistics --count fastapi_mvc
echo "[metrics] Run fastapi-mvc open TODO checks."
"$POETRY_BINARY" run flake8 --select=T --extend-exclude=fastapi_mvc/generators/**/template --statistics --count fastapi_mvc tests
echo "[metrics] Run fastapi-mvc black checks."
"$POETRY_BINARY" run black -l 80 --exclude "fastapi_mvc/generators/.*/template" --check fastapi_mvc
