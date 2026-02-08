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
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-25.11";
    flake-parts.url = "github:hercules-ci/flake-parts";
    pyproject-nix = {
      url = "github:pyproject-nix/pyproject.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    uv2nix = {
      url = "github:pyproject-nix/uv2nix";
      inputs.pyproject-nix.follows = "pyproject-nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    pyproject-build-systems = {
      url = "github:pyproject-nix/build-system-pkgs";
      inputs.pyproject-nix.follows = "pyproject-nix";
      inputs.uv2nix.follows = "uv2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    nix-utils = {
      url = "github:rszamszur/nix-utils";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, flake-parts, pyproject-nix, uv2nix, pyproject-build-systems, nix-utils }@inputs:
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
        packages =
          let
            mkProject =
              { python ? pkgs.python3
              }:
              let
                build = pkgs.callPackage ./build.nix {
                  inherit python pkgs src uv2nix pyproject-nix pyproject-build-systems;
                  lib = pkgs.lib;
                  nix-utils = nix-utils.lib;
                };
              in
              {
                "fastapi-mvc-${python.sourceVersion.major}${python.sourceVersion.minor}-wheel" = build.wheel;
                "fastapi-mvc-${python.sourceVersion.major}${python.sourceVersion.minor}-sdist" = build.sdist;
                "fastapi-mvc-${python.sourceVersion.major}${python.sourceVersion.minor}-venv" = build.virtualenv;
                "fastapi-mvc-${python.sourceVersion.major}${python.sourceVersion.minor}-app" = build.application;
              };

            src = nix-utils.lib.sources.filterPythonSources {
              path = ./.;
            };
          in
          {
            default = self'.packages.fastapi-mvc-311-venv;
          }
          // (mkProject { python = pkgs.python310; })
          // (mkProject { python = pkgs.python311; })
          // (mkProject { python = pkgs.python312; })
          // pkgs.lib.optionalAttrs pkgs.stdenv.isLinux {
            image = pkgs.callPackage ./image.nix {
              inherit pkgs;
              fastapi-mvc = self'.packages.fastapi-mvc-311-app;
            };
          };

        overlayAttrs = {
          inherit (config.packages) default;
        };

        apps = {
          fastapi-mvc = mkApp { drv = self'.packages.default; };
          metrics = {
            type = "app";
            program = toString (pkgs.writeScript "metrics" ''
              #!${pkgs.bash}/bin/bash
              export PATH="${pkgs.lib.makeBinPath [
                  self'.packages.default
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
              #!${pkgs.bash}/bin/bash
              export PATH="${pkgs.lib.makeBinPath [
                  self'.packages.default
                  pkgs.git
              ]}"
              echo "[nix][docs] Build fastapi-mvc documentation."
              sphinx-build docs site
            '');
          };
          unit-test = {
            type = "app";
            program = toString (pkgs.writeScript "unit-test" ''
              #!${pkgs.bash}/bin/bash
              export PATH="${pkgs.lib.makeBinPath [
                  self'.packages.default
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
              #!${pkgs.bash}/bin/bash
              export PATH="${pkgs.lib.makeBinPath [
                  self'.packages.default
                  pkgs.git
                  pkgs.coreutils
                  pkgs.gnumake
                  pkgs.uv
                  pkgs.bash
                  pkgs.findutils
                  pkgs.curl
              ]}"
              echo "[nix][integration-test] Run fastapi-mvc unit tests."
              pytest tests/integration
            '');
          };
          coverage = {
            type = "app";
            program = toString (pkgs.writeScript "coverage" ''
              #!${pkgs.bash}/bin/bash
              export PATH="${pkgs.lib.makeBinPath [
                  self'.packages.default
                  pkgs.git
                  pkgs.coreutils
                  pkgs.gnumake
                  pkgs.uv
                  pkgs.bash
                  pkgs.findutils
              ]}"
              echo "[nix][coverage] Run fastapi-mvc tests coverage."
              pytest --cov=fastapi_mvc --cov-fail-under=90 --cov-report=xml --cov-report=term-missing tests
            '');
          };
          mypy = {
            type = "app";
            program = toString (pkgs.writeScript "mypy" ''
              #!${pkgs.bash}/bin/bash
              export PATH="${pkgs.lib.makeBinPath [
                  self'.packages.default
                  pkgs.git
              ]}"
              echo "[nix][mypy] Run fastapi-mvc mypy checks."
              mypy fastapi_mvc
            '');
          };
          test = {
            type = "app";
            program = toString (pkgs.writeScript "test" ''
              #!${pkgs.bash}/bin/bash
              ${self'.apps.unit-test.program}
              ${self'.apps.integration-test.program}
            '');
          };
        };

        checks = {
          treefmt = pkgs.runCommand "treefmt" { } ''
            ${self'.formatter}/bin/treefmt --ci --working-dir ${self}
            touch $out
          '';
        };

        formatter = pkgs.writeShellApplication {
          name = "treefmt";
          text = ''treefmt "$@"'';
          runtimeInputs = [
            pkgs.deadnix
            pkgs.nixfmt
            pkgs.treefmt
          ];
        };

        devShells = {
          default = self'.devShells.virtualenv;
          virtualenv = pkgs.mkShell {
            name = "fastapi-mvc-venv";
            packages = [
              self'.packages.default
              self'.formatter
              pkgs.uv
              pkgs.git
            ];

            env = {
              UV_NO_SYNC = "1";
              UV_PYTHON = "${self'.packages.default}/bin/python";
              UV_PYTHON_DOWNLOADS = "never";
            };

            shellHook = ''
              # Undo dependency propagation by nixpkgs.
              unset PYTHONPATH
              # Get repository root using git. This is expanded at runtime by the editable `.pth` machinery.
              export REPO_ROOT=$(git rev-parse --show-toplevel)
            '';
          };
          dev-shell = pkgs.mkShell {
            name = "fastapi-mvc-dev-shell";
            packages = [
              self'.formatter
              pkgs.python3
              pkgs.uv
              pkgs.git
              pkgs.coreutils
              pkgs.gnumake
              pkgs.curl
            ];

            env = {
              UV_PYTHON = pkgs.python3.interpreter;
              UV_PYTHON_DOWNLOADS = "never";
            };

            shellHook = ''
              unset PYTHONPATH
            '';
          };
        };
      };
      flake = { };
    };
}
