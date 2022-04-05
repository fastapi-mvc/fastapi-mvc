#!/usr/bin/env bash

if [ -n "$DEBUG" ]; then
	set -x
fi

set -o errexit
set -o nounset
set -o pipefail

PYTHON="${PYTHON:=NOT_SET}"
if [[ $PYTHON == "NOT_SET" ]]; then
  if command -v python3 &> /dev/null; then
    PYTHON=python3
  elif command -v python &> /dev/null; then
    PYTHON=python
  else
    echo "[install] Python is not installed."
    exit 1
  fi
fi

PYTHON_VERSION=$($PYTHON -V 2>&1 | grep -Eo '([0-9]+\.[0-9]+\.[0-9]+)$')
if [[ ${PYTHON_VERSION} < "3.7.0" && ${PYTHON_VERSION} < "3.10.0" ]]; then
  echo "[install] Python version 3.7.0 or higher is required."
  exit 1
fi

POETRY_HOME="${POETRY_HOME:=${HOME}/.poetry}"
POETRY_VERSION="${POETRY_VERSION:=1.1.12}"
if ! command -v "$POETRY_HOME"/bin/poetry &> /dev/null; then
  echo "[install] Poetry is not installed. Begin download and install."
  curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/1.1.12/get-poetry.py | POETRY_HOME=$POETRY_HOME POETRY_VERSION=$POETRY_VERSION $PYTHON -
fi

POETRY_INSTALL_OPTS="${POETRY_INSTALL_OPTS:="--no-interaction"}"
echo "[install] Begin installing project."
"$POETRY_HOME"/bin/poetry install $POETRY_INSTALL_OPTS

cat << 'EOF'
Project successfully installed.
To activate virtualenv run: $ poetry shell
Now you should access CLI script: $ fastapi-mvc --help
Alternatively you can access CLI script via poetry run: $ poetry run fastapi-mvc --help
To deactivate virtualenv simply type: $ deactivate
To activate shell completion:
 - for bash: $ echo 'eval "$(_FASTAPI_MVC_COMPLETE=source_bash fastapi-mvc)' >> ~/.bashrc
 - for zsh: $ echo 'eval "$(_FASTAPI_MVC_COMPLETE=source_zsh fastapi-mvc)' >> ~/.zshrc
 - for fish: $ echo 'eval "$(_FASTAPI_MVC_COMPLETE=source_fish fastapi-mvc)' >> ~/.config/fish/completions/fastapi-mvc.fish
EOF
