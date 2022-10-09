PYTHON_NIXPKG ?= python39

.PHONY: build
build:  ## Build fastapi-mvc Nix package
	echo "[nix][build] Build fastapi-mvc Nix package."
	@nix-build -E 'with import <nixpkgs> { overlays = [ (import ./overlay.nix) ]; }; callPackage ./default.nix {python = pkgs.${PYTHON_NIXPKG}; poetry2nix = pkgs.poetry2nix;}'

.PHONY: install
install:  ## Install fastapi-mvc env with Nix
	echo "[nix][install] Install fastapi-mvc env with Nix"
	@nix-build -E 'with import <nixpkgs> { overlays = [ (import ./overlay.nix) ]; }; callPackage ./editable.nix {python = pkgs.${PYTHON_NIXPKG}; poetry2nix = pkgs.poetry2nix;}'

.PHONY: image
image:  ## Build fastapi-mvc image with Nix
	echo "[nix][image] Build fastapi-mvc image with Nix."
	@nix-build image.nix

.PHONY: docs
docs: install  ## Build fastapi-mvc documentation
	echo "[docs] Build fastapi-mvc documentation."
	result/bin/sphinx-build docs site

.PHONY: metrics
metrics: install  ## Run fastapi-mvc metrics checks
	echo "[nix][metrics] Run fastapi-mvc PEP 8 checks."
	result/bin/flake8 --select=E,W,I --max-line-length 88 --import-order-style pep8 --statistics --count fastapi_mvc
	echo "[nix][metrics] Run fastapi-mvc PEP 257 checks."
	result/bin/flake8 --select=D --ignore D301 --statistics --count fastapi_mvc
	echo "[nix][metrics] Run fastapi-mvc pyflakes checks."
	result/bin/flake8 --select=F --statistics --count fastapi_mvc
	echo "[nix][metrics] Run fastapi-mvc code complexity checks."
	result/bin/flake8 --select=C901 --statistics --count fastapi_mvc
	echo "[nix][metrics] Run fastapi-mvc open TODO checks."
	result/bin/flake8 --select=T --statistics --count fastapi_mvc tests
	echo "[nix][metrics] Run fastapi-mvc black checks."
	result/bin/black --check fastapi_mvc

.PHONY: unit-test
unit-test: install  ## Run fastapi-mvc unit tests
	echo "[nix][unit-test] Run fastapi-mvc unit tests."
	result/bin/pytest tests/unit

.PHONY: integration-test
integration-test: install  ## Run fastapi-mvc integration tests
	echo "[nix][integration-test] Run fastapi-mvc unit tests."
	result/bin/pytest tests/integration

.PHONY: coverage
coverage: install ## Run fastapi-mvc tests coverage
	echo "[nix][coverage] Run fastapi-mvc tests coverage."
	result/bin/pytest --cov-config=.coveragerc --cov=fastapi_mvc --cov-fail-under=90 --cov-report=xml --cov-report=term-missing tests

.PHONY: test
test: unit-test integration-test coverage ## Run fastapi-mvc tests
