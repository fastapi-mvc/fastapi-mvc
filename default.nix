{ lib
, python
, poetry2nix
, git
}:

poetry2nix.mkPoetryApplication {
  inherit python;

  projectDir = ./.;
  pyproject = ./pyproject.toml;
  poetrylock = ./poetry.lock;

  pythonImportsCheck = [ "fastapi_mvc" ];

  propagatedBuildInputs = [
    git
  ];

  meta = with lib; {
    homepage = "https://github.com/fastapi-mvc/fastapi-mvc";
    description = "Developer productivity tool for making high-quality FastAPI production-ready APIs.";
    license = licenses.mit;
  };
}
