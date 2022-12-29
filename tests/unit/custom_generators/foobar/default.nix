{ python
, poetry2nix
}:

poetry2nix.mkPoetryEnv {
  inherit python;
  pyproject = ./pyproject.toml;
  poetrylock = ./poetry.lock;
}
