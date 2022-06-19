{ pkgs ? import <nixpkgs> {} }:

let
  nonRootShadowSetup = { user, uid, gid ? uid }: with pkgs; [
    (
      writeTextDir "etc/shadow" ''
        root:!x:::::::
        ${user}:!:::::::
      ''
    )
    (
      writeTextDir "etc/passwd" ''
        root:x:0:0::/root:${runtimeShell}
        ${user}:x:${toString uid}:${toString gid}::/home/${user}:
      ''
    )
    (
      writeTextDir "etc/group" ''
        root:x:0:
        ${user}:x:${toString gid}:
      ''
    )
    (
      writeTextDir "etc/gshadow" ''
        root:x::
        ${user}:x::
      ''
    )
  ];

  fastapi_mvc = pkgs.callPackage ./default.nix {
    buildPythonPackage = pkgs.python39Packages.buildPythonPackage;
    fetchPypi = pkgs.python39Packages.fetchPypi;
    setuptools = pkgs.python39.pkgs.setuptools;
    cookiecutter = pkgs.python39.pkgs.cookiecutter;
    click = pkgs.python39.pkgs.click;
  };

  pyEnv = pkgs.python39.withPackages (ps: with ps; [
    fastapi_mvc
  ]);
in

pkgs.dockerTools.buildImage {
  name = "fastapi-mvc";
  tag = "latest";

  contents = [
    pyEnv
  ] ++ nonRootShadowSetup { uid = 999; user = "nonroot"; };

  config = {
    User = "nonroot";
    Entrypoint = [ "${pyEnv}/bin/python3" "-m" "fastapi_mvc" ];
  };
}
