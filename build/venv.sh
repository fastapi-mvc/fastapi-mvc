#!/usr/bin/env bash

if [ -n "$DEBUG" ]; then
	set -x
fi

set -o errexit
set -o nounset
set -o pipefail

DIR=$(cd $(dirname "${BASH_SOURCE}") && pwd -P)

if ! command -v python &> /dev/null; then
  echo "python is not installed"
  exit 1
fi

if ! command -v virtualenv &> /dev/null; then
  echo "virtualenv is not installed"
  exit 1
fi

PYTHON_VERSION=$(python -V 2>&1 | grep -Eo '([0-9]+\.[0-9]+\.[0-9]+)$')
if [[ ${PYTHON_VERSION} < "3.7.0" ]]; then
  echo "Please upgrade python to 3.7.0 or higher"
  exit 1
fi


echo "[venv] creating virtualenv"
virtualenv --python=python venv
echo "[venv] installing project"
venv/bin/pip install .

cat <<EOF
Project successfully installed in virtualenv
To activate virtualenv run from project root: $ source venv/bin/activate
Now you should access CLI binary: $ fastapi --help
To deactivate virtualenv simply type: $ deactivate
EOF