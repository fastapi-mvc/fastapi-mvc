final: prev:
let
  src = final.fetchFromGitHub {
    owner = "nix-community";
    repo = "poetry2nix";
    rev = "1.31.0";
    sha256 = "06psv5mc7xg31bvjpg030mwnk0sv90cj5bvgsdmcwicifpl3k3yj";
  };
  p2n = import "${src.out}/default.nix" { pkgs = final; poetry = final.poetry; };
in
{
  # p2n-final & p2n-prev refers to poetry2nix
  poetry2nix = p2n.overrideScope' (p2n-final: p2n-prev: {

    # py-final & py-prev refers to python packages
    defaultPoetryOverrides = p2n-prev.defaultPoetryOverrides.extend (py-final: py-prev: {

      mdit-py-plugins = py-prev.mdit-py-plugins.overridePythonAttrs (old: {
        buildInputs = old.buildInputs or [ ] ++ [ py-final.flit-core ];
      });

      idna = py-prev.idna.overridePythonAttrs (old: {
        buildInputs = old.buildInputs or [ ] ++ [ py-final.flit-core ];
      });

      sphinx = py-prev.sphinx.overridePythonAttrs (old: {
        buildInputs = old.buildInputs or [ ] ++ [ py-final.flit-core ];
      });

    });

  });
}
