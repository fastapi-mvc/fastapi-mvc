{ pkgs ? import <nixpkgs> { } }:

pkgs.mkShell {
  buildInputs = [
    pkgs.curl
    pkgs.gnumake
    pkgs.podman
    pkgs.python39
    (pkgs.poetry.override { python = pkgs.python39; })
  ];
  shellHook = ''
    export POETRY_HOME=${pkgs.poetry}
    export POETRY_VIRTUALENVS_IN_PROJECT=true
    unset SOURCE_DATE_EPOCH
  '';
}
