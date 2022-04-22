import pytest
from fastapi.testclient import TestClient
from {{cookiecutter.package_name}}.app.asgi import get_app


@pytest.fixture
def client():
    # This is an example fixture for generated test sake.
    # By default there should be a 'app' fixture just like this under:
    # tests/unit/app/conftest.py
    app = get_app()
    with TestClient(app) as client:
        yield client
{%- for endpoint, method in cookiecutter.controller_endpoints.items() %}


def test_{{endpoint}}(client):
    response = client.{{method}}("/{{cookiecutter.controller_name}}/{{endpoint}}")
    assert response.status_code == 200
    assert response.json() == {"hello": "world"}


{%- endfor %}
{%- raw %}

{% endraw %}