final: prev: {
  # p2n-final & p2n-prev refers to poetry2nix
  poetry2nix = prev.poetry2nix.overrideScope' (p2n-final: p2n-prev: {

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
