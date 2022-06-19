{ lib
, buildPythonPackage
, fetchPypi
, setuptools
, cookiecutter
, click
}:

buildPythonPackage rec {
  pname = "fastapi-mvc";
  version = "0.13.1";

  src = fetchPypi {
    inherit pname version;
    sha256 = "1f67vvxv59zdzwfh6bbldljh4xzlh3xcivj44ffrqly2259d1drq";
  };

  buildInputs = [
    setuptools
  ];

  propagatedBuildInputs = [
    cookiecutter
    click
  ];

  pythonImportsCheck = [ "fastapi_mvc" ];

  meta = with lib; {
    homepage = "https://github.com/rszamszur/fastapi-mvc";
    description = "Developer productivity tool for making high-quality FastAPI production-ready APIs.";
    license = licenses.mit;
  };
}
