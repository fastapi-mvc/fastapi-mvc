final: prev:
let
  src = final.fetchFromGitHub {
    owner = "SemMulder";
    repo = "poetry2nix";
    rev = "fix-750";
    sha256 = "0z0gzw7ic9mn846rz968r7v0z44pklzpn6pv4kfzg63xxr4wxzyr";
  };
  p2n = import "${src.out}/default.nix" { pkgs = final; poetry = final.poetry; };
in
{
  # p2n-final & p2n-prev refers to poetry2nix
  poetry2nix = p2n.overrideScope' (p2n-final: p2n-prev: {

    # py-final & py-prev refers to python packages
    defaultPoetryOverrides = p2n-prev.defaultPoetryOverrides.extend (py-final: py-prev: {

      flake8-todo = py-prev.flake8-todo.overridePythonAttrs (old: {
        buildInputs = old.buildInputs or [ ] ++ [ py-final.setuptools ];
      });

      sphinx = py-prev.sphinx.overridePythonAttrs (old: {
        buildInputs = old.buildInputs or [ ] ++ [ py-final.flit-core ];
      });

      pyyaml-include = py-prev.pyyaml-include.overridePythonAttrs (old: {
        postPatch = ''
          substituteInPlace setup.py --replace 'setup()' 'setup(version="${old.version}")'
        '';
      });

    });

  });
}
