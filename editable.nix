{ pkgs ? import <nixpkgs> { }
, python ? "python3"
}:

let
  fastapi-mvc = pkgs.poetry2nix.mkPoetryEnv {
    python = builtins.getAttr (python) pkgs;
    projectDir = ./.;
    pyproject = ./pyproject.toml;
    poetrylock = ./poetry.lock;
    editablePackageSources = {
      src = ./fastapi_mvc;
    };
  };
in
fastapi-mvc.env.overrideAttrs (oldAttrs: {
  buildInputs = [ pkgs.gnumake ];
})
