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

  {{cookiecutter.folder_name}} = pkgs.callPackage ./default.nix {
    buildPythonPackage = pkgs.python39Packages.buildPythonPackage;
    fetchPypi = pkgs.python39Packages.fetchPypi;
    setuptools = pkgs.python39.pkgs.setuptools;
    fastapi = pkgs.python39.pkgs.fastapi;
    uvicorn = pkgs.python39.pkgs.uvicorn;
    gunicorn = pkgs.python39.pkgs.gunicorn;
    click = pkgs.python39.pkgs.click;
{%- if cookiecutter.redis == "yes" %}
    aioredis = pkgs.python39.pkgs.aioredis;
{%- endif %}
{%- if cookiecutter.aiohttp == "yes" %}
    aiohttp = pkgs.python39.pkgs.aiohttp;
{%- endif %}
  };

  pyEnv = pkgs.python39.withPackages (ps: with ps; [
    {{cookiecutter.folder_name}}
  ]);
in

pkgs.dockerTools.buildImage {
  name = "{{cookiecutter.folder_name}}";
  tag = "latest";

  contents = [
    pyEnv
  ] ++ nonRootShadowSetup { uid = 999; user = "nonroot"; };

  config = {
    User = "nonroot";
    Entrypoint = [ "${pyEnv}/bin/python3" "-m" "{{cookiecutter.package_name}}" ];
  };
}
