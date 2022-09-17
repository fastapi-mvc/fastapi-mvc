{ pkgs ? import <nixpkgs> { }
, python ? "python3"
}:

let
  fastapi-mvc = pkgs.callPackage ./editable.nix {
    python = builtins.getAttr (python) pkgs;
    poetry2nix = pkgs.poetry2nix;
  };
in
fastapi-mvc.env.overrideAttrs (oldAttrs: {
  buildInputs = [ pkgs.gnumake ];
})
