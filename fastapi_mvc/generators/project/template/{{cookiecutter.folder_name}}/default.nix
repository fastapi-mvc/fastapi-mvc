{ lib
, buildPythonPackage
, fetchPypi
, setuptools
, fastapi
, uvicorn
, gunicorn
, click
{%- if cookiecutter.redis == "yes" %}
, aioredis
{%- endif %}
{%- if cookiecutter.aiohttp == "yes" %}
, aiohttp
{%- endif %}
}:

buildPythonPackage rec {
  pname = "{{cookiecutter.folder_name}}";
  version = "0.1.0";

  src = ./.;

  buildInputs = [
    setuptools
  ];

  propagatedBuildInputs = [
    fastapi
    uvicorn
    gunicorn
    click
{%- if cookiecutter.redis == "yes" %}
    aioredis
{%- endif %}
{%- if cookiecutter.aiohttp == "yes" %}
    aiohttp
{%- endif %}
  ];

  pythonImportsCheck = [ "{{cookiecutter.package_name}}" ];

  meta = with lib; {
    homepage = "{{cookiecutter.repo_url}}";
    description = "{{cookiecutter.project_description}}";
  };
}
