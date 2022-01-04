#!/usr/bin/env bash

if [ -n "$DEBUG" ]; then
	set -x
fi

set -o errexit
set -o nounset
set -o pipefail

DIR=$(cd $(dirname "${BASH_SOURCE}") && pwd -P)

if command -v python3 &> /dev/null; then
  PYTHON=python3
elif command -v python &> /dev/null; then
  PYTHON=python
else
  echo "[install] Python is not installed."
  exit 1
fi

PYTHON_VERSION=$($PYTHON -V 2>&1 | grep -Eo '([0-9]+\.[0-9]+\.[0-9]+)$')
if [[ ${PYTHON_VERSION} < "3.7.0" ]]; then
  echo "[install] Python version 3.7.0 or higher is required."
  exit 1
fi

POETRY_HOME="${POETRY_HOME:=${HOME}/.local}"
if ! command -v "$POETRY_HOME"/bin/poetry &> /dev/null; then
  echo "[install] Poetry is not installed. Begin download and install."
  curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | POETRY_HOME=$POETRY_HOME $PYTHON -
fi

echo "[install] Begin installing project."
"$POETRY_HOME"/bin/poetry install --no-interaction

cat <<EOF
Project successfully installed.
To activate virtualenv run: $ poetry shell
Now you should access CLI script: $ fastapi-mvc --help
Alternatively you can access CLI script via poetry run: $ poetry run fastapi-mvc --help
To deactivate virtualenv simply type: $ deactivate
EOF