{
  description = "Fastapi-mvc flake";
  nixConfig = {
    bash-prompt = ''\n\[\033[1;32m\][nix-develop:\w]\$\[\033[0m\] '';
    extra-trusted-public-keys = [
      "fastapi-mvc.cachix.org-1:knQ8Qo41bnhBmOB6Sp0UH10EV76AXW5o69SbAS668Fg="
    ];
    extra-substituters = [
      "https://fastapi-mvc.cachix.org"
    ];
  };

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-22.11";
    flake-parts.url = "github:hercules-ci/flake-parts";
    poetry2nix = {
      url = "github:nix-community/poetry2nix?ref=1.40.1";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, flake-parts, poetry2nix }@inputs:
    let
      mkApp =
        { drv
        , name ? drv.pname or drv.name
        , exePath ? drv.passthru.exePath or "/bin/${name}"
        }:
        {
          type = "app";
          program = "${drv}${exePath}";
        };
    in
    flake-parts.lib.mkFlake { inherit inputs; } {
      imports = [
        inputs.flake-parts.flakeModules.easyOverlay
      ];
      systems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      perSystem = { config, self', inputs', pkgs, system, ... }: {
        # Add poetry2nix overrides to nixpkgs
        _module.args.pkgs = import nixpkgs {
          inherit system;
          overlays = [ self.overlays.poetry2nix ];
        };

        packages =
          let
            mkProject =
              { python ? pkgs.python3
              }:
              pkgs.callPackage ./default.nix {
                inherit python;
                poetry2nix = pkgs.poetry2nix;
                git = pkgs.git;
              };
          in
          {
            default = mkProject { };
            fastapi-mvc-py38 = mkProject { python = pkgs.python38; };
            fastapi-mvc-py39 = mkProject { python = pkgs.python39; };
            fastapi-mvc-py310 = mkProject { python = pkgs.python310; };
            fastapi-mvc-py311 = mkProject { python = pkgs.python311; };
            fastapi-mvc-dev = pkgs.callPackage ./editable.nix {
              poetry2nix = pkgs.poetry2nix;
              python = pkgs.python3;
            };
          } // pkgs.lib.optionalAttrs pkgs.stdenv.isLinux {
            image = pkgs.callPackage ./image.nix {
              inherit pkgs;
              fastapi-mvc = config.packages.default;
            };
          };

        overlayAttrs = {
          inherit (config.packages) default;
        };

        apps = {
          fastapi-mvc = mkApp { drv = config.packages.default; };
          metrics = {
            type = "app";
            program = toString (pkgs.writeScript "metrics" ''
              export PATH="${pkgs.lib.makeBinPath [
                  config.packages.fastapi-mvc-dev
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
                  config.packages.fastapi-mvc-dev
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
                  config.packages.fastapi-mvc-dev
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
                  config.packages.fastapi-mvc-dev
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
                  config.packages.fastapi-mvc-dev
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
              pytest --cov=fastapi_mvc --cov-fail-under=90 --cov-report=xml --cov-report=term-missing tests
            '');
          };
          mypy = {
            type = "app";
            program = toString (pkgs.writeScript "mypy" ''
              export PATH="${pkgs.lib.makeBinPath [
                  config.packages.fastapi-mvc-dev
                  pkgs.git
              ]}"
              echo "[nix][mypy] Run fastapi-mvc mypy checks."
              mypy fastapi_mvc
            '');
          };
          test = {
            type = "app";
            program = toString (pkgs.writeScript "test" ''
              ${config.apps.unit-test.program}
              ${config.apps.integration-test.program}
            '');
          };
        };

        devShells = {
          default = config.packages.fastapi-mvc-dev.env.overrideAttrs (oldAttrs: {
            buildInputs = [
              pkgs.git
              pkgs.poetry
              pkgs.coreutils
              pkgs.findutils
            ];
          });
          poetry = import ./shell.nix { inherit pkgs; };
        };
      };
      flake = {
        overlays.poetry2nix = nixpkgs.lib.composeManyExtensions [
          poetry2nix.overlay
          (import ./overlay.nix)
        ];
      };
    };
}
