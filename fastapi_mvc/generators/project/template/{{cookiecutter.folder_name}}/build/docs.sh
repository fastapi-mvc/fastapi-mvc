#!/usr/bin/env bash

if [ -n "$DEBUG" ]; then
	set -x
fi

set -o errexit
set -o nounset
set -o pipefail

POETRY_HOME="${POETRY_HOME:=${HOME}/.poetry}"
SPHINX_BUILD_OPTS="${SPHINX_BUILD_OPTS:=""}"
echo "[docs] Build {{cookiecutter.project_name}} documentation."
"$POETRY_HOME"/bin/poetry run sphinx-build docs site $SPHINX_BUILD_OPTS
