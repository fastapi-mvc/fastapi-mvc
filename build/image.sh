#!/usr/bin/env bash

if [ -n "$DEBUG" ]; then
	set -x
fi

set -o errexit
set -o nounset
set -o pipefail

DIR=$(cd $(dirname "${BASH_SOURCE}") && pwd -P)


if command -v docker &> /dev/null; then
  echo "[image] Found docker-engine, begin building image."
  docker build -t fastapi-mvc:"$TAG" .
elif command -v podman &> /dev/null; then
  echo "[image] Found podman container engine, begin building image."
  podman build -t fastapi-mvc:"$TAG" .
else
  echo "[image] Neither docker nor podman container engine found."
  exit 1
fi
