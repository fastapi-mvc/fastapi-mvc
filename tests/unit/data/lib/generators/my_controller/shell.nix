{ pkgs ? import
    (builtins.fetchTarball {
      name = "22.05";
      url = "https://github.com/NixOS/nixpkgs/archive/72783a2d0dbbf030bff1537873dd5b85b3fb332f.tar.gz";
      sha256 = "1xggh6cim9kxl7nr6fwmsxzqqlnazyddak30xcd4api3f9g3slnz";
    })
    { }
}:

let
  copier = pkgs.callPackage ./default.nix {
    python = pkgs.python39;
    poetry2nix = pkgs.poetry2nix;
  };
in
copier.env.overrideAttrs (oldAttrs: {
  buildInputs = [
    pkgs.git
    pkgs.poetry
  ];
})
