{ pkgs ? import <nixpkgs> { }
, python ? pkgs.python3
, poetry2nix ? pkgs.poetry2nix
}:

let
  myAppEnv = poetry2nix.mkPoetryEnv {
    inherit python;
    projectDir = ./.;
    pyproject = ./pyproject.toml;
    poetrylock = ./poetry.lock;

    editablePackageSources = {
      my-app = ./fastapi_mvc;
    };
  };
in
myAppEnv.env
