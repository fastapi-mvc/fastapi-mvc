{ pkgs ? import <nixpkgs> { overlays = [ (import ./overlay.nix) ]; }
, name ? "fastapi-mvc"
, tag ? "latest"
}:

let
  app = pkgs.callPackage ./default.nix {
    python = pkgs.python39;
    poetry2nix = pkgs.poetry2nix;
  };
in

pkgs.dockerTools.buildImage {
  inherit name tag;

  contents = [
    app
    pkgs.bash
    pkgs.coreutils
    pkgs.curl
    pkgs.cacert
    pkgs.gnumake
  ];

  runAsRoot = ''
    #!${pkgs.runtimeShell}
    ${pkgs.dockerTools.shadowSetup}
    mkdir /tmp
    chmod 777 -R /tmp
    mkdir -p /usr/bin
    ln -s ${pkgs.coreutils}/bin/env /usr/bin/env
    groupadd -r nonroot
    useradd -r -g nonroot nonroot
    mkdir -p /home/nonroot
    chown nonroot:nonroot /home/nonroot
  '';

  config = {
    Env = [
      "SSL_CERT_FILE=${pkgs.cacert}/etc/ssl/certs/ca-bundle.crt"
      "PYTHONDONTWRITEBYTECODE=1"
      "PYTHONUNBUFFERED=1"
    ];
    User = "nonroot";
    WorkingDir = "/home/nonroot";
    Entrypoint = [ "${app}/bin/fastapi-mvc" ];
  };
}
