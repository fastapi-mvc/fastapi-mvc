{ pkgs ? import <nixpkgs> { }
, python ? "python3"
}:

let
  pythonPackage = builtins.getAttr (python) pkgs;
  poetry = pkgs.poetry.override { python = pythonPackage; };
in
pkgs.mkShell {
  buildInputs = [
    pkgs.curl
    pkgs.gnumake
    pkgs.kubernetes-helm
    pkgs.kubectl
    pkgs.minikube
    pythonPackage
    poetry
  ];
  shellHook = ''
    export POETRY_HOME=${poetry}
    export POETRY_VIRTUALENVS_IN_PROJECT=true
    unset SOURCE_DATE_EPOCH
  '';
}
