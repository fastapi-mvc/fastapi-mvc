{ pkgs ? import <nixpkgs> { } }:

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

  fastapi-mvc = pkgs.callPackage ./default.nix {
    python = pkgs.python39;
    poetry2nix = pkgs.poetry2nix;
  };

  pyEnv = fastapi-mvc.dependencyEnv;
in

pkgs.dockerTools.buildImage {
  name = "fastapi-mvc";
  tag = "latest";

  contents = [
    pyEnv
  ] ++ nonRootShadowSetup { uid = 999; user = "nonroot"; };

  config = {
    User = "nonroot";
    Entrypoint = [ "${pyEnv}/bin/fastapi-mvc" ];
  };
}
