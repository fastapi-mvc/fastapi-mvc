#!/usr/bin/env bash

if [ -n "$DEBUG" ]; then
	set -x
fi

set -o errexit
set -o nounset
set -o pipefail

DIR=$(cd $(dirname "${BASH_SOURCE}") && pwd -P)

poetry run flake8 --select=E,W,I --max-line-length 80 --import-order-style pep8 --exclude .git,__pycache__,.eggs,*.egg,.pytest_cache,fastapi_mvc/version.py,fastapi_mvc/__init__.py,fastapi_mvc/template --tee --output-file=pep8_violations.txt --statistics --count fastapi_mvc
poetry run flake8 --select=D --ignore D301 --tee --exclude fastapi_mvc/template --output-file=pep257_violations.txt --statistics --count fastapi_mvc
poetry run flake8 --select=C901 --tee --exclude fastapi_mvc/template --output-file=code_complexity.txt --count fastapi_mvc
poetry run flake8 --select=T --tee  --exclude fastapi_mvc/template--output-file=todo_occurence.txt --statistics --count fastapi_mvc tests
poetry run black -l 80 --exclude fastapi_mvc/template --check fastapi_mvc