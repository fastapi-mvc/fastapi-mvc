{ pkgs ? import <nixpkgs> { }
, fastapi-mvc
, name ? "fastapi-mvc"
, tag ? "latest"
}:

pkgs.dockerTools.buildImage {
  inherit name tag;

  contents = [
    fastapi-mvc
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
    Entrypoint = [ "${fastapi-mvc}/bin/fastapi-mvc" ];
  };
}
