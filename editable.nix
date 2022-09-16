{ python
, poetry2nix
}:

poetry2nix.mkPoetryEnv {
  inherit python;

  projectDir = ./.;
  pyproject = ./pyproject.toml;
  poetrylock = ./poetry.lock;

  editablePackageSources = {
    fastapi-mvc = ./.;
  };
}
