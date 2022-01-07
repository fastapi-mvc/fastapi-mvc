.DEFAULT_GOAL:=help

.EXPORT_ALL_VARIABLES:

ifndef VERBOSE
.SILENT:
endif

# set default shell
SHELL=/usr/bin/env bash -o pipefail -o errexit

# Use the 0.0 tag for testing, it shouldn't clobber any release builds
TAG ?= $(shell cat TAG)

REPO_INFO ?= $(shell git config --get remote.origin.url)
COMMIT_SHA ?= git-$(shell git rev-parse --short HEAD)

help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z0-9_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

.PHONY: image
image:  ## Build fastapi-mvc image
	@build/image.sh

.PHONY: clean-image
clean-image:  ## Clean fastapi-mvc image
	@build/clean-image.sh

.PHONY: install
install:  ## Install fastapi-mvc with poetry
	@build/install.sh

.PHONY: metrics
metrics: install ## Run fastapi-mvc metrics checks
	@build/metrics.sh

.PHONY: unit-test
unit-test: install ## Run fastapi-mvc unit tests
	@build/unit-test.sh

.PHONY: integration-test
integration-test: install ## Run fastapi-mvc integration tests
	@build/integration-test.sh

.PHONY: show-version
show-version:
	echo -n $(TAG)
