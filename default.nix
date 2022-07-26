{ lib
, python
, poetry2nix
}:

poetry2nix.mkPoetryApplication rec {
  inherit python;

  projectDir = ./.;
  src = ./.;
  pyproject = ./pyproject.toml;
  poetrylock = ./poetry.lock;

  pythonImportsCheck = [ "fastapi_mvc" ];

  meta = with lib; {
    homepage = "https://github.com/rszamszur/fastapi-mvc";
    description = "Developer productivity tool for making high-quality FastAPI production-ready APIs.";
    license = licenses.mit;
  };
}
