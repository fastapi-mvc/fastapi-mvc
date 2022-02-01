#!/usr/bin/env bash

if [ -n "$DEBUG" ]; then
	set -x
fi

set -o errexit
set -o nounset
set -o pipefail

if [ -e /tmp/test-project ]; then
    rm -r /tmp/test-project
fi

POETRY_HOME="${POETRY_HOME:=${HOME}/.poetry}"
echo "[template-checks] Generate test-project."
"$POETRY_HOME"/bin/poetry run fastapi-mvc new -I /tmp/test-project

cd /tmp/test-project
echo "[template-checks] Run style guide checks."
make metrics
echo "[template-checks] Run unit tests."
make unit-test
echo "[template-checks] Run integration tests."
make integration-test
