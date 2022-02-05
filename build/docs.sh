#!/usr/bin/env bash

if [ -n "$DEBUG" ]; then
	set -x
fi

set -o errexit
set -o nounset
set -o pipefail

POETRY_HOME="${POETRY_HOME:=${HOME}/.poetry}"
MKDOCS_INSTALL_OPTS="${MKDOCS_INSTALL_OPTS:=""}"
echo "[docs] Build fastapi-mvc documentation."
"$POETRY_HOME"/bin/poetry run mkdocs build $MKDOCS_INSTALL_OPTS
