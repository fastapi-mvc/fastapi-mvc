.DEFAULT_GOAL:=help

.EXPORT_ALL_VARIABLES:

ifndef VERBOSE
.SILENT:
endif

# set default shell
SHELL=/usr/bin/env bash -o pipefail -o errexit

TAG ?= $(shell cat TAG)
UV_INSTALL_DIR ?= ${HOME}/.local/bin
UV_BINARY ?= ${UV_INSTALL_DIR}/uv
UV_VERSION ?= 0.10.0

help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z0-9_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

.PHONY: show-version
show-version:  ## Display version
	echo -n "${TAG}"

.PHONY: build
build: ## Build fastapi-mvc package
	echo "[build] Build fastapi-mvc package."
	${UV_BINARY} build

.PHONY: install
install: ## Install fastapi-mvc with poetry
	@build/install.sh

.PHONY: image
image: ## Build fastapi-mvc image
	@build/image.sh

.PHONY: clean-image
clean-image: ## Clean fastapi-mvc image
	@build/clean-image.sh

.PHONY: metrics
metrics: install ## Run fastapi-mvc metrics checks
	echo "[metrics] Run fastapi-mvc PEP 8 checks."
	${UV_BINARY} run flake8 --select=E,W,I --max-line-length 88 --import-order-style pep8 --statistics --count fastapi_mvc
	echo "[metrics] Run fastapi-mvc PEP 257 checks."
	${UV_BINARY} run flake8 --select=D --ignore D301 --statistics --count fastapi_mvc
	echo "[metrics] Run fastapi-mvc pyflakes checks."
	${UV_BINARY} run flake8 --select=F --statistics --count fastapi_mvc
	echo "[metrics] Run fastapi-mvc code complexity checks."
	${UV_BINARY} run flake8 --select=C901 --statistics --count fastapi_mvc
	echo "[metrics] Run fastapi-mvc open TODO checks."
	${UV_BINARY} run flake8 --select=T --statistics --count fastapi_mvc tests
	echo "[metrics] Run fastapi-mvc black checks."
	${UV_BINARY} run black --check fastapi_mvc

.PHONY: unit-test
unit-test: install ## Run fastapi-mvc unit tests
	echo "[unit-test] Run fastapi-mvc unit tests."
	${UV_BINARY} run pytest tests/unit

.PHONY: integration-test
integration-test: install ## Run fastapi-mvc integration tests
	echo "[unit-test] Run fastapi-mvc integration tests."
	${UV_BINARY} run pytest tests/integration

.PHONY: coverage
coverage: install ## Run fastapi-mvc tests coverage
	echo "[coverage] Run fastapi-mvc tests coverage."
	${UV_BINARY} run pytest --cov=fastapi_mvc --cov-fail-under=90 --cov-report=xml --cov-report=term-missing tests

.PHONY: test
test: unit-test integration-test  ## Run fastapi-mvc tests

.PHONY: docs
docs: install ## Build fastapi-mvc documentation
	echo "[docs] Build fastapi-mvc documentation."
	${UV_BINARY} run sphinx-build docs site

.PHONY: mypy
mypy: install  ## Run fastapi-mvc mypy checks
	echo "[mypy] Run fastapi-mvc mypy checks."
	${UV_BINARY} run mypy fastapi_mvc
