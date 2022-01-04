#!/usr/bin/env bash

if [ -n "$DEBUG" ]; then
	set -x
fi

set -o errexit
set -o nounset
set -o pipefail

DIR=$(cd $(dirname "${BASH_SOURCE}") && pwd -P)


if command -v docker &> /dev/null; then
  echo "[image] Found docker-engine, begin removing image."
  docker rmi -f fastapi-mvc:"$TAG" || true
elif command -v podman &> /dev/null; then
  echo "[image] Found podman container engine, begin removing image."
  podman rmi -f fastapi-mvc:"$TAG" || true
else
  echo "[image] Neither docker nor podman container engine found."
  exit 1
fi
