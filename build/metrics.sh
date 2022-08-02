#!/usr/bin/env bash

if [ -n "$DEBUG" ]; then
	set -x
fi

set -o errexit
set -o nounset
set -o pipefail


POETRY_HOME="${POETRY_HOME:=${HOME}/.poetry}"
echo "[metrics] Run fastapi-mvc PEP 8 checks."
"$POETRY_HOME"/bin/poetry run flake8 --select=E,W,I --max-line-length 80 --import-order-style pep8 --exclude .git,__pycache__,.eggs,*.egg,.pytest_cache,fastapi_mvc/version.py,fastapi_mvc/__init__.py,fastapi_mvc/generators/**/template --statistics --count fastapi_mvc
echo "[metrics] Run fastapi-mvc PEP 257 checks."
"$POETRY_HOME"/bin/poetry run flake8 --select=D --ignore D301 --exclude ,fastapi_mvc/generators/**/template --statistics --count fastapi_mvc
echo "[metrics] Run fastapi-mvc code complexity checks."
"$POETRY_HOME"/bin/poetry run flake8 --select=C901 --exclude ,fastapi_mvc/generators/**/template --count fastapi_mvc
echo "[metrics] Run fastapi-mvc open TODO checks."
"$POETRY_HOME"/bin/poetry run flake8 --select=T --exclude ,fastapi_mvc/generators/**/template --statistics --count fastapi_mvc tests
echo "[metrics] Run fastapi-mvc black checks."
"$POETRY_HOME"/bin/poetry run black -l 80 --exclude "fastapi_mvc/generators/.*/template" --check fastapi_mvc
