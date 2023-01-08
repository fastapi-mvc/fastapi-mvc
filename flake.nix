{
  description = "Fastapi-mvc flake";
  nixConfig.bash-prompt = ''\n\[\033[1;32m\][nix-develop:\w]\$\[\033[0m\] '';

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-22.11";
    flake-utils.url = "github:numtide/flake-utils";
    flake-utils.inputs.nixpkgs.follows = "nixpkgs";
    poetry2nix = {
      url = "github:nix-community/poetry2nix?ref=1.38.0";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, flake-utils, poetry2nix }:
    {
      overlays.default = nixpkgs.lib.composeManyExtensions [
        poetry2nix.overlay
        (import ./overlay.nix)
        (final: prev: {
          fastapi-mvc = prev.callPackage ./default.nix {
            python = final.python3;
            poetry2nix = final.poetry2nix;
            git = final.git;
          };
          fastapi-mvc-dev = prev.callPackage ./editable.nix {
            python = final.python3;
            poetry2nix = final.poetry2nix;
          };
        })
      ];
    } // (flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          overlays = [ self.overlays.default ];
        };
      in
      rec {
        packages = {
          default = pkgs.fastapi-mvc;
          fastapi-mvc-py38 = pkgs.fastapi-mvc.override { python = pkgs.python38; };
          fastapi-mvc-py39 = pkgs.fastapi-mvc.override { python = pkgs.python39; };
          fastapi-mvc-py310 = pkgs.fastapi-mvc.override { python = pkgs.python310; };
          fastapi-mvc-py311 = (pkgs.fastapi-mvc.overrideAttrs (oldAttrs: {
            # Override import check. It will fail for now due to:
            # https://github.com/cython/cython/issues/4804
            pythonImportsCheck = [ ];
          })).override { python = pkgs.python311; };
          poetryEnv = pkgs.fastapi-mvc-dev;
        } // pkgs.lib.optionalAttrs pkgs.stdenv.isLinux {
          image = pkgs.callPackage ./image.nix {
            inherit pkgs;
            fastapi-mvc = pkgs.fastapi-mvc;
          };
        };

        apps = {
          fastapi-mvc = flake-utils.lib.mkApp { drv = pkgs.fastapi-mvc; };
          metrics = {
            type = "app";
            program = toString (pkgs.writeScript "metrics" ''
              export PATH="${pkgs.lib.makeBinPath [
                  pkgs.fastapi-mvc-dev
                  pkgs.git
              ]}"
              echo "[nix][metrics] Run fastapi-mvc PEP 8 checks."
              flake8 --select=E,W,I --max-line-length 88 --import-order-style pep8 --statistics --count fastapi_mvc
              echo "[nix][metrics] Run fastapi-mvc PEP 257 checks."
              flake8 --select=D --ignore D301 --statistics --count fastapi_mvc
              echo "[nix][metrics] Run fastapi-mvc pyflakes checks."
              flake8 --select=F --statistics --count fastapi_mvc
              echo "[nix][metrics] Run fastapi-mvc code complexity checks."
              flake8 --select=C901 --statistics --count fastapi_mvc
              echo "[nix][metrics] Run fastapi-mvc open TODO checks."
              flake8 --select=T --statistics --count fastapi_mvc tests
              echo "[nix][metrics] Run fastapi-mvc black checks."
              black --check fastapi_mvc
            '');
          };
          docs = {
            type = "app";
            program = toString (pkgs.writeScript "docs" ''
              export PATH="${pkgs.lib.makeBinPath [
                  pkgs.fastapi-mvc-dev
                  pkgs.git
              ]}"
              echo "[nix][docs] Build fastapi-mvc documentation."
              sphinx-build docs site
            '');
          };
          unit-test = {
            type = "app";
            program = toString (pkgs.writeScript "unit-test" ''
              export PATH="${pkgs.lib.makeBinPath [
                  pkgs.fastapi-mvc-dev
                  pkgs.git
                  pkgs.coreutils
              ]}"
              echo "[nix][unit-test] Run fastapi-mvc unit tests."
              pytest tests/unit
            '');
          };
          integration-test = {
            type = "app";
            program = toString (pkgs.writeScript "integration-test" ''
              export PATH="${pkgs.lib.makeBinPath [
                  pkgs.fastapi-mvc-dev
                  pkgs.git
                  pkgs.coreutils
                  pkgs.gnumake
                  pkgs.poetry
                  pkgs.bash
                  pkgs.findutils
              ]}"
              export POETRY_HOME=${pkgs.poetry}
              export POETRY_BINARY=${pkgs.poetry}/bin/poetry
              export POETRY_VIRTUALENVS_IN_PROJECT=true
              echo "[nix][integration-test] Run fastapi-mvc unit tests."
              pytest tests/integration
            '');
          };
          coverage = {
            type = "app";
            program = toString (pkgs.writeScript "coverage" ''
              export PATH="${pkgs.lib.makeBinPath [
                  pkgs.fastapi-mvc-dev
                  pkgs.git
                  pkgs.coreutils
                  pkgs.gnumake
                  pkgs.poetry
                  pkgs.bash
                  pkgs.findutils
              ]}"
              export POETRY_HOME=${pkgs.poetry}
              export POETRY_BINARY=${pkgs.poetry}/bin/poetry
              export POETRY_VIRTUALENVS_IN_PROJECT=true
              echo "[nix][coverage] Run fastapi-mvc tests coverage."
              pytest --cov-config=.coveragerc --cov=fastapi_mvc --cov-fail-under=90 --cov-report=xml --cov-report=term-missing tests
            '');
          };
          test = {
            type = "app";
            program = toString (pkgs.writeScript "test" ''
              ${apps.unit-test.program}
              ${apps.integration-test.program}
            '');
          };
        };

        devShells = {
          default = pkgs.fastapi-mvc-dev.env.overrideAttrs (oldAttrs: {
            buildInputs = [
              pkgs.git
              pkgs.poetry
            ];
          });
          poetry = import ./shell.nix { inherit pkgs; };
        };
      }));
}
