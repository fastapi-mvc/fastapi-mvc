#!/usr/bin/env bash

if [ -n "$DEBUG" ]; then
	set -x
fi

set -o errexit
set -o nounset
set -o pipefail

if ! command -v git &> /dev/null; then
  echo "[install] Git is not installed."
  exit 1
fi

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

PYTHON_MAJOR_VERSION=$($PYTHON -c 'import sys; print(sys.version_info[0])')
PYTHON_MINOR_VERSION=$($PYTHON -c 'import sys; print(sys.version_info[1])')
if [[ "$PYTHON_MAJOR_VERSION" -lt 3 ]] || [[ "$PYTHON_MINOR_VERSION" -lt 10 ]]; then
  echo "[install] Python version 3.10.0 or higher is required."
  exit 1
fi

UV_INSTALL_DIR="${UV_INSTALL_DIR:=${HOME}/.local/bin}"
UV_BINARY="${UV_BINARY:=${UV_INSTALL_DIR}/uv}"
UV_VERSION="${UV_VERSION:=0.10.0}"
if ! command -v "$UV_BINARY" &> /dev/null; then
  echo "[install] UV is not installed. Begin download and install."
  export UV_VERSION
  export UV_BINARY
  curl -LsSf https://astral.sh/uv/$UV_VERSION/install.sh | sh
fi

UV_INSTALL_OPTS="${UV_INSTALL_OPTS:="--extra test --extra docs"}"
echo "[install] Begin installing project."
echo "OPTS: $UV_INSTALL_OPTS"
"$UV_BINARY" sync $UV_INSTALL_OPTS

cat << 'EOF'
Project successfully installed.
To activate virtualenv run: $ uv venv
Now you should access CLI script: $ fastapi-mvc --help
Alternatively you can access CLI script via uv run: $ uv run fastapi-mvc --help
To deactivate virtualenv simply type: $ deactivate
To activate shell completion:
 - for bash: $ echo 'eval "$(_FASTAPI_MVC_COMPLETE=source_bash fastapi-mvc)' >> ~/.bashrc
 - for zsh: $ echo 'eval "$(_FASTAPI_MVC_COMPLETE=source_zsh fastapi-mvc)' >> ~/.zshrc
 - for fish: $ echo 'eval "$(_FASTAPI_MVC_COMPLETE=source_fish fastapi-mvc)' >> ~/.config/fish/completions/fastapi-mvc.fish
EOF
