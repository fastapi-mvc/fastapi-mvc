{
  pkgs,
  lib,
  src,
  python,
  uv2nix,
  pyproject-nix,
  pyproject-build-systems,
  nix-utils,
}:

let
  inherit (nix-utils.sources)
    filterSources
    languageIgnoreFilesets
    languageFileFilters
    ;
  inherit (pkgs.lib.fileset) unions;

  workspace = uv2nix.lib.workspace.loadWorkspace {
    # Workaround for https://github.com/pyproject-nix/uv2nix/issues/179
    workspaceRoot = /. + (builtins.unsafeDiscardStringContext src);
  };
  workspaceOverlay = workspace.mkPyprojectOverlay { sourcePreference = "wheel"; };
  pyprojectOverrides = final: prev: {
    pyyaml-include = prev.pyyaml-include.overrideAttrs (old: {
      patch = ''
        substituteInPlace setup.py --replace 'setup()' 'setup(version="${old.version}")'
      '';
    });

    pydantic = prev.pydantic.overrideAttrs (old: {
      buildInputs = old.buildInputs or [ ] ++ [ pkgs.libxcrypt ];
    });

    flake8-todo = prev.flake8-todo.overrideAttrs (old: {
      buildInputs = old.buildInputs or [ ] ++ [ final.setuptools ];
    });

    sphinx = prev.sphinx.overrideAttrs (old: {
      buildInputs = old.buildInputs or [ ] ++ [ final.flit-core ];
    });

    sphinx-click = prev.sphinx-click.override {
      sourcePreference = "wheel";
    };

    pathspec = prev.pathspec.overrideAttrs (old: {
      buildInputs = old.buildInputs or [ ] ++ [ final.flit-core ];
    });

    plumbum = prev.plumbum.overrideAttrs (old: {
      buildInputs = old.buildInputs or [ ] ++ [
        final.hatch-vcs
        final.hatchling
      ];
    });

    pydocstyle = prev.pydocstyle.overrideAttrs (old: {
      buildInputs = old.buildInputs or [ ] ++ [
        final.poetry-core
        final.setuptools
      ];
    });

    iniconfig = prev.iniconfig.overrideAttrs (old: {
      buildInputs = old.buildInputs or [ ] ++ [
        final.hatch-vcs
        final.hatchling
        final.build
        final.setuptools-scm
      ];
    });
  };

  pythonSet =
    (pkgs.callPackage pyproject-nix.build.packages {
      inherit python;
    }).overrideScope
      (
        lib.composeManyExtensions [
          pyproject-build-systems.overlays.wheel
          workspaceOverlay
          pyprojectOverrides
        ]
      );
  editableOverlay = workspace.mkEditablePyprojectOverlay {
    # Use environment variable
    root = "$REPO_ROOT";
    # Optional: Only editable for these packages
    members = [ "fastapi-mvc" ];
  };

  # Override previous set with our overridable overlay.
  editablePythonSet = pythonSet.overrideScope (
    lib.composeManyExtensions [
      editableOverlay

      # Apply fixups for building an editable package of your workspace packages
      (final: prev: {
        # It's a good idea to filter the sources goting into an editable build
        # so the editable package doesn't have to be rebuild on every change.
        fastapi-mvc = prev.fastapi-mvc.overrideAttrs (old: {
          src =
            let
              ignoreFilesets = languageIgnoreFilesets old.src;
              ignoreFileFilters = languageFileFilters old.src;
            in
            filterSources {
              path = old.src;
              positiveFileset = unions ([
                (old.src + "/README.md")
                (old.src + "/uv.lock")
                (old.src + "/pyproject.toml")
                (old.src + "/fastapi_mvc/")
                (old.src + "/flake.nix")
                (old.src + "/flake.lock")
                (old.src + "/build.nix")
                (old.src + "/image.nix")
              ]);
              negativeFileset = unions ([
                ignoreFilesets.common
                ignoreFilesets.python.venv
                ignoreFilesets.python.build
                ignoreFilesets.python.pyTest
                ignoreFilesets.python.config
                ignoreFileFilters.common
                ignoreFileFilters.python.pyCache
                ignoreFileFilters.python.pyTestCache
                ignoreFileFilters.python.eggInfo
              ]);
            };

          # Hatchling (our build system) has a dependency on the `editables` package when building editables.
          #
          # In normal Python flows this dependency is dynamically handled, and doesn't need to be explicitly declared.
          # This behaviour is documented in PEP-660
          #
          # With Nix the dependency needs to be explicitly declared.
          nativeBuildInputs = old.nativeBuildInputs ++ final.resolveBuildSystem { editables = [ ]; };
        });
      })
    ]
  );

  # Build virtual environment, with local packages being editable.
  #
  # Enable all optional dependencies for development.
  virtualenv = editablePythonSet.mkVirtualEnv "fastapi-mvc-dev-env" workspace.deps.all;

  sdist =
    (pythonSet.fastapi-mvc.override {
      pyprojectHook = pythonSet.pyprojectDistHook;
    }).overrideAttrs
      (_: {
        env.uvBuildType = "sdist";
      });
  wheel = pythonSet.fastapi-mvc.override {
    pyprojectHook = pythonSet.pyprojectDistHook;
  };

  util = pyproject-nix.build.util {
    runCommand = pkgs.runCommand;
    python3 = pythonSet.python;
  };
  application = util.mkApplication {
    venv = pythonSet.mkVirtualEnv "application-env" workspace.deps.default;
    package = pythonSet.fastapi-mvc;
  };
in
{
  inherit
    sdist
    wheel
    virtualenv
    application
    ;
}
